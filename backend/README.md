# Vimana Wars — Leaderboard Backend

A lightweight Flask REST API with SQLite database for global score tracking and
optional email accounts. Registered players receive a permanent `VMN-XXXXXXXX`
Game ID; guests can still submit scores without signing in.

## Running Locally

```bash
# In your terminal
cd backend
python app.py
```
Server will start on `http://127.0.0.1:5000`.

For a hosted deployment, set `DATABASE_URL` to a PostgreSQL connection string.
The backend automatically uses PostgreSQL when that variable is present and
keeps SQLite as the zero-configuration local fallback. `render.yaml` contains
the production web-service command; Render or another managed host terminates
HTTPS in front of Gunicorn.

## API Endpoints

- `GET /` — API health check and info
- `POST /auth/register` — Create an account
  ```json
  {
    "email": "arjuna@example.com",
    "password": "celestial123",
    "player_name": "Arjuna"
  }
  ```
  Returns a bearer `token` and a stable `user.game_id`.
- `POST /auth/login` — Sign in with `email` and `password`; returns a new token
- `GET /auth/me` — Read the current profile with `Authorization: Bearer <token>`
- `POST /auth/logout` — Revoke the current bearer token
- `POST /scores` — Submit a score
  ```json
  {
    "player_name": "Arjuna",
    "score": 14500,
    "level_reached": 8,
    "difficulty": "hard"
  }
  ```
  Add `Authorization: Bearer <token>` to associate the score with the account's
  Game ID. Without it, the score is recorded as a guest entry.
- `GET /scores/top?limit=10&difficulty=normal` — Fetch top 10 scores
- `GET /scores/stats` — Total scores and global high score

Passwords are stored as salted PBKDF2-SHA256 hashes and session tokens are
stored only as SHA-256 hashes. Set `REQUIRE_EMAIL_VERIFICATION=true` in a
public deployment. Email delivery is intentionally provider-neutral: connect
the verification and reset tokens to your transactional email provider before
launching publicly. Never enable `SHOW_DEV_AUTH_TOKENS` outside local testing.

## Deploying for Free

You can deploy this on **Render**, **Railway**, or **PythonAnywhere** in 2 minutes:
1. Push your repository to GitHub.
2. Link the repository to Render (Web Service).
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `python backend/app.py`
5. Copy your live URL (e.g. `https://vimana-wars.onrender.com`) and update `API_BASE_URL` in `constants.py` or your settings!
