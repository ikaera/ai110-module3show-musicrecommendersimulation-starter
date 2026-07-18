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

DEFAULT_WEIGHTS = {
    "genre": 2.0, "mood": 1.0, "energy": 1.5, "valence": 1.0, "acoustic": 0.5,
    "decade": 0.5, "popularity": 1.0, "language": 0.5, "instrumentalness": 0.5,
    "liveness": 0.5, "secondary_mood": 0.5, "explicit_penalty": 1.0,
}

STRATEGIES = {
    "balanced": DEFAULT_WEIGHTS,
    "genre_first": {**DEFAULT_WEIGHTS, "genre": 4.0, "mood": 0.5, "energy": 0.75, "valence": 0.5},
    "mood_first": {**DEFAULT_WEIGHTS, "genre": 0.5, "mood": 3.0, "energy": 0.75, "valence": 0.5},
    "energy_focused": {**DEFAULT_WEIGHTS, "genre": 0.5, "mood": 0.5, "energy": 4.0, "valence": 2.0},
}

def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, List[str]]:
    """Scores a song against user preferences using a weighted Algorithm Recipe (a swappable strategy); returns (score, reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")

    if song["mood"] == user_prefs.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        points = w["energy"] * (1 - abs(song["energy"] - target_energy))
        score += points
        reasons.append(f"energy closeness (+{points:.2f})")

    target_valence = user_prefs.get("valence")
    if target_valence is not None:
        points = w["valence"] * (1 - abs(song["valence"] - target_valence))
        score += points
        reasons.append(f"valence closeness (+{points:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        matches = (likes_acoustic and song["acousticness"] > 0.5) or (not likes_acoustic and song["acousticness"] <= 0.5)
        if matches:
            score += w["acoustic"]
            reasons.append(f"acousticness preference match (+{w['acoustic']:.1f})")

    preferred_decade = user_prefs.get("preferred_decade")
    if preferred_decade is not None and song["release_decade"] == preferred_decade:
        score += w["decade"]
        reasons.append(f"release decade match (+{w['decade']:.1f})")

    target_popularity = user_prefs.get("target_popularity")
    if target_popularity is not None:
        points = w["popularity"] * (1 - abs(song["popularity"] - target_popularity) / 100)
        score += points
        reasons.append(f"popularity closeness (+{points:.2f})")

    preferred_language = user_prefs.get("preferred_language")
    if preferred_language is not None and song["language"] == preferred_language:
        score += w["language"]
        reasons.append(f"language match (+{w['language']:.1f})")

    target_instrumentalness = user_prefs.get("target_instrumentalness")
    if target_instrumentalness is not None:
        points = w["instrumentalness"] * (1 - abs(song["instrumentalness"] - target_instrumentalness))
        score += points
        reasons.append(f"instrumentalness closeness (+{points:.2f})")

    target_liveness = user_prefs.get("target_liveness")
    if target_liveness is not None:
        points = w["liveness"] * (1 - abs(song["liveness"] - target_liveness))
        score += points
        reasons.append(f"liveness closeness (+{points:.2f})")

    preferred_secondary_mood = user_prefs.get("preferred_secondary_mood")
    if preferred_secondary_mood is not None and song["secondary_mood"] == preferred_secondary_mood:
        score += w["secondary_mood"]
        reasons.append(f"secondary mood match (+{w['secondary_mood']:.1f})")

    allow_explicit = user_prefs.get("allow_explicit")
    if allow_explicit is not None and song["explicit"] and not allow_explicit:
        score -= w["explicit_penalty"]
        reasons.append(f"explicit content penalty (-{w['explicit_penalty']:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Scores every song under the chosen strategy's weights, ranks, and returns the top k as (song, score, explanation)."""
    weights = STRATEGIES.get(mode, DEFAULT_WEIGHTS)
    scored = [(song, *score_song(user_prefs, song, weights)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    top_k = ranked[:k]
    return [(song, score, ", ".join(reasons)) for song, score, reasons in top_k]
