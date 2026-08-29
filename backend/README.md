# Vimana Wars — Leaderboard Backend

A lightweight Flask REST API with SQLite database for global score tracking.

## Running Locally

```bash
# In your terminal
cd backend
python app.py
```
Server will start on `http://127.0.0.1:5000`.

## API Endpoints

- `GET /` — API health check and info
- `POST /scores` — Submit a score
  ```json
  {
    "player_name": "Arjuna",
    "score": 14500,
    "level_reached": 8,
    "difficulty": "hard"
  }
  ```
- `GET /scores/top?limit=10&difficulty=normal` — Fetch top 10 scores
- `GET /scores/stats` — Total scores and global high score

## Deploying for Free

You can deploy this on **Render**, **Railway**, or **PythonAnywhere** in 2 minutes:
1. Push your repository to GitHub.
2. Link the repository to Render (Web Service).
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `python backend/app.py`
5. Copy your live URL (e.g. `https://vimana-wars.onrender.com`) and update `API_BASE_URL` in `constants.py` or your settings!
