# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MyJammer

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

MyJammer generates a ranked list of song recommendations from a 20-song catalog based on a user's stated taste preferences. It assumes the user knows what genre and mood they want, and has a sense of how energetic, acoustic, and groove-driven they want their music to feel. It is designed for classroom exploration, not for real users, and uses a single hardcoded profile rather than learning from listening history.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song in the catalog gets a score based on how closely it matches what the user said they like. Genre is worth the most points, if a song's genre matches the user's favorite, it earns 3 points. Mood is worth 2 points for an exact match. Then four numeric features, energy, valence, danceability, and acousticness, each contribute up to 1 point based on how close the song's value is to the user's target. The closer the match, the more points. The maximum possible score is 9.0. Once every song is scored, they are sorted from highest to lowest and the top 5 are returned as recommendations. The starter logic only scored genre, mood, and energy, this version adds valence, danceability, and acousticness, and separates the scoring logic into its own function so it is easier to read and change.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 20 songs stored in a CSV file. Genres represented include lofi, pop, rock, indie pop, hip-hop, r&b, jazz, folk, classical, ambient, synthwave, and edm. Moods include chill, happy, intense, relaxed, moody, and focused. The original starter file had 10 songs, 10 more were added to improve variety. Despite this, the dataset is still very small and skews toward certain genres. There are no songs in genres like country, reggae, metal, or latin, and moods like sad, nostalgic, or romantic are entirely missing. Artist diversity, lyrics, language, and cultural context are not captured at all.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works well for users with a clear, specific taste profile, particularly lofi and chill listeners. For the lofi/chill/low-energy user profile used in testing, the top results (Midnight Coding and Library Rain) were exactly the songs a human would expect. The proximity scoring for energy and acousticness does a good job of separating nearly identical songs, a song with energy 0.35 and one with energy 0.42 get meaningfully different scores when the target is 0.38, rather than being treated the same. The separation between categorical and continuous signals also feels right: genre and mood dominate, while the numeric features refine the ranking within those categories.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Genre and mood use exact string matching, so "indie pop" and "pop" score 0 on genre even though they are closely related. A user who prefers pop might genuinely enjoy Rooftop Lights but the system will never rank it highly. Tempo is not considered at all, even though it is included in the dataset. There is no artist preference, two users could have identical numeric profiles but very different feelings about specific artists, and the system cannot distinguish them. The catalog itself is biased toward genres that are common in English-language streaming contexts, meaning users with tastes in underrepresented genres will get poor results. The system also has no memory, it cannot learn from what a user actually played or skipped.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

The primary profile tested was a lofi/chill listener targeting low energy (0.38), moderate valence (0.58), moderate danceability (0.60), and high acousticness (0.75). The expected top results were Midnight Coding and Library Rain, both lofi, both chill, both acoustic, and that is what the system returned. A secondary check was done with the original starter profile (pop/happy/0.8 energy), where Sunrise City scored highest as expected. One thing worth noting is that Focus Flow (lofi but focused mood) scored noticeably lower than the two chill lofi songs despite being nearly identical on all numeric features, which confirms the mood weight is doing its job.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

The most impactful improvement would be replacing exact genre and mood matching with fuzzy or similarity-based matching, so "indie pop" and "pop" would be treated as close rather than completely different. Adding artist preference as an optional signal would also help personalize results. A larger and more diverse catalog is essential, 20 songs is not enough to surface meaningful variety. It would also be useful to add a diversity constraint so the top 5 results do not all come from the same genre. Longer term, incorporating implicit feedback, what a user skips or replays, would allow the system to update preferences automatically rather than relying on a hardcoded profile.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this system made it clear how much of a recommender's behavior comes down to design decisions, specifically which features to include and how much weight to give each one. The choice to weight genre at 3 points versus mood at 2 points was not obvious at first, but reasoning through the math showed how much it shifted which songs ranked highest. What was surprising is how well a simple rule-based system can perform on a small, clean dataset, the results for the lofi/chill profile felt genuinely reasonable. It also changed how I think about apps like Spotify: what looks like intelligence is often a much larger version of this same loop, score every candidate, sort, return the top results, just with thousands of features and millions of songs instead of six features and twenty.