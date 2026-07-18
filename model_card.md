# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

_Give your model a short, descriptive name._
\*Example: **VibeFinder 1.0\***

**VibeFinder 1.0**

---

## 2. Intended Use

_Describe what your recommender is designed to do and who it is for._

_Prompts:_

- _What kind of recommendations does it generate_
- _What assumptions does it make about the user_
- _Is this for real users or classroom exploration_

VibeFinder suggests songs to **one person at a time**, based on the taste they tell it about (their favorite genre, mood, and a few other preferences).

- **Who it's for:** a single listener exploring a small demo music catalog — not a real streaming app with millions of songs or users.
- **What it assumes:** the user already knows and can state their taste in simple terms, like "I like pop music, in a happy mood, pretty energetic."
- **Is this real or classroom-only?** This is a **classroom learning project**. It's built to teach how recommendation scoring works, not to be used as a real product. It has never been tested with real listeners.

---

## 3. How the Model Works

_Explain your scoring approach in simple language._

_Prompts:_

- _What features of each song are used (genre, energy, mood, etc.)_
- _What user preferences are considered_
- _How does the model turn those into a score_
- _What changes did you make from the starter logic_

_Avoid code here. Pretend you are explaining the idea to a friend who does not program._

Think of it like a very simple, very literal music-store clerk. You tell the clerk what you like, and the clerk checks every single song in the store, one at a time, giving each one a "grade" for how well it fits what you asked for.

**What it asks the user for (the "taste profile"):**

- Favorite **genre** (like "pop" or "rock") — a category word
- Favorite **mood** (like "happy" or "chill") — a vibe word
- Target **energy** — a number from 0 (very calm) to 1 (very intense)
- Target **valence** — a number from 0 (sad-sounding) to 1 (happy-sounding)
- Whether you like **acoustic** (unplugged, natural-instrument) sounding music or not

**How it scores each song:**

1. **Genre check:** does the song's genre exactly match what you asked for? If yes, +2 points. If no, +0.
2. **Mood check:** same idea, but for mood. Match = +1 point.
3. **Energy check:** instead of just rewarding "high energy," it rewards **closeness** — a song near your target energy scores well, whether your target is low or high. Worth up to +1.5 points.
4. **Valence check:** same closeness idea, but for how happy/sad the song sounds. Worth up to +1 point.
5. **Acoustic check:** does the song's "acoustic-ness" match whether you said you like acoustic music? Match = +0.5 points.

All five points get added together into one final score per song (max possible score is about 6.0). Every song in the catalog gets scored this way, then they're sorted highest-to-lowest, and the top few are shown to the user — along with the specific reasons for their score, so it's not a black box.

**What changed from the starter code:** the starter file only had empty placeholder functions. I wrote the actual CSV loading, the 5-part scoring formula above, and the sorting/ranking logic from scratch.

---

## 4. Data

_Describe the dataset the model uses._

_Prompts:_

- _How many songs are in the catalog_
- _What genres or moods are represented_
- _Did you add or remove data_
- _Are there parts of musical taste missing in the dataset_

- **Catalog size:** 38 songs (started from a 10-song sample file, and I added 28 more).
- **Song features:** each song has a genre, mood, energy (0–1), tempo in beats-per-minute, valence (0–1, sad↔happy), danceability (0–1), and acousticness (0–1, electronic↔acoustic).
- **What I added:** 28 new songs covering genres and moods missing from the starter set — including hiphop, metal, classical, country, EDM (electronic dance music), reggae, blues, funk, k-pop, folk, techno, soul, latin, punk, and gospel — plus new moods like sad, angry, nostalgic, and romantic.
- **What's still missing:** most genres only have **1 or 2 songs**, so there isn't much _variety within_ a genre — the system can't really compare "which pop song is best for you," only "is this a pop song or not." There's also no data on lyrics, artist popularity, or listening history — everything is based purely on the song's own sound attributes (this is called **content-based filtering** — recommending based on the _content_ of the item itself, rather than what similar _users_ liked).

---

## 5. Strengths

_Where does your system seem to work well_

_Prompts:_

- _User types for which it gives reasonable results_
- _Any patterns you think your scoring captures correctly_
- _Cases where the recommendations matched your intuition_

- **Clear winners when the catalog supports it:** when a user's favorite genre _and_ mood both exist in the catalog, the system finds an obviously-correct top pick. For example, a "pop, happy, high energy" profile correctly picked an upbeat pop song as its #1 result.
- **"Closeness" scoring works as intended:** for energy and valence, the system never just picks the most extreme song (loudest/happiest) — it picks whichever song is _nearest_ to what the user actually asked for. A user who wants medium energy gets medium-energy songs, not the most intense ones.
- **No crashes on missing data:** if a user's stated genre doesn't exist in the catalog at all, the system doesn't error out — it gracefully falls back to ranking by the remaining numeric checks (energy, valence, acoustic fit).

---

## 6. Limitations and Bias

_Where the system struggles or behaves unfairly._

_Prompts:_

- _Features it does not consider_
- _Genres or moods that are underrepresented_
- _Cases where the system overfits to one preference_
- _Ways the scoring might unintentionally favor some users_

- **Genre matches aren't real competition.** Most genres in the 38-song catalog only have 1–2 songs. So if a user's favorite genre has just one song, that song automatically wins the +2.0 genre bonus — not because it's a great fit, but because it's the _only_ option. There's no real "best pop song for you," only "the one pop song we have."
- **A "filter bubble" toward generic songs.** ("Filter bubble" = when a system keeps showing similar, safe results instead of a variety.) When a user's genre or mood doesn't exist in the catalog at all, the system falls back to comparing only energy and valence (happy/sad-ness). This quietly favors songs with _average_, middle-of-the-road energy and mood over songs with a bold, distinctive vibe — so unusual tastes get pushed toward "safe" songs instead of the songs that might actually stand out.
- **Some song traits are ignored entirely.** The scoring never looks at `danceability` (how easy a song is to dance to) or `tempo_bpm` (how fast the song is, in beats per minute). Two users who only differ on "I want something fast" vs. "I want something slow" will get the exact same recommendations today.

---

## 7. Evaluation

_How you checked whether the recommender behaved as expected._

_Prompts:_

- _Which user profiles you tested_
- _What you looked for in the recommendations_
- _What surprised you_
- _Any simple tests or comparisons you ran_

_No need for numeric metrics unless you created some._

**How I tested it:** I ran 5 different taste profiles through the recommender — 3 realistic ones (**High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**) and 2 "adversarial" ones, meaning profiles designed on purpose to try to confuse or break the scoring logic:

- **Energetic but Sad** — asks for high energy _and_ a sad mood at the same time (a contradiction most real songs don't have).
- **Unknown Genre** — asks for a genre ("grunge") that doesn't exist anywhere in the catalog.

Full terminal outputs for all 5 are pasted in the README's "Experiments You Tried" section.

**What surprised me:**

- For "Energetic but Sad," the system picked `Storm Runner` (an _intense_ rock song — not sad) over `Slow Fade` (which actually matches the sad mood). This happened because the genre match (+2.0) plus energy closeness outweighed the one point for correctly matching mood. It's "working exactly as coded," but it doesn't feel like the right recommendation for someone who explicitly asked for something sad.
- For "Unknown Genre," I expected an error or a nonsense result. Instead, it gracefully fell back to ranking purely by energy and valence closeness — no crash at all.

**Comparing profiles side by side:**

- **High-Energy Pop vs. Chill Lofi:** opposite energy targets (0.9 vs. 0.3) → completely different #1 songs. This is expected and good — energy closeness is doing exactly what it should.
- **Chill Lofi vs. Deep Intense Rock:** both have a real genre+mood match available in the catalog, so each cleanly wins on its own dedicated song. Shows genre+mood together are a strong signal _when the data actually supports it_.
- **Deep Intense Rock vs. Energetic but Sad:** same energy target and similar genre, but mood flips from "intense" to "sad" — yet the #1 song doesn't change. This exposes the "mood is too weak a signal" bias from section 6.
- **High-Energy Pop vs. Unknown Genre:** Pop has a strong genre+mood match to lean on; Unknown Genre has none, so its entire top 5 is decided by energy/valence alone — a preview of what _any_ user sees once their stated taste isn't represented in the catalog.

**One small experiment:** I temporarily doubled the energy weight and halved the genre weight, then reverted it. The #1 song in each profile barely changed — strong "triple matches" (genre + mood + energy all fitting) still won no matter the weights. The change only reshuffled songs in the middle of the list that had just one weak match. Lesson: weight-tuning mostly affects close calls, not clear winners.

---

## 8. Future Work

_Ideas for how you would improve the model next._

_Prompts:_

- _Additional features or preferences_
- _Better ways to explain recommendations_
- _Improving diversity among the top results_
- _Handling more complex user tastes_

- **Add more preferences:** let users state a target `tempo_bpm` (song speed) or `danceability`, so the system isn't blind to those traits.
- **Add a diversity penalty:** ("diversity penalty" = subtracting points to avoid repeating the same artist or genre too many times) so the top 5 doesn't feel repetitive.
- **Balance mood against genre:** testing showed mood can get completely overridden by genre + energy, even when mood is the more important signal for the user. Worth experimenting with a higher mood weight or a "mood must match" hard filter.

---

## 9. Personal Reflection

_A few sentences about your experience._

_Prompts:_

- _What you learned about recommender systems_
- _Something unexpected or interesting you discovered_
- _How this changed the way you think about music recommendation apps_

- **Biggest learning moment:** watching the "Energetic but Sad" test pick a happy-sounding rock song over one that actually matched the sad mood. It showed me that a recommender can do _exactly_ what it was programmed to do and still feel "wrong" to a person — the code wasn't buggy, the weights just didn't match human intuition.
- **How AI tools helped, and where I double-checked them:** the AI assistant sped up writing the CSV-loading and scoring code, and caught a Windows terminal encoding issue I wouldn't have noticed right away. But I still had to manually verify the _math_ behind the energy-closeness formula actually rewarded "near the target" instead of just "higher is better" — running the code and reading real output was the only way to confirm that, not just trusting that it looked correct.
- **What surprised me about simple algorithms:** a handful of `if` checks and one distance formula can still _feel_ like a real, thoughtful recommendation. It made me realize a lot of what feels like "AI magic" in real music apps might just be well-tuned weighted scoring, not something mysterious.
- **What I'd try next:** add the diversity penalty and test with a much bigger catalog that has more than 1–2 songs per genre, so genre matches become real competition instead of a default win.
