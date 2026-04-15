# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

Each Song in this recommender carries ten attributes: an ID, title, and artist for identification, plus seven features that describe how it sounds — genre (the musical style, like lofi or pop), mood (the emotional feel, like chill or intense), energy (a 0–1 scale of loudness and intensity), tempo in BPM, valence (how musically bright or dark the song feels), danceability (how groove-driven the rhythm is), and acousticness (how acoustic versus electronic the instrumentation is). 

The UserProfile stores a matching set of preferences: a favorite genre, a favorite mood, a target energy level as a float, and a boolean flag for whether the user prefers acoustic-sounding songs, which maps to a threshold on the song's acousticness value rather than an exact numeric match. There are float targets for valence and danceability, following the same proximity scoring approach used for energy.

To compute a score, the Recommender compares each song's attributes against the user's profile using two types of rules: categorical matching checks whether the song's mood and genre exactly equal the user's favorites, awarding the most points to mood since it's the strongest signal for whether a song feels right; proximity scoring measures how close each numeric feature (energy, valence, danceability, acousticness) is to the user's target, so a song that's slightly off is only slightly penalized rather than disqualified entirely. Every song receives a final score between 0.0 and 1.0 from combining these signals, and the Recommender selects the top x amount og songs by that score (default 5) as the final recommendations.

Taste Profile:
user_prefs = {
    # Categorical preferences
    "genre": "lofi",
    "mood": "chill",
    "target_energy": 0.38, # low-energy, calm listening
    "target_valence": 0.58, # slightly positive, not euphoric
    "target_danceability": 0.60, # moderate groove, not a dance track
    "target_acousticness": 0.75, # prefers acoustic/organic sound
}

class UserProfile:
    favorite_genre:       str
    favorite_mood:        str
    target_energy:        float
    target_valence:       float
    target_danceability:  float
    target_acousticness:  float

Algorithm recipe:
My recommender scores every song in the catalog against a user's taste profile using six features split into two groups: categorical and numeric. The categorical group — mood and genre — handles binary matching. If a song's mood exactly matches the user's preferred mood, it earns the largest share of points, since emotional feel is the strongest signal for whether a song belongs in a recommendation. If the genre also matches, it earns additional points. No partial credit is given for near-misses on either field — a chill song and an intense song are simply incompatible, regardless of how similar they sound on paper.

The numeric group — energy, valence, and danceability — uses proximity scoring. Rather than rewarding high or low values unconditionally, each feature measures how close the song's value is to the user's personal target. A song with energy 0.40 scores higher than one with energy 0.93 for a user targeting 0.38, even though the higher-energy song has "more" of the feature. Energy carries the most weight among the three since it is the most directly felt quality of a song, followed by valence, which captures emotional brightness, and danceability, which reflects rhythmic feel. Acousticness is handled separately as a boolean gate: if the user prefers acoustic-sounding music, songs with an acousticness score above 0.65 receive a bonus, and songs below that threshold do not — and vice versa for users who prefer electronic sounds.

The categorical and numeric scores are combined into a final score between 0.0 and 1.0, with categorical features weighted at 40% and numeric features at 60%. This split ensures that mood and genre are strong signals without completely overriding numeric closeness — a song in a slightly different genre can still rank well if its sound profile closely matches what the user wants. All 20 songs are scored, sorted from highest to lowest, and the top five are returned as recommendations

Finalized Recipe:
total_score = genre_score + mood_score + energy_score + valence_score + danceability_score + acousticness_score

Genre:        3.0          (max 3.0)
Mood:         2.0          (max 2.0)
4 continuous: 1.0 each     (max 4.0 combined)
─────────────────────────────────────
max = 9.0 pts

Categorical:  5.0 / 9.0 = 56%  ← categorical leads
Numeric:      4.0 / 9.0 = 44%

genre_score        = 3.0  if song.genre == user.favorite_genre  else 0.0
mood_score         = 2.0  if song.mood  == user.favorite_mood   else 0.0
energy_score       = 1.0 - abs(song.energy       - user.target_energy)
valence_score      = 1.0 - abs(song.valence      - user.target_valence)
danceability_score = 1.0 - abs(song.danceability - user.target_danceability)
acousticness_score = 1.0 - abs(song.acousticness - user.target_acousticness)

max possible = 9.0 pts

Bias:
This system might over-prioritize genre, but I do think this is important for a song preference. Mood would be rated higher than energy here too and the rest will be of lower priority. If someone prefers a certain artist, this recommender also does not take that into account. Tempo is also not considered since it appears difficult to work with as it can be a very diverse range. 

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

When the weight changes, the recommendation order is different

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

