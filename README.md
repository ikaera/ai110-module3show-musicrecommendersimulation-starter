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

[Explain design in plain language.]

Music apps usually use two strategies to recommend songs:

**1. Collaborative filtering** — look at other users.
If people who liked Song A and Song B also liked Song C,
recommend Song C to anyone who liked A and B but hasn't heard C yet. [1]

**2. Content-based filtering** — look at the song itself.
Match a song's own traits (genre, tempo, energy) to what a
listener already likes. [2]

Most real platforms use both. YouTube Music, for example, uses
collaborative filtering to find groups of users with similar taste,
and content-based filtering to explain _why_ a song fits — and to
recommend brand-new songs nobody has listened to yet. [3] Spotify does
something similar, partly to solve the "cold start" problem: a new
song has no listening history yet, so collaborative filtering alone
can't recommend it. [2]

**My version uses content-based filtering only.** I only have song
data and one user's preferences — no other users to compare against.

**What it prioritizes:** closeness, not size. For a number like energy,
the song closest to what the user wants scores highest — not the song
with the biggest number.

---

**Sources**
[1] [Music Tomorrow — Spotify Recommendation System Guide](https://music-tomorrow.com/blog/how-spotify-recommendation-system-works-complete-guide)
[2] [TechAhead — How Spotify's Recommendation System Works](https://www.techaheadcorp.com/blog/spotify-recommendation-system/)
[3] [Beatstorapon — YouTube Music Algorithm 2026](https://beatstorapon.com/blog/ultimate-youtube-music-algorithm-a-comprehensive-guide/)
Some prompts to answer:

[- What features does each `Song` use in your system

- For example: genre, mood, energy, tempo]

**What features does each `Song` use in your system?**

- `genre` — category, like pop, lofi, or rock
- `mood` — the vibe word, like happy, chill, or intense
- `energy` — number 0–1, how calm or intense the song feels
- `tempo_bpm` — how fast the song is, in beats per minute
- `valence` — number 0–1, how sad or happy the song sounds
- `danceability` — number 0–1, how easy the song is to move to
- `acousticness` — number 0–1, how acoustic vs. electronic it sounds

Simple description of each so it's easy to picture:

genre & mood — words, not numbers. Either they match the user's preference or they don't.
energy, valence, danceability, acousticness — numbers between 0 and 1. Think of 0 and 1 as opposite ends of a dial (calm ↔ intense, sad ↔ happy, still ↔ danceable, electronic ↔ acoustic).
tempo_bpm — the only feature that isn't 0–1, it's a real speed measurement (beats per minute).

**What information does your `UserProfile` store?**

- `favorite_genre` — the one genre this user prefers, like pop or jazz
- `favorite_mood` — the one mood this user prefers, like happy or chill
- `target_energy` — number 0–1, the energy level this user wants
- `likes_acoustic` — yes/no, does this user prefer acoustic-sounding songs

Simple description of each:

favorite_genre & favorite_mood — words, not numbers. Just what the user says they like.
target_energy — a target, not a maximum. A user with target_energy = 0.8 wants songs near 0.8, not necessarily the highest-energy songs available.
likes_acoustic — a simple true/false switch. No in-between.

One thing worth noticing: UserProfile is basically a smaller, simpler version of Song. It only stores preferences for 4 of the 7 song traits — there's no user preference for danceability or tempo_bpm in your current design. That's worth a one-line mention in your README or model card if you want to flag it as a possible "Future Work" idea (e.g., "add target_tempo so users can ask for faster or slower songs").

**How does your `Recommender` compute a score for each song?**

- `genre` matches `favorite_genre` → yes/no check, worth points if it matches
- `mood` matches `favorite_mood` → yes/no check, worth points if it matches
- `energy` compared to `target_energy` → closeness check, not "bigger is better"
- `valence` compared to a "positive" target → closeness check
- `acousticness` compared to `likes_acoustic` → matches the user's preference or not

All these small checks are added together into one final score for that song.

Simple description of each part:

Yes/no checks (genre, mood) — either the song matches what the user asked for, or it doesn't. No partial credit.
Closeness checks (energy, valence) — the song doesn't need to be "high" or "low," it needs to be near what the user wants. A song exactly at the target scores best; songs further away score worse either direction.
Final score — think of it like a report card. Each trait gives a small grade, and you add all the small grades together to get one final number for that song, out of 100.

**How do you choose which songs to recommend?**

- First, every song in the catalog gets its own score, one at a time
- Then, all the scored songs get sorted from highest score to lowest
- Finally, only the top `k` songs are shown to the user

      Songs → score each one → sort best to worst → keep top k → show user

---

### Algorithm Recipe (finalized weights)

| Check | Type | Points | Formula |
|---|---|---|---|
| genre match | yes/no | +2.0 | `2.0 if song.genre == favorite_genre else 0` |
| mood match | yes/no | +1.0 | `1.0 if song.mood == favorite_mood else 0` |
| energy closeness | numeric | up to +1.5 | `1.5 * (1 - abs(song.energy - target_energy))` |
| valence closeness | numeric | up to +1.0 | `1.0 * (1 - abs(song.valence - target_valence))` |
| acousticness preference | yes/no | +0.5 | `0.5 if (likes_acoustic and acousticness > 0.5) or (not likes_acoustic and acousticness <= 0.5) else 0` |

Max possible score ≈ 6.0. Genre counts double mood because it's the strongest taste signal; the closeness formulas reward being *near* the target, not just high or low.

**Expected bias:** genre is weighted 2x mood, so the system may over-recommend a song's genre match even when mood is the better fit — e.g., a sad rock song could outscore a happy song from a different genre. Worth watching for in Phase 4 evaluation.

---

### Diagram: How a recommendation gets made

    USER PROFILE                 SONG
    favorite_genre: pop          genre: pop
    favorite_mood: happy         mood: happy
    target_energy: 0.8           energy: 0.82
    likes_acoustic: false        acousticness: 0.18
           │                            │
           └───────────┬────────────────┘
                        ▼
                  score_song()
              (compares the two, adds
               up matches + closeness)
                        │
                        ▼
                  Song Score: 92/100
                        │
          (repeat for every song in catalog)
                        │
                        ▼
                 recommend_songs()
            (sorts all scores, keeps top k)
                        │
                        ▼
              Top 5 songs shown to user

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

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
