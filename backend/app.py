"""
backend/app.py
Flask REST API for Vimana Wars Online Leaderboard.
Uses SQLite for zero-config persistence.
"""
import sqlite3
import os
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = Path(os.environ.get("DATABASE_PATH", "leaderboard.db"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                difficulty TEXT DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# Initialize database table on startup
init_db()


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "game": "Vimana Wars API",
        "status": "online",
        "endpoints": {
            "GET /scores/top": "Get top leaderboard entries (?limit=10)",
            "POST /scores": "Submit a new score {player_name, score, level_reached, difficulty}",
            "GET /scores/stats": "Global gameplay metrics",
        }
    })


@app.route("/scores", methods=["POST"])
def submit_score():
    data = request.get_json(silent=True) or {}
    player_name = str(data.get("player_name", "Anonymous")).strip()[:20] or "Anonymous"
    
    try:
        score = int(data.get("score", 0))
        level_reached = int(data.get("level_reached", 1))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid score or level format"}), 400

    difficulty = str(data.get("difficulty", "normal")).lower()
    if difficulty not in ("easy", "normal", "hard"):
        difficulty = "normal"

    if score < 0:
        return jsonify({"error": "Score cannot be negative"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO scores (player_name, score, level_reached, difficulty)
            VALUES (?, ?, ?, ?)
            """,
            (player_name, score, level_reached, difficulty)
        )
        conn.commit()
        inserted_id = cursor.lastrowid

    return jsonify({
        "success": True,
        "message": "Score recorded successfully",
        "id": inserted_id,
        "player_name": player_name,
        "score": score,
    }), 201


@app.route("/scores/top", methods=["GET"])
def get_top_scores():
    try:
        limit = min(max(1, int(request.args.get("limit", 10))), 50)
    except ValueError:
        limit = 10

    difficulty = request.args.get("difficulty")

    with get_db() as conn:
        if difficulty and difficulty in ("easy", "normal", "hard"):
            rows = conn.execute(
                """
                SELECT id, player_name, score, level_reached, difficulty, created_at
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
                SELECT id, player_name, score, level_reached, difficulty, created_at
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
            "score": row["score"],
            "level_reached": row["level_reached"],
            "difficulty": row["difficulty"],
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
        total_games = conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0]
        max_score = conn.execute("SELECT MAX(score) FROM scores").fetchone()[0] or 0
        avg_score = conn.execute("SELECT AVG(score) FROM scores").fetchone()[0] or 0

    return jsonify({
        "total_games_submitted": total_games,
        "highest_score": max_score,
        "average_score": round(avg_score, 1),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Vimana Wars Leaderboard Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
