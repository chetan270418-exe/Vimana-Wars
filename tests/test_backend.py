"""
tests/test_backend.py
Unit tests for the Flask Leaderboard REST API.
"""
import pytest
from backend.app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_leaderboard.db"
    monkeypatch.setattr("backend.app.DB_PATH", db_file)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_index_route(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"


def test_submit_and_get_scores(client):
    payload = {
        "player_name": "Arjuna",
        "score": 50000,
        "level_reached": 10,
        "difficulty": "hard",
        "ship_class": "garuda",
    }
    res = client.post("/scores", json=payload)
    assert res.status_code == 201
    res_data = res.get_json()
    assert res_data["success"] is True
    assert res_data["ship_class"] == "garuda"

    # Retrieve top scores
    res_top = client.get("/scores/top")
    assert res_top.status_code == 200
    top_data = res_top.get_json()
    assert top_data["count"] == 1
    assert top_data["leaderboard"][0]["player_name"] == "Arjuna"
    assert top_data["leaderboard"][0]["score"] == 50000
    assert top_data["leaderboard"][0]["ship_class"] == "garuda"


def test_stats_route(client):
    client.post("/scores", json={"player_name": "Hero", "score": 10000, "level_reached": 5, "difficulty": "normal"})
    res = client.get("/scores/stats")
    assert res.status_code == 200
    stats = res.get_json()
    assert stats["total_games_submitted"] == 1
    assert stats["highest_score"] == 10000


def test_account_lifecycle_and_authenticated_score(client):
    register = client.post("/auth/register", json={
        "email": "arjuna@example.com",
        "password": "celestial123",
        "player_name": "Arjuna",
    })
    assert register.status_code == 201
    account = register.get_json()
    assert account["success"] is True
    assert account["user"]["game_id"].startswith("VMN-")
    token = account["token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.get_json()["user"]["game_id"] == account["user"]["game_id"]

    duplicate = client.post("/auth/register", json={
        "email": "ARJUNA@example.com",
        "password": "another123",
        "player_name": "Other",
    })
    assert duplicate.status_code == 409

    bad_login = client.post("/auth/login", json={
        "email": "arjuna@example.com", "password": "wrongpass"
    })
    assert bad_login.status_code == 401

    score = client.post("/scores", headers={"Authorization": f"Bearer {token}"}, json={
        "player_name": "Spoofed Name",
        "score": 777,
        "level_reached": 4,
        "difficulty": "normal",
        "ship_class": "garuda",
    })
    assert score.status_code == 201
    assert score.get_json()["player_name"] == "Arjuna"
    assert score.get_json()["game_id"] == account["user"]["game_id"]

    top = client.get("/scores/top").get_json()["leaderboard"][0]
    assert top["game_id"] == account["user"]["game_id"]

    logout = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout.status_code == 200
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_cloud_profile_and_personal_stats(client):
    register = client.post("/auth/register", json={
        "email": "profile@example.com",
        "password": "celestial123",
        "player_name": "Profile Hero",
    }).get_json()
    headers = {"Authorization": f"Bearer {register['token']}"}

    profile = client.put("/account/profile", headers=headers, json={
        "profile": {
            "player_name": "Profile Hero",
            "achievements": ["first_blood", "high_scorer"],
            "last_wave": 12,
            "unknown_secret": "must not be stored",
        }
    })
    assert profile.status_code == 200
    assert "unknown_secret" not in profile.get_json()["profile"]

    client.post("/scores", headers=headers, json={
        "score": 1200, "level_reached": 4, "difficulty": "normal",
        "kills": 6, "total_damage": 900,
    })
    stats = client.get("/account/stats", headers=headers)
    assert stats.status_code == 200
    assert stats.get_json()["games"] == 1
    assert stats.get_json()["best_score"] == 1200
    assert stats.get_json()["total_kills"] == 6
    assert stats.get_json()["achievements_unlocked"] == 2


def test_password_reset_token_flow(client, monkeypatch):
    monkeypatch.setattr("backend.app.SHOW_DEV_AUTH_TOKENS", True)
    client.post("/auth/register", json={
        "email": "reset@example.com",
        "password": "oldpassword",
        "player_name": "Reset Hero",
    })
    request_reset = client.post("/auth/request-password-reset", json={
        "email": "reset@example.com",
    })
    assert request_reset.status_code == 200
    reset_token = request_reset.get_json()["reset_token"]

    reset = client.post("/auth/reset-password", json={
        "token": reset_token, "password": "newpassword",
    })
    assert reset.status_code == 200
    assert client.post("/auth/login", json={
        "email": "reset@example.com", "password": "oldpassword",
    }).status_code == 401
    assert client.post("/auth/login", json={
        "email": "reset@example.com", "password": "newpassword",
    }).status_code == 200
