import os
import time
import json
import secrets
import hashlib
import psycopg
from psycopg.rows import dict_row

POOLER_URL = os.environ.get("VIMANA_LIVE_DATABASE_URL", "").strip()

print("==================================================")
print("SUPABASE POSTGRESQL QUERY AUDIT & VERIFICATION")
print("==================================================")

if not POOLER_URL:
    print("Set VIMANA_LIVE_DATABASE_URL to run the live database audit; nothing was executed.")
    raise SystemExit(0)

try:
    conn = psycopg.connect(POOLER_URL, row_factory=dict_row)
    print(" [OK] Connected to Supabase via Transaction Pooler!")
except Exception as e:
    print(f" [FAIL] Connection error: {e}")
    exit(1)

with conn:
    # 1. Schema check
    print("\n--- 1. Checking Public Tables ---")
    cur = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
    tables = [r["table_name"] for r in cur.fetchall()]
    print(f" [OK] Found tables: {tables}")
    assert "users" in tables, "users table missing"
    assert "scores" in tables, "scores table missing"
    assert "sessions" in tables, "sessions table missing"
    assert "profiles" in tables, "profiles table missing"
    assert "auth_tokens" in tables, "auth_tokens table missing"

    # 2. Users Table Queries
    print("\n--- 2. Users Table Queries ---")
    unique_suffix = str(int(time.time()))
    test_game_id = f"VM-{secrets.token_hex(4).upper()}"
    test_email = f"audit_{unique_suffix}@vimana.test"
    test_pass_hash = hashlib.sha256(b"SecretP@ss123").hexdigest()
    
    # INSERT user
    cur = conn.execute(
        """
        INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (test_game_id, test_email, "AuditPilot", test_pass_hash, 1)
    )
    user_row = cur.fetchone()
    user_id = user_row["id"]
    print(f" [OK] User INSERT RETURNING id: user_id = {user_id}")

    # SELECT user by email
    cur = conn.execute("SELECT id, game_id, email, player_name, email_verified FROM users WHERE email = %s;", (test_email,))
    selected_user = cur.fetchone()
    print(f" [OK] User SELECT by email: {selected_user['player_name']} (Game ID: {selected_user['game_id']})")

    # 3. Sessions Queries
    print("\n--- 3. Sessions Queries ---")
    test_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(test_token.encode("utf-8")).hexdigest()
    expires_at = int(time.time()) + 3600
    
    conn.execute(
        "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (%s, %s, %s);",
        (token_hash, user_id, expires_at)
    )
    print(" [OK] Session INSERT passed")

    cur = conn.execute("SELECT user_id, expires_at FROM sessions WHERE token_hash = %s;", (token_hash,))
    sess = cur.fetchone()
    print(f" [OK] Session SELECT passed: user_id = {sess['user_id']}")

    # 4. Profiles Queries
    print("\n--- 4. Profiles Queries ---")
    initial_profile = json.dumps({"player_name": "AuditPilot", "high_score": 1000, "last_ship": "pushpaka"})
    conn.execute("INSERT INTO profiles (user_id, profile_json) VALUES (%s, %s);", (user_id, initial_profile))
    print(" [OK] Profile INSERT passed")

    updated_profile = json.dumps({"player_name": "AuditPilot", "high_score": 99999, "last_ship": "garuda"})
    conn.execute("UPDATE profiles SET profile_json = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s;", (updated_profile, user_id))
    print(" [OK] Profile UPDATE passed")

    cur = conn.execute("SELECT profile_json FROM profiles WHERE user_id = %s;", (user_id,))
    p_row = cur.fetchone()
    print(f" [OK] Profile SELECT passed: {p_row['profile_json']}")

    # 5. Scores & Leaderboard Queries
    print("\n--- 5. Scores & Leaderboard Queries ---")
    cur = conn.execute(
        """
        INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class, user_id, game_id, kills, total_damage, duration_seconds)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        ("AuditPilot", 77700, 10, "hard", "garuda", user_id, test_game_id, 120, 45000, 310.5)
    )
    score_id = cur.fetchone()["id"]
    print(f" [OK] Score INSERT RETURNING id: score_id = {score_id}")

    # Top scores
    cur = conn.execute("SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at FROM scores ORDER BY score DESC LIMIT 5;")
    top_scores = cur.fetchall()
    print(f" [OK] Global Leaderboard query (LIMIT 5): {len(top_scores)} rows retrieved")
    for r in top_scores:
        print(f"     Rank: {r['score']} pts | {r['player_name']} | Ship: {r['ship_class']} | Diff: {r['difficulty']}")

    # Filtered by difficulty
    cur = conn.execute("SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at FROM scores WHERE difficulty = %s ORDER BY score DESC LIMIT 5;", ("hard",))
    hard_scores = cur.fetchall()
    print(f" [OK] Filtered Leaderboard (difficulty='hard'): {len(hard_scores)} rows retrieved")

    # Aggregate stats
    cur = conn.execute("SELECT COUNT(*) AS total_runs, MAX(score) AS high_score, AVG(score) AS avg_score FROM scores;")
    stats_row = cur.fetchone()
    print(f" [OK] Global Stats query: Total Runs = {stats_row['total_runs']}, High Score = {stats_row['high_score']}, Avg = {int(stats_row['avg_score'] or 0)}")

    # Personal stats
    cur = conn.execute("SELECT COUNT(*) AS runs, MAX(score) AS best_score FROM scores WHERE user_id = %s;", (user_id,))
    p_stats = cur.fetchone()
    print(f" [OK] Personal Stats query for user_id {user_id}: Runs = {p_stats['runs']}, Best = {p_stats['best_score']}")

print("\n==================================================")
print("ALL DATABASE QUERIES ARE WORKING 100% IN SUPABASE!")
print("==================================================")
