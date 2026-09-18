"""
backend/app.py
Flask REST API for Vimana Wars Online Leaderboard.
Uses SQLite for zero-config persistence.
"""
import sqlite3
import os
import logging
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from pathlib import Path
from flask import Flask, request, jsonify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("VimanaWarsBackend")

app = Flask(__name__)
from flask_socketio import SocketIO, join_room, leave_room, emit
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

try:
    from python_game.backend.firebase_service import (
        save_user_to_firebase, save_score_to_firebase,
        save_cloud_save_to_firebase, get_firebase_status,
    )
except ImportError:
    try:
        from backend.firebase_service import (
            save_user_to_firebase, save_score_to_firebase,
            save_cloud_save_to_firebase, get_firebase_status,
        )
    except ImportError:
        from firebase_service import (
            save_user_to_firebase, save_score_to_firebase,
            save_cloud_save_to_firebase, get_firebase_status,
        )

DB_PATH = Path(os.environ.get("DATABASE_PATH", "leaderboard.db"))
if not DB_PATH.exists() and (Path(__file__).resolve().parent.parent / "leaderboard.db").exists():
    DB_PATH = Path(__file__).resolve().parent.parent / "leaderboard.db"
elif not DB_PATH.exists() and (Path(__file__).resolve().parent.parent.parent / "leaderboard.db").exists():
    DB_PATH = Path(__file__).resolve().parent.parent.parent / "leaderboard.db"
# PostgreSQL is opt-in through the environment. Never keep a database
# password in source code: local development must remain zero-config and
# production deployments must provide DATABASE_URL through their secret store.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
SESSION_TTL_SECONDS = 30 * 24 * 60 * 60
ACTION_TOKEN_TTL_SECONDS = 30 * 60
REQUIRE_EMAIL_VERIFICATION = os.environ.get("REQUIRE_EMAIL_VERIFICATION", "0").lower() in ("1", "true", "yes")
SHOW_DEV_AUTH_TOKENS = os.environ.get("SHOW_DEV_AUTH_TOKENS", "0").lower() in ("1", "true", "yes")
# Browser clients need explicit CORS origins when the React site is hosted on
# a different Render domain.  Keep this allow-list based instead of using '*'
# so bearer tokens are never exposed to arbitrary origins.
_CORS_ORIGINS = {
    origin.strip().rstrip("/")
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:4173,http://localhost:8443",
    ).split(",")
    if origin.strip()
}
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_SHIP_IDS = (
    "pushpaka", "tripura", "garuda", "vajra", "naga",
    "agneyastra", "soma", "kubera", "surya", "airavata",
    "kamadhenu", "narasimha",
)
_RATE_LIMITS = {
    "register": (5, 60),
    "login": (10, 60),
    "verify": (10, 60),
    "reset_request": (5, 60),
    "reset_password": (10, 60),
    "score": (60, 60),
}
_rate_state = defaultdict(deque)
_rate_lock = threading.Lock()
_PROFILE_KEYS = {
    "player_name", "high_score", "last_wave", "difficulty", "last_ship",
    "last_realm", "realm_unlock_seen", "total_kills", "games_played",
    "total_damage", "best_combo", "total_boons", "bosses_defeated",
    "playtime_seconds", "ships_mastered", "achievements", "endless_high_wave",
    "endless_high_score",
}

ACHIEVEMENT_CATALOG = (
    {"id": "first_blood", "name": "First Blood", "description": "Slay your first Asura.", "icon": "⚔️", "category": "combat"},
    {"id": "chakram_master", "name": "Sudarshana Mastery", "description": "Defeat 3+ enemies with one Chakram throw.", "icon": "🪓", "category": "combat"},
    {"id": "dash_phantom", "name": "Untouchable Phantom", "description": "Execute 8 Vayu Dashes in one run.", "icon": "💨", "category": "skill"},
    {"id": "combo_god", "name": "Combo Maestro", "description": "Reach an ×8 combo multiplier.", "icon": "⚡", "category": "skill"},
    {"id": "kumbhakarna_bane", "name": "Giant Slayer", "description": "Defeat Kumbhakarna on Wave 5.", "icon": "🛡️", "category": "boss"},
    {"id": "ravana_vanquisher", "name": "Slayer of Lanka", "description": "Vanquish Ravana on Wave 10.", "icon": "👑", "category": "boss"},
    {"id": "wave_5_veteran", "name": "Into the Deep", "description": "Reach Wave 5.", "icon": "🌊", "category": "campaign"},
    {"id": "wave_10_breaker", "name": "Break Lanka's Gate", "description": "Reach Wave 10.", "icon": "🚪", "category": "campaign"},
    {"id": "mahishasura_bane", "name": "Warlord Breaker", "description": "Defeat Mahishasura.", "icon": "🐂", "category": "boss"},
    {"id": "wave_15_conqueror", "name": "Forge Walker", "description": "Reach Wave 15.", "icon": "🔥", "category": "campaign"},
    {"id": "vritra_vanquisher", "name": "Storm Breaker", "description": "Defeat Vritra.", "icon": "⚡", "category": "boss"},
    {"id": "boss_collector", "name": "Four Thrones Fall", "description": "Defeat all four campaign bosses.", "icon": "👑", "category": "boss"},
    {"id": "campaign_conqueror", "name": "Conqueror of the Mahayuddha", "description": "Clear all 20 campaign waves.", "icon": "🏅", "category": "campaign"},
    {"id": "hardcore_hero", "name": "Immortal Warrior", "description": "Complete the campaign on Hard.", "icon": "🔥", "category": "skill"},
    {"id": "bomb_annihilator", "name": "Brahmastra Unleashed", "description": "Vaporize 8+ enemies with one Brahmastra.", "icon": "💥", "category": "combat"},
    {"id": "boon_collector", "name": "Blessed by the Devas", "description": "Attain 4 Divine Astral Boons in one run.", "icon": "✨", "category": "collection"},
    {"id": "high_scorer", "name": "Legend of the Realm", "description": "Score more than 25,000 points.", "icon": "🏆", "category": "score"},
    {"id": "cube_collector", "name": "Astral Arsenal", "description": "Collect 10 ability cubes in one run.", "icon": "🔷", "category": "collection"},
    {"id": "overdrive_online", "name": "Overdrive Online", "description": "Collect an Astra Overdrive cube.", "icon": "💗", "category": "collection"},
)
_ACHIEVEMENT_IDS = {item["id"] for item in ACHIEVEMENT_CATALOG}


def get_db():
    if DATABASE_URL:
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError("psycopg is required when DATABASE_URL is configured") from exc
        connection = psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=10)
        return _PostgresConnection(connection)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=30)
    connection.row_factory = sqlite3.Row
    return connection


class _PostgresConnection:
    """Tiny compatibility wrapper for the existing parameterized queries."""
    is_postgres = True

    def __init__(self, connection):
        self._connection = connection

    def execute(self, statement, params=()):
        return self._connection.execute(statement.replace("?", "%s"), params)

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self._connection.close()


def _is_postgres() -> bool:
    return bool(DATABASE_URL)


def _is_integrity_error(exc: Exception) -> bool:
    return isinstance(exc, sqlite3.IntegrityError) or (
        _is_postgres() and getattr(exc, "sqlstate", None) == "23505"
    )


def init_db():
    with get_db() as conn:
        id_definition = (
            "INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY"
            if _is_postgres() else "INTEGER PRIMARY KEY AUTOINCREMENT"
        )
        email_definition = "email TEXT NOT NULL UNIQUE" if _is_postgres() else "email TEXT NOT NULL UNIQUE COLLATE NOCASE"
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id %s,
                game_id TEXT NOT NULL UNIQUE,
                %s,
                player_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                email_verified INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ % (id_definition, email_definition))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS auth_tokens (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                purpose TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                consumed_at INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                profile_json TEXT NOT NULL DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id %s,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                difficulty TEXT DEFAULT 'normal',
                ship_class TEXT DEFAULT 'pushpaka',
                user_id INTEGER,
                game_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ % id_definition)
        # Safe migrations for databases created by earlier versions.
        migration_columns = (
            "ALTER TABLE users ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN ship_class TEXT DEFAULT 'pushpaka'",
            "ALTER TABLE scores ADD COLUMN user_id INTEGER",
            "ALTER TABLE scores ADD COLUMN game_id TEXT",
            "ALTER TABLE scores ADD COLUMN kills INTEGER DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN total_damage INTEGER DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN duration_seconds REAL DEFAULT 0",
        )
        statements = tuple(
            statement.replace("ADD COLUMN ", "ADD COLUMN IF NOT EXISTS ")
            for statement in migration_columns
        ) if _is_postgres() else migration_columns
        for statement in statements:
            try:
                conn.execute(statement)
            except Exception as exc:
                # SQLite and PostgreSQL both report duplicate columns here;
                # preserve real connection/schema errors.
                duplicate_column = (
                    isinstance(exc, sqlite3.OperationalError)
                    or (_is_postgres() and getattr(exc, "sqlstate", None) == "42701")
                )
                if not duplicate_column:
                    raise
        conn.commit()


# Initialize database table on startup
init_db()


@app.after_request
def add_cors_headers(response):
    """Allow the separately hosted React frontend to call this API."""
    origin = request.headers.get("Origin", "").rstrip("/")
    if origin in _CORS_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "600"
        response.headers.add("Vary", "Origin")
    return response


@app.route("/<path:_path>", methods=["OPTIONS"])
def cors_preflight(_path):
    return ("", 204)


@app.route("/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS":
        return ("", 204)
    logger.info("API Root status checked from %s", request.remote_addr)
    return jsonify({
        "game": "Vimana Wars API",
        "status": "online",
        "firebase_gsa": get_firebase_status(),
        "endpoints": {
            "GET /health": "Server health and database/GSA status",
            "GET /scores/top": "Get top leaderboard entries (?limit=10&difficulty=normal)",
            "POST /scores": "Submit a score (Bearer token optional for guest submissions)",
            "POST /auth/register": "Create an email account and receive a stable Game ID",
            "POST /auth/login": "Sign in with email and password",
            "POST /auth/verify-email": "Verify an email address with its one-time token",
            "POST /auth/request-password-reset": "Request a password reset token",
            "POST /auth/reset-password": "Set a new password with a reset token",
            "GET /auth/me": "Get the signed-in player profile",
            "GET /account/profile": "Get cloud-synced progression and achievements",
            "PUT /account/profile": "Sync cloud-saved progression and achievements",
            "GET /account/stats": "Get personal online gameplay statistics",
            "GET /achievements": "Get the achievement catalog and unlocked trophies",
            "POST /achievements": "Award an achievement to the signed-in profile",
            "GET /multiplayer/lobbies": "Browse active multiplayer lobbies",
            "POST /multiplayer/lobbies": "Create a multiplayer lobby",
            "GET /scores/stats": "Global gameplay metrics",
        }
    })


@app.route("/health", methods=["GET"])
def health():
    database = "postgresql" if DATABASE_URL else "sqlite"
    try:
        with get_db() as conn:
            conn.execute("SELECT 1").fetchone()
    except Exception as exc:
        logger.exception("Database health check failed")
        return jsonify({
            "status": "degraded",
            "service": "Vimana Wars Backend",
            "database": database,
            "database_error": str(exc)[:240],
            "firebase_gsa": get_firebase_status(),
            "timestamp": time.time(),
        }), 503
    return jsonify({
        "status": "healthy",
        "service": "Vimana Wars Backend",
        "database": database,
        "firebase_gsa": get_firebase_status(),
        "timestamp": time.time(),
    })


def _rate_limit(action: str):
    """Small process-local guard; production deployments should use Redis."""
    limit, window = _RATE_LIMITS[action]
    now = time.monotonic()
    key = (action, request.remote_addr or "unknown")
    with _rate_lock:
        calls = _rate_state[key]
        while calls and now - calls[0] >= window:
            calls.popleft()
        if len(calls) >= limit:
            retry_after = max(1, int(window - (now - calls[0])))
            return jsonify({"error": "Too many requests. Please try again shortly."}), 429, {
                "Retry-After": str(retry_after)
            }
        calls.append(now)
    return None


def _new_action_token(conn, user_id: int, purpose: str) -> str:
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO auth_tokens (token_hash, user_id, purpose, expires_at) VALUES (?, ?, ?, ?)",
        (hashlib.sha256(token.encode("utf-8")).hexdigest(), user_id, purpose,
         int(time.time()) + ACTION_TOKEN_TTL_SECONDS),
    )
    return token


def _default_profile() -> dict:
    return {
        "player_name": "Warrior", "high_score": 0, "last_wave": 0,
        "difficulty": "normal", "last_ship": "pushpaka", "last_realm": 1,
        "realm_unlock_seen": [], "total_kills": 0, "games_played": 0,
        "total_damage": 0, "best_combo": 1, "total_boons": 0,
        "bosses_defeated": [], "playtime_seconds": 0, "ships_mastered": [],
        "achievements": [], "endless_high_wave": 0, "endless_high_score": 0,
    }


def _profile_from_payload(value) -> dict:
    if not isinstance(value, dict):
        return {}
    profile = {}
    for key in _PROFILE_KEYS:
        if key in value:
            profile[key] = value[key]
    # Prevent a malformed client from creating unbounded profile data.
    encoded = json.dumps(profile, separators=(",", ":"))
    return profile if len(encoded) <= 100_000 else {}


# Multiplayer lobby state is intentionally ephemeral. It is suitable for a
# first lobby/matchmaking layer; live combat state belongs in a WebSocket or
# dedicated game server and should not be stored in this request database.
_lobbies = {}
_lobbies_lock = threading.Lock()


def _new_lobby_code() -> str:
    with _lobbies_lock:
        while True:
            code = secrets.token_hex(3).upper()
            if code not in _lobbies:
                return code


def _lobby_payload(lobby: dict) -> dict:
    return {
        "code": lobby["code"],
        "mode": lobby["mode"],
        "max_players": lobby["max_players"],
        "status": lobby["status"],
        "host_game_id": lobby["host_game_id"],
        "players": list(lobby["players"].values()),
        "created_at": lobby["created_at"],
        "rules": lobby.get("rules", {"health": 100, "win_condition": "first pilot to reduce the opponent to 0 HP"}),
    }


def _password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 210_000)
    return f"pbkdf2_sha256$210000${salt.hex()}${digest.hex()}"


def _password_matches(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        expected = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(rounds)
        ).hex()
        return hmac.compare_digest(expected, digest_hex)
    except (TypeError, ValueError):
        return False


def _new_game_id(conn) -> str:
    while True:
        game_id = f"VMN-{secrets.token_hex(4).upper()}"
        if conn.execute("SELECT 1 FROM users WHERE game_id = ?", (game_id,)).fetchone() is None:
            return game_id


def _user_payload(row) -> dict:
    return {
        "game_id": row["game_id"],
        "email": row["email"],
        "player_name": row["player_name"],
        "email_verified": bool(row["email_verified"]) if "email_verified" in row.keys() else False,
    }


def _current_user():
    """Resolve an opaque bearer token without exposing password data."""
    header = request.headers.get("Authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    token = header[7:].strip()
    if not token:
        return None
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id, u.email, u.player_name, u.email_verified
            FROM sessions s JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """, (token_hash, now)
        ).fetchone()
    return row


@app.route("/auth/register", methods=["POST"])
def register():
    limited = _rate_limit("register")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    player_name = str(data.get("player_name", "Warrior")).strip()[:20] or "Warrior"
    if not _EMAIL_RE.match(email) or len(email) > 254:
        return jsonify({"error": "Enter a valid email address"}), 400
    if len(password) < 8 or len(password) > 128:
        return jsonify({"error": "Password must be 8 to 128 characters"}), 400

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with get_db() as conn:
        try:
            game_id = _new_game_id(conn)
            _reg_sql = """
                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                """
            if _is_postgres():
                _reg_sql += " RETURNING id"
            cursor = conn.execute(
                _reg_sql, (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            if _is_postgres():
                _urow = cursor.fetchone()
                user_id = (_urow[0] if isinstance(_urow, (tuple, list)) else _urow["id"]) if _urow else None
            else:
                user_id = cursor.lastrowid
            verification_token = _new_action_token(conn, user_id, "verify_email")
            conn.execute(
                "INSERT INTO profiles (user_id, profile_json) VALUES (?, ?)",
                (user_id, json.dumps(_default_profile(), separators=(",", ":"))),
            )
            session_token = None
            if not REQUIRE_EMAIL_VERIFICATION:
                session_token = token
            else:
                # A new account must verify its email before a session is issued.
                token = None
            if session_token:
                conn.execute(
                    "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
                    (token_hash, user_id, int(time.time()) + SESSION_TTL_SECONDS)
                )
            row = conn.execute(
                "SELECT game_id, email, player_name, email_verified FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            conn.commit()
            if row:
                save_user_to_firebase({
                    "game_id": row["game_id"],
                    "email": row["email"],
                    "player_name": row["player_name"],
                    "email_verified": bool(row["email_verified"]),
                })
        except Exception as exc:
            if not _is_integrity_error(exc):
                raise
            if _is_postgres():
                conn.rollback()
            return jsonify({"error": "An account with that email already exists"}), 409
    response = {
        "success": True,
        "token": token,
        "verification_required": REQUIRE_EMAIL_VERIFICATION,
        "user": _user_payload(row),
    }
    if REQUIRE_EMAIL_VERIFICATION and SHOW_DEV_AUTH_TOKENS:
        response["verification_token"] = verification_token
    return jsonify(response), 201


@app.route("/auth/login", methods=["POST"])
def login():
    limited = _rate_limit("login")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, game_id, email, player_name, password_hash, email_verified FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        if row is None or not _password_matches(password, row["password_hash"]):
            return jsonify({"error": "Email or password is incorrect"}), 401
        if REQUIRE_EMAIL_VERIFICATION and not row["email_verified"]:
            return jsonify({
                "error": "Please verify your email before signing in",
                "verification_required": True,
            }), 403
        token = secrets.token_urlsafe(32)
        conn.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (hashlib.sha256(token.encode("utf-8")).hexdigest(), row["id"], int(time.time()) + SESSION_TTL_SECONDS)
        )
        conn.commit()
    return jsonify({"success": True, "token": token, "user": _user_payload(row)}), 200


@app.route("/auth/me", methods=["GET"])
def me():
    user = _current_user()
    if user is None:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify({"user": _user_payload(user)})


@app.route("/auth/verify-email", methods=["POST"])
def verify_email():
    limited = _rate_limit("verify")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    raw_token = str(data.get("token", "")).strip()
    if not raw_token:
        return jsonify({"error": "Verification token is required"}), 400
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id, u.email, u.player_name, u.email_verified
            FROM auth_tokens t JOIN users u ON u.id = t.user_id
            WHERE t.token_hash = ? AND t.purpose = 'verify_email'
              AND t.consumed_at IS NULL AND t.expires_at > ?
            """, (token_hash, now)
        ).fetchone()
        if row is None:
            return jsonify({"error": "Verification token is invalid or expired"}), 400
        conn.execute("UPDATE users SET email_verified = 1 WHERE id = ?", (row["id"],))
        conn.execute("UPDATE auth_tokens SET consumed_at = ? WHERE token_hash = ?", (now, token_hash))
        session_token = secrets.token_urlsafe(32)
        conn.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (hashlib.sha256(session_token.encode("utf-8")).hexdigest(), row["id"], now + SESSION_TTL_SECONDS),
        )
        conn.commit()
    return jsonify({"success": True, "token": session_token,
                    "user": {**_user_payload(row), "email_verified": True}})


@app.route("/auth/request-password-reset", methods=["POST"])
def request_password_reset():
    limited = _rate_limit("reset_request")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    response = {"success": True, "message": "If that email exists, reset instructions have been created."}
    with get_db() as conn:
        row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if row is not None:
            reset_token = _new_action_token(conn, row["id"], "reset_password")
            conn.commit()
            if SHOW_DEV_AUTH_TOKENS:
                response["reset_token"] = reset_token
    return jsonify(response)


@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    limited = _rate_limit("reset_password")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    raw_token = str(data.get("token", "")).strip()
    password = str(data.get("password", ""))
    if len(password) < 8 or len(password) > 128:
        return jsonify({"error": "Password must be 8 to 128 characters"}), 400
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT user_id FROM auth_tokens
            WHERE token_hash = ? AND purpose = 'reset_password'
              AND consumed_at IS NULL AND expires_at > ?
            """, (token_hash, now)
        ).fetchone()
        if row is None:
            return jsonify({"error": "Reset token is invalid or expired"}), 400
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (_password_hash(password), row["user_id"]))
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (row["user_id"],))
        conn.execute("UPDATE auth_tokens SET consumed_at = ? WHERE token_hash = ?", (now, token_hash))
        conn.commit()
    return jsonify({"success": True, "message": "Password updated. Please sign in again."})


@app.route("/auth/logout", methods=["POST"])
def logout():
    header = request.headers.get("Authorization", "")
    token = header[7:].strip() if header.lower().startswith("bearer ") else ""
    if token:
        with get_db() as conn:
            conn.execute(
                "DELETE FROM sessions WHERE token_hash = ?",
                (hashlib.sha256(token.encode("utf-8")).hexdigest(),)
            )
            conn.commit()
    return jsonify({"success": True})


def _require_user():
    user = _current_user()
    if user is None:
        return None, (jsonify({"error": "Authentication required"}), 401)
    return user, None


def _lobby_player(user, ship_class="pushpaka", ready=False, host=False):
    return {
        "game_id": user["game_id"],
        "player_name": user["player_name"],
        "ship_class": ship_class if ship_class in _SHIP_IDS else "pushpaka",
        "ready": bool(ready),
        "host": bool(host),
        # These are match rules/initial values for the future authoritative
        # duel server. HTTP lobby state is not trusted for combat results.
        "health": 100,
        "max_health": 100,
    }


def _cleanup_lobbies() -> None:
    cutoff = time.time() - 30 * 60
    expired = [code for code, lobby in _lobbies.items() if lobby["created_at"] < cutoff]
    for code in expired:
        _lobbies.pop(code, None)


@app.route("/multiplayer/lobbies", methods=["GET", "POST"])
def multiplayer_lobbies():
    if request.method == "GET":
        with _lobbies_lock:
            _cleanup_lobbies()
            return jsonify({"lobbies": [_lobby_payload(lobby) for lobby in _lobbies.values()]})

    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    mode = str(data.get("mode", "campaign")).lower()
    if mode not in ("campaign", "endless", "duel"):
        mode = "campaign"
    try:
        max_players = min(4, max(2, int(data.get("max_players", 2))))
    except (TypeError, ValueError):
        max_players = 2
    if mode == "duel":
        max_players = 2
    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    code = _new_lobby_code()
    host = _lobby_player(user, ship_class, ready=False, host=True)
    lobby = {
        "code": code, "mode": mode, "max_players": max_players,
        "status": "waiting", "host_game_id": user["game_id"],
        "players": {user["game_id"]: host}, "created_at": time.time(),
        "rules": {
            "health": 100,
            "win_condition": "first pilot to reduce the opponent to 0 HP",
        } if mode == "duel" else {
            "health": 100,
            "win_condition": "complete the selected wave set",
        },
    }
    with _lobbies_lock:
        _lobbies[code] = lobby
    return jsonify({"lobby": _lobby_payload(lobby)}), 201


@app.route("/multiplayer/lobbies/<code>", methods=["GET"])
def get_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if user["game_id"] not in lobby["players"]:
            return jsonify({"error": "Join this lobby to view its private status"}), 403
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/join", methods=["POST"])
def join_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if lobby["status"] != "waiting":
            return jsonify({"error": "Lobby has already started"}), 409
        if user["game_id"] not in lobby["players"] and len(lobby["players"]) >= lobby["max_players"]:
            return jsonify({"error": "Lobby is full"}), 409
        lobby["players"][user["game_id"]] = _lobby_player(user, ship_class)
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/ready", methods=["POST"])
def ready_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None or user["game_id"] not in lobby["players"]:
            return jsonify({"error": "You are not in this lobby"}), 404
        player = lobby["players"][user["game_id"]]
        player["ready"] = bool(data.get("ready", not player["ready"]))
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/start", methods=["POST"])
def start_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if lobby["host_game_id"] != user["game_id"]:
            return jsonify({"error": "Only the lobby host can start the match"}), 403
        if len(lobby["players"]) < 2:
            return jsonify({"error": "At least two players are required"}), 409
        if not all(player["ready"] for player in lobby["players"].values()):
            return jsonify({"error": "Every player must be ready"}), 409
        lobby["status"] = "running"
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/leave", methods=["POST"])
def leave_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"success": True})
        lobby["players"].pop(user["game_id"], None)
        if not lobby["players"]:
            _lobbies.pop(code.upper(), None)
        elif lobby["host_game_id"] == user["game_id"]:
            new_host_id = next(iter(lobby["players"]))
            lobby["host_game_id"] = new_host_id
            for game_id, player in lobby["players"].items():
                player["host"] = game_id == new_host_id
        return jsonify({"success": True, "lobby": _lobby_payload(lobby) if lobby["players"] else None})


@app.route("/account/profile", methods=["GET"])
def get_profile():
    user, error = _require_user()
    if error:
        return error
    with get_db() as conn:
        row = conn.execute("SELECT profile_json, updated_at FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    try:
        profile = json.loads(row["profile_json"]) if row else _default_profile()
    except (TypeError, ValueError):
        profile = _default_profile()
    return jsonify({"profile": profile, "updated_at": row["updated_at"] if row else None})


@app.route("/account/profile", methods=["PUT"])
def update_profile():
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    incoming = _profile_from_payload(data.get("profile", data))
    if not incoming:
        return jsonify({"error": "A valid profile object is required"}), 400
    with get_db() as conn:
        row = conn.execute("SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
        try:
            current = json.loads(row["profile_json"]) if row else _default_profile()
        except (TypeError, ValueError):
            current = _default_profile()
        current.update(incoming)
        if "player_name" in current:
            current["player_name"] = str(current["player_name"]).strip()[:20] or "Warrior"
        encoded = json.dumps(current, separators=(",", ":"))
        if len(encoded) > 100_000:
            return jsonify({"error": "Profile is too large"}), 413
        conn.execute(
            """
            INSERT INTO profiles (user_id, profile_json, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET profile_json = excluded.profile_json,
                                               updated_at = CURRENT_TIMESTAMP
            """, (user["id"], encoded)
        )
        if current.get("player_name"):
            conn.execute("UPDATE users SET player_name = ? WHERE id = ?", (current["player_name"], user["id"]))
        conn.commit()
    return jsonify({"success": True, "profile": current})


@app.route("/achievements", methods=["GET", "POST"])
def award_achievement():
    if request.method == "GET":
        user, _ = _require_user()
        unlocked = set()
        if user:
            with get_db() as conn:
                row = conn.execute(
                    "SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)
                ).fetchone()
            try:
                unlocked = {
                    item for item in json.loads(row["profile_json"]).get("achievements", [])
                    if item in _ACHIEVEMENT_IDS
                } if row else set()
            except (TypeError, ValueError, AttributeError):
                unlocked = set()
        return jsonify({
            "achievements": [
                {**item, "unlocked": item["id"] in unlocked}
                for item in ACHIEVEMENT_CATALOG
            ],
            "unlocked": sorted(unlocked),
            "authenticated": bool(user),
        })

    user, error = _require_user()
    if error:
        return jsonify({"success": False, "message": "Guest mode - achievement saved locally"}), 200
    data = request.get_json(silent=True) or {}
    achievement_id = str(data.get("achievement_id", "")).strip()
    if not achievement_id:
        return jsonify({"error": "achievement_id required"}), 400
    if achievement_id not in _ACHIEVEMENT_IDS:
        return jsonify({"error": "Unknown achievement"}), 422
    with get_db() as conn:
        row = conn.execute("SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
        try:
            current = json.loads(row["profile_json"]) if row else _default_profile()
        except (TypeError, ValueError):
            current = _default_profile()
        if "achievements" not in current or not isinstance(current["achievements"], list):
            current["achievements"] = []
        if achievement_id not in current["achievements"]:
            current["achievements"].append(achievement_id)
            encoded = json.dumps(current, separators=(",", ":"))
            conn.execute(
                """
                INSERT INTO profiles (user_id, profile_json, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET profile_json = excluded.profile_json,
                                                   updated_at = CURRENT_TIMESTAMP
                """, (user["id"], encoded)
            )
            conn.commit()
    return jsonify({"success": True, "achievement_id": achievement_id, "awarded": True})


@app.route("/account/stats", methods=["GET"])
def get_account_stats():
    user, error = _require_user()
    if error:
        return error
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS games, COALESCE(MAX(score), 0) AS best_score,
                   COALESCE(SUM(score), 0) AS total_score,
                   COALESCE(MAX(level_reached), 0) AS best_wave,
                   COALESCE(SUM(kills), 0) AS total_kills,
                   COALESCE(SUM(total_damage), 0) AS total_damage
            FROM scores WHERE user_id = ?
            """, (user["id"],)
        ).fetchone()
        achievements = conn.execute(
            "SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)
        ).fetchone()
    unlocked = 0
    if achievements:
        try:
            unlocked = len(json.loads(achievements["profile_json"]).get("achievements", []))
        except (TypeError, ValueError):
            unlocked = 0
    return jsonify({
        "game_id": user["game_id"], "games": row["games"],
        "best_score": row["best_score"], "total_score": row["total_score"],
        "best_wave": row["best_wave"], "total_kills": row["total_kills"],
        "total_damage": row["total_damage"], "achievements_unlocked": unlocked,
    })


@app.route("/scores", methods=["POST"])
def submit_score():
    limited = _rate_limit("score")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    user = _current_user()
    player_name = str(data.get("player_name", "Anonymous")).strip()[:20] or "Anonymous"
    
    try:
        score = int(data.get("score", 0))
        level_reached = int(data.get("level_reached", 1))
        kills = int(data.get("kills", 0))
        total_damage = int(data.get("total_damage", 0))
        duration_seconds = float(data.get("duration_seconds", 0))
    except (ValueError, TypeError):
        logger.warning("Invalid score/level submission from %s: %s", request.remote_addr, data)
        return jsonify({"error": "Invalid score or level format"}), 400

    difficulty = str(data.get("difficulty", "normal")).lower()
    if difficulty not in ("easy", "normal", "hard", "endless"):
        difficulty = "normal"

    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    if ship_class not in _SHIP_IDS:
        ship_class = "pushpaka"

    # These are deliberately generous sanity limits. They stop accidental or
    # obviously forged payloads while leaving room for future balance changes.
    max_wave = 10000 if difficulty == "endless" else 20
    max_score = max(250_000, level_reached * 250_000)
    if level_reached < 1 or level_reached > max_wave:
        return jsonify({"error": "Invalid wave value"}), 422
    if score < 0 or score > max_score or kills < 0 or kills > level_reached * 1000:
        logger.warning("Negative score rejected from %s: %s", request.remote_addr, score)
        return jsonify({"error": "Score failed sanity validation"}), 422
    if total_damage < 0 or duration_seconds < 0 or duration_seconds > 24 * 60 * 60:
        return jsonify({"error": "Run statistics failed sanity validation"}), 422

    with get_db() as conn:
        _insert_sql = """
                INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class,
                                    user_id, game_id, kills, total_damage, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        if _is_postgres():
            _insert_sql += " RETURNING id"
        cursor = conn.execute(
            _insert_sql,
            (
                user["player_name"] if user else player_name,
                score, level_reached, difficulty, ship_class,
                user["id"] if user else None,
                user["game_id"] if user else None,
                kills, total_damage, duration_seconds,
            )
        )
        # Fetch RETURNING row BEFORE commit (commit closes the cursor on SQLite)
        if _is_postgres():
            _srow = cursor.fetchone()
            inserted_id = (_srow[0] if isinstance(_srow, (tuple, list)) else _srow["id"]) if _srow else None
        else:
            inserted_id = cursor.lastrowid
        conn.commit()
        save_score_to_firebase({
            "player_name": user["player_name"] if user else player_name,
            "game_id": user["game_id"] if user else "",
            "score": score,
            "level_reached": level_reached,
            "difficulty": difficulty,
            "ship_class": ship_class,
            "kills": kills,
        })

    stored_name = user["player_name"] if user else player_name
    logger.info(
        "🏆 Score Recorded [ID=%s]: Warrior='%s' | Ship='%s' | Score=%s | Wave=%s | Diff='%s'",
        inserted_id, stored_name, ship_class.upper(), score, level_reached, difficulty.upper()
    )

    return jsonify({
        "success": True,
        "message": "Score recorded successfully",
        "id": inserted_id,
        "player_name": stored_name,
        "game_id": user["game_id"] if user else None,
        "ship_class": ship_class,
        "score": score,
        "level_reached": level_reached,
        "difficulty": difficulty,
        "kills": kills,
        "total_damage": total_damage,
        "duration_seconds": duration_seconds,
    }), 201


@app.route("/scores/top", methods=["GET"])
def get_top_scores():
    try:
        limit = min(max(1, int(request.args.get("limit", 10))), 50)
    except ValueError:
        limit = 10

    difficulty = request.args.get("difficulty")
    logger.info("Fetching leaderboard: limit=%s, difficulty=%s", limit, difficulty)

    with get_db() as conn:
        if difficulty and difficulty in ("easy", "normal", "hard", "endless"):
            rows = conn.execute(
                """
                SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at
                FROM scores
                WHERE difficulty = ?
                ORDER BY score DESC, created_at ASC
                LIMIT ?
                """,
                (difficulty, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at
                FROM scores
                ORDER BY score DESC, created_at ASC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

    leaderboard = [
        {
            "rank": i + 1,
            "player_name": row["player_name"],
            "game_id": row["game_id"],
            "score": row["score"],
            "level_reached": row["level_reached"],
            "difficulty": row["difficulty"],
            "ship_class": row["ship_class"] or "pushpaka",
            "created_at": row["created_at"],
        }
        for i, row in enumerate(rows)
    ]

    return jsonify({
        "count": len(leaderboard),
        "leaderboard": leaderboard
    })


@app.route("/scores/stats", methods=["GET"])
def get_stats():
    with get_db() as conn:
        def _scalar(cur):
            r = cur.fetchone()
            if not r:
                return 0
            if isinstance(r, (tuple, list)):
                return r[0]
            if isinstance(r, dict):
                return next(iter(r.values()))
            try:
                return r[0]
            except Exception:
                return 0

        total_games = _scalar(conn.execute("SELECT COUNT(*) FROM scores")) or 0
        total_players = _scalar(conn.execute("SELECT COUNT(*) FROM users")) or 0
        max_score = _scalar(conn.execute("SELECT MAX(score) FROM scores")) or 0
        avg_score = _scalar(conn.execute("SELECT AVG(score) FROM scores")) or 0

    logger.info("Global stats queried: total_games=%s, max_score=%s", total_games, max_score)
    return jsonify({
        "total_games_submitted": total_games,
        "highest_score": max_score,
        "average_score": round(float(avg_score), 1),
        "registered_players": total_players,
    })

_duel_state = {}
_sid_to_player = {}

@socketio.on("join_duel")
def handle_join_duel(data):
    token = data.get("token")
    room_code = data.get("room_code")
    game_id = data.get("game_id")
    ship_class = data.get("ship_class", "pushpaka")

    if not token or not room_code or not game_id:
        emit("error", {"message": "Invalid join data"})
        return

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id
            FROM sessions s JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """, (token_hash, now)
        ).fetchone()

    if not row or row["game_id"] != game_id:
        emit("error", {"message": "Unauthorized"})
        return

    join_room(room_code)
    _sid_to_player[request.sid] = {"room_code": room_code, "game_id": game_id}

    if room_code not in _duel_state:
        _duel_state[room_code] = {}

    _duel_state[room_code][game_id] = {
        "game_id": game_id,
        "hp": 100,
        "max_hp": 100
    }

    emit("player_joined", {"game_id": game_id, "ship_class": ship_class}, to=room_code)


@socketio.on("player_input")
def handle_player_input(data):
    player = _sid_to_player.get(request.sid)
    if not player:
        return
    emit("opponent_state", data, to=player["room_code"], include_self=False)


@socketio.on("hit_registered")
def handle_hit_registered(data):
    player = _sid_to_player.get(request.sid)
    if not player:
        return

    room_code = player["room_code"]
    target_id = data.get("target_game_id")
    damage = min(50, max(0, int(data.get("damage", 0))))

    room_state = _duel_state.get(room_code)
    if not room_state or target_id not in room_state:
        return

    target = room_state[target_id]
    target["hp"] = max(0, target["hp"] - damage)

    players_list = [{"game_id": k, "hp": v["hp"], "max_hp": v["max_hp"]} for k, v in room_state.items()]
    emit("hp_update", {"players": players_list}, to=room_code)

    if target["hp"] == 0:
        emit("duel_end", {"winner_game_id": player["game_id"]}, to=room_code)


@socketio.on("disconnect")
def handle_disconnect():
    player = _sid_to_player.pop(request.sid, None)
    if player:
        room_code = player["room_code"]
        game_id = player["game_id"]
        emit("player_left", {"game_id": game_id}, to=room_code)
        
        room_state = _duel_state.get(room_code)
        if room_state and game_id in room_state:
            del room_state[game_id]
            if not room_state:
                del _duel_state[room_code]


@socketio.on("duel_ping")
def handle_duel_ping(data):
    emit("duel_pong", data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Vimana Wars Leaderboard Server on port {port}...")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
