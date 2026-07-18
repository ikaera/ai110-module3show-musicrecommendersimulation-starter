# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1 (Add Advanced Song Features): add 7+ new song attributes not in the baseline data, update `data/songs.csv` and the scoring logic in `src/recommender.py` so the new attributes actually affect scoring, and add a demo profile that exercises them.

**Prompts used:**

- "Optional Extensions — Challenge 1: Add Advanced Song Features. Introduce 7 or more complex attributes... Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes. In ai_interactions.md, document the agentic workflow..."
- (Plan proposed by the assistant, approved with a plain "yes"): 7 new columns — `popularity` (0-100), `release_decade`, `explicit`, `language`, `instrumentalness` (0-1), `liveness` (0-1), `secondary_mood` — each derived deterministically from the existing `genre`/`mood`/`valence`/`danceability` columns (not random), plus 6 new scoring checks and 1 new penalty rule (explicit content) in `score_song`.

**What did the agent generate or change?**

- Wrote a one-off Python script (in the scratchpad, not committed) that read the existing 38-row `songs.csv`, computed all 7 new columns per row using genre/mood lookup tables, and wrote an expanded CSV with 17 columns total.
- Replaced `data/songs.csv` with the expanded version (38 rows, 7 new columns each).
- Updated `load_songs()` in `src/recommender.py` to convert `popularity`, `instrumentalness`, `liveness` to floats and `explicit` to a real Python bool.
- Added 7 new checks to `score_song()`: decade match (+0.5), popularity closeness (up to +1.0), language match (+0.5), instrumentalness closeness (up to +0.5), liveness closeness (up to +0.5), secondary mood match (+0.5), and an explicit-content penalty (-1.0) — all gated behind `.get()` so profiles without these keys are unaffected.
- Added a `"Clean Mainstream 2020s"` profile to `src/main.py` that sets all 7 new preference keys, to prove the new scoring paths actually fire.

**What did you verify or fix manually?**

- Ran `python -m src.main` and read the full breakdown for the new profile — confirmed `Pulse Overdrive` (EDM, 2020s, high popularity, English, correct secondary mood) won cleanly with every new check contributing points, and that `Concrete Bloom` (hiphop, flagged `explicit=True`) correctly took the -1.0 penalty and dropped to #5.
- Ran `pytest` — both existing tests (unrelated to the new columns) still pass, confirming the change didn't break the dataclass-based `Recommender` path.
- Manually reviewed the genre→decade/language/instrumentalness/liveness lookup tables for plausibility (e.g. classical/ambient marked mostly instrumental, punk/metal/hiphop flagged explicit, jazz/blues/folk given higher liveness) rather than trusting the script's output blindly.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

**Strategy pattern.** Instead of building 4 separate scoring functions (a lot of duplicated logic), the actual scoring *algorithm shape* stays exactly the same — same checks, same order — but the *weights* used inside it become a swappable object. Each "mode" (Genre-First, Mood-First, Energy-Focused, Balanced) is really just a different weights dictionary, not different code.

**How did AI help you brainstorm or implement it?**

I asked the assistant (Claude, in this chat) to brainstorm a design pattern for "4 or more ranking strategies... that keeps your code modular," attaching the existing `recommender.py`. It proposed the Strategy pattern specifically because the four modes only ever differ by *point values*, never by which checks run or how they're combined — so the smallest correct change was parameterizing `score_song`'s hardcoded constants into a `weights` dict, rather than writing 4 near-duplicate functions (which would have violated DRY and been harder to keep in sync). It proposed the concrete shape: a `DEFAULT_WEIGHTS` dict, a `STRATEGIES` dict of named weight overrides built with dict-unpacking (`{**DEFAULT_WEIGHTS, "genre": 4.0, ...}`), and a `mode` parameter threaded through `recommend_songs` → `score_song`.

**How does the pattern appear in your final code?**

- `DEFAULT_WEIGHTS` and `STRATEGIES` in `src/recommender.py` (right before `score_song`) define the 4 strategies: `balanced`, `genre_first`, `mood_first`, `energy_focused`.
- `score_song(user_prefs, song, weights=None)` reads every point value from the `weights` dict (`w["genre"]`, `w["energy"]`, etc.) instead of hardcoded numbers — this is the "strategy" being injected.
- `recommend_songs(user_prefs, songs, k=5, mode="balanced")` looks up `STRATEGIES[mode]` and passes it into `score_song` for every song — this is where the caller picks which strategy to use.
- `src/main.py` demonstrates switching: it runs the same "Deep Intense Rock" profile through all 4 modes in a loop (`for mode in STRATEGIES:`) and prints each ranking, so the rankings visibly reorder based on which strategy is active.
