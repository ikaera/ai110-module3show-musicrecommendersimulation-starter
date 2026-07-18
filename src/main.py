"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, STRATEGIES

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.85, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "valence": 0.5, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.4, "likes_acoustic": False},
    # Adversarial: high energy contradicts a "sad" mood - which signal wins?
    "Adversarial: Energetic but Sad": {"genre": "rock", "mood": "sad", "energy": 0.9, "valence": 0.2, "likes_acoustic": False},
    # Adversarial: genre with zero matches in the catalog - tests fallback to numeric-only scoring
    "Adversarial: Unknown Genre": {"genre": "grunge", "mood": "euphoric", "energy": 0.5, "valence": 0.5, "likes_acoustic": False},
    # Uses the Challenge 1 extended attributes: decade, popularity, language, instrumentalness, liveness, secondary mood, explicit filter
    "Clean Mainstream 2020s": {
        "genre": "edm", "mood": "energetic", "energy": 0.9, "valence": 0.8, "likes_acoustic": False,
        "preferred_decade": "2020s", "target_popularity": 90, "allow_explicit": False,
        "preferred_language": "english", "target_instrumentalness": 0.2, "target_liveness": 0.15,
        "preferred_secondary_mood": "electric",
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    k = 5
    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=k)
        print(f"\n=== Profile: {name} ===")
        print(f"Top {k} for {user_prefs}:\n")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")
            print()

    # Challenge 2: same profile, ranked under each scoring mode (Strategy pattern)
    mode_demo_profile = PROFILES["Deep Intense Rock"]
    for mode in STRATEGIES:
        recommendations = recommend_songs(mode_demo_profile, songs, k=3, mode=mode)
        print(f"\n=== Mode: {mode} (profile: Deep Intense Rock) ===\n")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{i}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"   Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
