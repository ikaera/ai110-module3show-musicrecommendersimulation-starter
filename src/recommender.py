import csv
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
    """Reads songs.csv into a list of dicts with numeric fields converted to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = float(row["popularity"])
            row["explicit"] = row["explicit"] == "True"
            row["instrumentalness"] = float(row["instrumentalness"])
            row["liveness"] = float(row["liveness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences using the weighted Algorithm Recipe; returns (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        points = 1.5 * (1 - abs(song["energy"] - target_energy))
        score += points
        reasons.append(f"energy closeness (+{points:.2f})")

    target_valence = user_prefs.get("valence")
    if target_valence is not None:
        points = 1.0 * (1 - abs(song["valence"] - target_valence))
        score += points
        reasons.append(f"valence closeness (+{points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        matches = (likes_acoustic and song["acousticness"] > 0.5) or (not likes_acoustic and song["acousticness"] <= 0.5)
        if matches:
            score += 0.5
            reasons.append("acousticness preference match (+0.5)")

    preferred_decade = user_prefs.get("preferred_decade")
    if preferred_decade is not None and song["release_decade"] == preferred_decade:
        score += 0.5
        reasons.append("release decade match (+0.5)")

    target_popularity = user_prefs.get("target_popularity")
    if target_popularity is not None:
        points = 1.0 * (1 - abs(song["popularity"] - target_popularity) / 100)
        score += points
        reasons.append(f"popularity closeness (+{points:.2f})")

    preferred_language = user_prefs.get("preferred_language")
    if preferred_language is not None and song["language"] == preferred_language:
        score += 0.5
        reasons.append("language match (+0.5)")

    target_instrumentalness = user_prefs.get("target_instrumentalness")
    if target_instrumentalness is not None:
        points = 0.5 * (1 - abs(song["instrumentalness"] - target_instrumentalness))
        score += points
        reasons.append(f"instrumentalness closeness (+{points:.2f})")

    target_liveness = user_prefs.get("target_liveness")
    if target_liveness is not None:
        points = 0.5 * (1 - abs(song["liveness"] - target_liveness))
        score += points
        reasons.append(f"liveness closeness (+{points:.2f})")

    preferred_secondary_mood = user_prefs.get("preferred_secondary_mood")
    if preferred_secondary_mood is not None and song["secondary_mood"] == preferred_secondary_mood:
        score += 0.5
        reasons.append("secondary mood match (+0.5)")

    allow_explicit = user_prefs.get("allow_explicit")
    if allow_explicit is not None and song["explicit"] and not allow_explicit:
        score -= 1.0
        reasons.append("explicit content penalty (-1.0)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, ranks by score, and returns the top k as (song, score, explanation)."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    top_k = ranked[:k]
    return [(song, score, ", ".join(reasons)) for song, score, reasons in top_k]
