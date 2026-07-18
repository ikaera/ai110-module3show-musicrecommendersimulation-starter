# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Most genres in the 38-song catalog have only 1-2 songs. That means a "genre match" is often a near-guarantee for whichever song exists in that genre, not real competition based on fit — if a user's favorite genre has one song, that song wins the +2.0 genre bonus by default even if its mood or energy is a poor match. Separately, when a user's genre or mood has zero matches in the catalog (e.g. an unlisted genre), the system falls back entirely to energy/valence closeness, which quietly favors songs with "average" energy and valence over songs with more extreme, distinctive vibes — a mild filter-bubble effect toward generic middle-of-the-road tracks. Finally, the scoring has no preference for `danceability` or `tempo_bpm`, so two users who differ only on how fast or danceable they like their music will get identical recommendations.

---

## 7. Evaluation  

I tested 5 profiles: **High-Energy Pop**, **Chill Lofi**, **Deep Intense Rock**, and two adversarial edge cases — **Energetic but Sad** (contradicting energy and mood signals) and **Unknown Genre** (a genre not in the catalog at all). Full terminal outputs are in the README's "Experiments You Tried" section.

**What surprised me:** for "Energetic but Sad," the system picked `Storm Runner` (an intense rock song, not sad at all) over `Slow Fade` (which actually matches the sad mood), because genre + energy closeness outscored the one point for a correct mood match. That's technically "working as coded," but it doesn't feel like the right call for someone who explicitly wants sad music. For "Unknown Genre," I expected the system to break or return junk — instead it gracefully fell back to ranking by energy/valence closeness alone, with no crash.

**Profile comparisons:**
- High-Energy Pop vs. Chill Lofi: opposite energy targets (0.9 vs 0.3) produce completely different top songs (`Sunrise City` vs `Library Rain`) — makes sense, energy closeness is doing its job.
- Chill Lofi vs. Deep Intense Rock: both have real genre+mood matches available in the catalog, so each wins cleanly on its own dedicated song (`Library Rain` vs `Storm Runner`) — shows genre+mood together are a strong, reliable signal when the data supports it.
- Deep Intense Rock vs. Energetic but Sad: same energy target (0.9) and similar genre (rock), but the mood flips from "intense" to "sad" — the top song stays `Storm Runner` in both cases, which exposes the mood-weight-is-too-weak bias described in section 6.
- High-Energy Pop vs. Unknown Genre: Pop has a strong genre+mood match to lean on; Unknown Genre has none, so its whole top 5 is decided by energy/valence closeness only — a preview of what every user sees once their stated preference isn't in the catalog.

I also ran a weight-shift experiment (doubled energy weight, halved genre weight): the #1 song in each profile barely changed, because strong triple-matches (genre+mood+energy) still won regardless of weights. The shift only reordered mid-pack songs that had a single, weaker match — a useful sign that weight-tuning mostly affects close calls, not clear winners.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
