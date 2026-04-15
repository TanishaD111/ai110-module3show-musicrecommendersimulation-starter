from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]            = int(row["id"])
            row["energy"]        = float(row["energy"])
            row["tempo_bpm"]     = float(row["tempo_bpm"])
            row["valence"]       = float(row["valence"])
            row["danceability"]  = float(row["danceability"])
            row["acousticness"]  = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences using the finalized recipe.
    Returns (total_score, explanation).

    Scoring recipe (max 9.0 pts):
      genre_score        = 3.0 if genre matches else 0.0
      mood_score         = 2.0 if mood matches  else 0.0
      energy_score       = 1.0 - abs(song - target)
      valence_score      = 1.0 - abs(song - target)
      danceability_score = 1.0 - abs(song - target)
      acousticness_score = 1.0 - abs(song - target)
    """
    genre_score        = 3.0 if song["genre"] == user_prefs["genre"] else 0.0
    mood_score         = 2.0 if song["mood"]  == user_prefs["mood"]  else 0.0
    energy_score       = 1.0 - abs(song["energy"]       - user_prefs.get("energy",       0.5))
    valence_score      = 1.0 - abs(song["valence"]      - user_prefs.get("valence",      0.5))
    danceability_score = 1.0 - abs(song["danceability"] - user_prefs.get("danceability", 0.5))
    acousticness_score = 1.0 - abs(song["acousticness"] - user_prefs.get("acousticness", 0.5))

    total = genre_score + mood_score + energy_score + valence_score + danceability_score + acousticness_score

    reasons = []
    if genre_score > 0:
        reasons.append(f"genre match ({song['genre']})")
    if mood_score > 0:
        reasons.append(f"mood match ({song['mood']})")
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs.get('energy', 0.5):.2f}")
    explanation = ", ".join(reasons)

    return total, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Ranks all songs by score and returns the top k.
    Uses score_song as the judge for every song in the catalog.
    Required by src/main.py
    """
    """
    scored = []
    for song in songs:
        total, explanation = score_song(user_prefs, song)
        scored.append((song, total, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]"""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
