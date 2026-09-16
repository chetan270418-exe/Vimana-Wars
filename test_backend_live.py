"""Optional live backend smoke test.

This file is deliberately opt-in.  It must never contain a real database
password and it must not connect to a hosted database during ordinary pytest
collection.  Run it explicitly with ``VIMANA_LIVE_DATABASE_URL`` when a live
PostgreSQL deployment needs checking.
"""
import os
import time


def run_live_checks(database_url: str) -> None:
    os.environ["DATABASE_URL"] = database_url
    from backend.app import app

    client = app.test_client()
    unique = str(int(time.time()))
    print("=== BACKEND LIVE SMOKE TEST ===")

    res = client.get("/")
    body = res.get_json() or {}
    print(f"[1] GET / -> {res.status_code} {body.get('status', '?')}")

    res = client.get("/scores/top")
    body = res.get_json() or {}
    print(f"[2] GET /scores/top -> {res.status_code}, count={body.get('count')}")

    res = client.post("/scores", json={
        "player_name": "ArjunaTest",
        "score": 22500,
        "level_reached": 8,
        "difficulty": "hard",
        "ship_class": "garuda",
        "kills": 88,
        "total_damage": 28000,
        "duration_seconds": 240.0,
    })
    body = res.get_json() or {}
    print(f"[3] POST /scores -> {res.status_code}, score={body.get('score')}")

    email = f"pilot_{unique}@vimana.test"
    res = client.post("/auth/register", json={
        "email": email,
        "password": "BrahmaAstra2025!",
        "player_name": f"Dharmic_{unique[:6]}",
    })
    body = res.get_json() or {}
    print(f"[4] POST /auth/register -> {res.status_code}, game_id={(body.get('user') or {}).get('game_id')}")
    token = body.get("token")
    if not token:
        print("Registration did not return a session token; stop here.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/account/profile", headers=headers)
    print(f"[5] GET /account/profile -> {res.status_code}")

    res = client.post("/scores", headers=headers, json={
        "player_name": "ShouldBeIgnored",
        "score": 55000,
        "level_reached": 10,
        "difficulty": "hard",
        "ship_class": "vajra",
        "kills": 200,
        "total_damage": 75000,
        "duration_seconds": 480.0,
    })
    body = res.get_json() or {}
    print(f"[6] POST /scores authenticated -> {res.status_code}, player={body.get('player_name')}")


if __name__ == "__main__":
    live_url = os.environ.get("VIMANA_LIVE_DATABASE_URL", "").strip()
    if not live_url:
        print("Set VIMANA_LIVE_DATABASE_URL to run the live smoke test; nothing was executed.")
    else:
        run_live_checks(live_url)
