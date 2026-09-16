import os
os.environ['DATABASE_URL'] = 'postgresql://postgres.wlergqltjdyzpqiucovr:CHetanamit37@aws-0-ap-southeast-2.pooler.supabase.com:6543/postgres'

from backend.app import app
import time

client = app.test_client()
unique = str(int(time.time()))

print('=== BACKEND FULL TEST SUITE ===')

# 1. Root
res = client.get('/')
j = res.get_json()
status = j.get("status", "?") if j else "NO JSON"
print(f'[1] GET / -> {res.status_code} {status}')

# 2. Scores top
res = client.get('/scores/top')
j = res.get_json() or {}
print(f'[2] GET /scores/top -> {res.status_code}, count={j.get("count")}')

# 3. Submit score (guest)
res = client.post('/scores', json={
    'player_name': 'ArjunaTest',
    'score': 22500,
    'level_reached': 8,
    'difficulty': 'hard',
    'ship_class': 'garuda',
    'kills': 88,
    'total_damage': 28000,
    'duration_seconds': 240.0
})
j = res.get_json() or {}
print(f'[3] POST /scores (guest) -> {res.status_code} id={j.get("id")} score={j.get("score")} err={j.get("error")}')

# 4. Register user
email = f'pilot_{unique}@vimana.test'
res = client.post('/auth/register', json={
    'email': email,
    'password': 'BrahmaAstra2025!',
    'player_name': f'Dharmic_{unique[:6]}'
})
j = res.get_json() or {}
user_data = j.get("user") or {}
print(f'[4] POST /auth/register -> {res.status_code} token={bool(j.get("token"))} player={user_data.get("player_name")} err={j.get("error")}')
session_token = j.get('token')

# 5. Login
res = client.post('/auth/login', json={'email': email, 'password': 'BrahmaAstra2025!'})
j = res.get_json() or {}
print(f'[5] POST /auth/login -> {res.status_code} success={j.get("success")} err={j.get("error")}')
if j.get('token'):
    session_token = j['token']

# 6. Get profile
headers = {'Authorization': f'Bearer {session_token}'} if session_token else {}
res = client.get('/account/profile', headers=headers)
j = res.get_json() or {}
profile = j.get("profile") or {}
print(f'[6] GET /account/profile -> {res.status_code} player={profile.get("player_name")} err={j.get("error")}')

# 7. Authenticated score
res = client.post('/scores', json={
    'player_name': 'ShouldBeIgnored',
    'score': 55000,
    'level_reached': 10,
    'difficulty': 'hard',
    'ship_class': 'vajra',
    'kills': 200,
    'total_damage': 75000,
    'duration_seconds': 480.0
}, headers=headers)
j = res.get_json() or {}
print(f'[7] POST /scores (auth) -> {res.status_code} id={j.get("id")} player={j.get("player_name")} err={j.get("error")}')

# 8. Leaderboard final
res = client.get('/scores/top')
j = res.get_json() or {}
lb = j.get("leaderboard", [])
top = lb[0] if lb else {}
print(f'[8] GET /scores/top -> count={j.get("count")} top={top.get("player_name")} score={top.get("score")}')

print()
print('=== DONE ===')
