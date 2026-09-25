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
    from backend import app as backend_app
    backend_app._rate_state.clear()
    backend_app._lobbies.clear()
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


def test_cloud_progression_merge_keeps_best_and_unions_unlocks(client):
    account = client.post("/auth/register", json={
        "email": "progress-merge@example.com",
        "password": "celestial123",
        "player_name": "Progress Pilot",
    }).get_json()
    headers = {"Authorization": f"Bearer {account['token']}"}

    client.put("/account/profile", headers=headers, json={"profile": {
        "high_score": 90_000,
        "last_wave": 88,
        "ships_mastered": ["pushpaka", "garuda"],
        "achievements": ["first_blood"],
    }})
    client.put("/account/profile", headers=headers, json={"profile": {
        "high_score": 500,
        "last_wave": 5,
        "ships_mastered": ["tripura"],
        "achievements": ["wave_5"],
    }})

    profile = client.get("/account/profile", headers=headers).get_json()["profile"]
    assert profile["high_score"] == 90_000
    assert profile["last_wave"] == 88
    assert set(profile["ships_mastered"]) == {"pushpaka", "garuda", "tripura"}
    assert set(profile["achievements"]) == {"first_blood", "wave_5"}


def test_cpp_achievement_ids_are_normalized_and_synced(client):
    account = client.post("/auth/register", json={
        "email": "native-achievements@example.com",
        "password": "celestial123",
        "player_name": "Native Pilot",
    }).get_json()
    headers = {"Authorization": f"Bearer {account['token']}"}

    for achievement_id in ("FIRST_BLOOD", "WAVE_5", "BOSS_1"):
        response = client.post("/achievements", headers=headers, json={
            "achievement_id": achievement_id,
        })
        assert response.status_code == 200
        assert response.get_json()["achievement_id"] == achievement_id.lower()

    gallery = client.get("/achievements", headers=headers)
    assert gallery.status_code == 200
    assert {"first_blood", "wave_5", "boss_1"}.issubset(gallery.get_json()["unlocked"])


def test_cloud_ship_mastery_never_regresses(client):
    account = client.post("/auth/register", json={
        "email": "mastery@example.com",
        "password": "celestial123",
        "player_name": "Mastery Pilot",
    }).get_json()
    headers = {"Authorization": f"Bearer {account['token']}"}

    first = client.put("/account/profile", headers=headers, json={
        "profile": {"ship_mastery": {"pushpaka": 37, "garuda": 12}},
    })
    assert first.status_code == 200
    stale = client.put("/account/profile", headers=headers, json={
        "profile": {"ship_mastery": {"pushpaka": 4, "garuda": 8, "tripura": 5}},
    })
    assert stale.status_code == 200

    profile = client.get("/account/profile", headers=headers).get_json()["profile"]
    assert profile["ship_mastery"] == {"pushpaka": 37, "garuda": 12, "tripura": 5}


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


def test_required_email_verification_flow(client, monkeypatch):
    monkeypatch.setattr("backend.app.REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr("backend.app.SHOW_DEV_AUTH_TOKENS", True)
    register = client.post("/auth/register", json={
        "email": "verify@example.com",
        "password": "celestial123",
        "player_name": "Verified Hero",
    })
    assert register.status_code == 201
    body = register.get_json()
    assert body["verification_required"] is True
    assert "token" not in body or body["token"] is None
    assert client.post("/auth/login", json={
        "email": "verify@example.com", "password": "celestial123",
    }).status_code == 403

    verified = client.post("/auth/verify-email", json={"token": body["verification_token"]})
    assert verified.status_code == 200
    assert client.post("/auth/login", json={
        "email": "verify@example.com", "password": "celestial123",
    }).status_code == 200


def test_score_sanity_validation(client):
    negative = client.post("/scores", json={
        "score": -1, "level_reached": 1,
    })
    assert negative.status_code == 422

    campaign_completion = client.post("/scores", json={
        "score": 100, "level_reached": 300, "difficulty": "normal",
    })
    assert campaign_completion.status_code == 201

    impossible_wave = client.post("/scores", json={
        "score": 100, "level_reached": 301, "difficulty": "normal",
    })
    assert impossible_wave.status_code == 422

    impossible_stats = client.post("/scores", json={
        "score": 100, "level_reached": 1, "kills": -2,
    })
    assert impossible_stats.status_code == 422


def test_multiplayer_lobby_lifecycle(client):
    first = client.post("/auth/register", json={
        "email": "host@example.com", "password": "celestial123", "player_name": "Host"
    }).get_json()
    second = client.post("/auth/register", json={
        "email": "guest@example.com", "password": "celestial123", "player_name": "Wingman"
    }).get_json()
    host_headers = {"Authorization": f"Bearer {first['token']}"}
    guest_headers = {"Authorization": f"Bearer {second['token']}"}

    created = client.post("/multiplayer/lobbies", headers=host_headers, json={
        "mode": "campaign", "max_players": 2, "ship_class": "garuda"
    })
    assert created.status_code == 201
    lobby = created.get_json()["lobby"]
    code = lobby["code"]
    assert len(lobby["players"]) == 1

    joined = client.post(f"/multiplayer/lobbies/{code}/join", headers=guest_headers, json={
        "ship_class": "vajra"
    })
    assert joined.status_code == 200
    assert len(joined.get_json()["lobby"]["players"]) == 2

    assert client.post(f"/multiplayer/lobbies/{code}/ready", headers=host_headers,
                       json={"ready": True}).status_code == 200
    assert client.post(f"/multiplayer/lobbies/{code}/ready", headers=guest_headers,
                       json={"ready": True}).status_code == 200
    started = client.post(f"/multiplayer/lobbies/{code}/start", headers=host_headers)
    assert started.status_code == 200
    assert started.get_json()["lobby"]["status"] == "running"


def test_duel_lobby_has_two_slots_and_health_rules(client):
    account = client.post("/auth/register", json={
        "email": "duelist@example.com", "password": "celestial123", "player_name": "Duelist"
    }).get_json()
    headers = {"Authorization": f"Bearer {account['token']}"}

    response = client.post("/multiplayer/lobbies", headers=headers, json={
        "mode": "duel", "max_players": 4, "ship_class": "surya"
    })
    assert response.status_code == 201
    lobby = response.get_json()["lobby"]
    assert lobby["mode"] == "duel"
    assert lobby["max_players"] == 2
    assert lobby["rules"]["health"] == 100
    assert lobby["players"][0]["health"] == 100
