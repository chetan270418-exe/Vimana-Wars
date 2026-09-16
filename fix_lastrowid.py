"""
Fix cursor.lastrowid (SQLite-only) so it also works with PostgreSQL (psycopg3).
Strategy: append RETURNING id to INSERT statements and read from fetchone().
"""
filepath = 'backend/app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# ── Fix 1: register() — INSERT INTO users … RETURNING id ─────────────────────
old_register = '''                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                ''', (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            user_id = cursor.lastrowid'''

new_register = '''                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                RETURNING id
                ''', (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            _row = cursor.fetchone()
            user_id = _row[0] if _row else cursor.lastrowid'''

text = text.replace(
    '''                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                \"\"\", (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            user_id = cursor.lastrowid''',
    '''                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                RETURNING id
                \"\"\", (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            _row = cursor.fetchone()
            user_id = _row[0] if _row else None''',
)

# ── Fix 2: submit_score() — INSERT INTO scores … RETURNING id ────────────────
text = text.replace(
    '''                INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class,
                                    user_id, game_id, kills, total_damage, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            \"\"\",''',
    '''                INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class,
                                    user_id, game_id, kills, total_damage, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            \"\"\",''',
)

text = text.replace(
    '''        conn.commit()
        inserted_id = cursor.lastrowid''',
    '''        conn.commit()
        _srow = cursor.fetchone()
        inserted_id = _srow[0] if _srow else None''',
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patches applied.")

# Quick verify
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
if 'cursor.lastrowid' in content:
    print("WARNING: cursor.lastrowid still present!")
else:
    print("All cursor.lastrowid references replaced.")
