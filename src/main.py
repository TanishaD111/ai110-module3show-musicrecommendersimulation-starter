"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.38,   # low-energy, calm listening
        "valence":      0.58,   # slightly positive, not euphoric
        "danceability": 0.60,   # moderate groove, not a dance track
        "acousticness": 0.75,   # prefers acoustic/organic sound
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 40)
    print("  Top Recommendations")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 9.0")
        print(f"    Why:   {explanation}")
    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()
