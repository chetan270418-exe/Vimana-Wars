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
- `POST /auth/verify-email` — Consume a one-time verification token
- `POST /auth/request-password-reset` — Start a reset flow without revealing whether an email exists
- `POST /auth/reset-password` — Consume a reset token and revoke old sessions
- `GET /account/profile` — Read cloud-synced progression and achievements
- `PUT /account/profile` — Sync whitelisted local progression and achievements
- `GET /account/stats` — Read server-calculated personal run statistics
- `GET /multiplayer/lobbies` — Browse active lobbies
- `POST /multiplayer/lobbies` — Create a campaign or endless lobby
- `GET /multiplayer/lobbies/<code>` — Read a lobby you joined
- `POST /multiplayer/lobbies/<code>/join` — Join a lobby with a ship class
- `POST /multiplayer/lobbies/<code>/ready` — Toggle player ready state
- `POST /multiplayer/lobbies/<code>/start` — Host starts when all players are ready
- `POST /multiplayer/lobbies/<code>/leave` — Leave and transfer host if needed
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

Authentication and score endpoints have process-local rate limits and generous
score/wave/statistics sanity checks. For multiple production instances, move
rate-limit state to Redis and add server-issued run attestations or replay
validation; a client-only game can never make score submissions fully
trustworthy by itself.

The multiplayer routes currently provide an authenticated, ephemeral lobby
layer. Lobby memory is intentionally lost if the API restarts. Live player
movement, enemy simulation, hit detection, and combat reconciliation still
belong in a real-time authoritative game server (WebSocket/UDP), not in these
HTTP lobby requests.

## Deploying for Free

You can deploy this on **Render**, **Railway**, or **PythonAnywhere** in 2 minutes:
1. Push your repository to GitHub.
2. Link the repository to Render (Web Service).
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `python backend/app.py`
5. Copy your live URL (e.g. `https://vimana-wars.onrender.com`) and launch the
   game with `VIMANA_API_URL=https://vimana-wars.onrender.com` set in its
   environment. This avoids changing source code between local and hosted builds.
