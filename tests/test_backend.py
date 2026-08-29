"""
tests/test_backend.py
Unit tests for the Flask Leaderboard REST API.
"""
import pytest
import tempfile
import os
from pathlib import Path
from backend.app import app, init_db, get_db


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
    }
    res = client.post("/scores", json=payload)
    assert res.status_code == 201
    res_data = res.get_json()
    assert res_data["success"] is True

    # Retrieve top scores
    res_top = client.get("/scores/top")
    assert res_top.status_code == 200
    top_data = res_top.get_json()
    assert top_data["count"] == 1
    assert top_data["leaderboard"][0]["player_name"] == "Arjuna"
    assert top_data["leaderboard"][0]["score"] == 50000


def test_stats_route(client):
    client.post("/scores", json={"player_name": "Hero", "score": 10000, "level_reached": 5, "difficulty": "normal"})
    res = client.get("/scores/stats")
    assert res.status_code == 200
    stats = res.get_json()
    assert stats["total_games_submitted"] == 1
    assert stats["highest_score"] == 10000
