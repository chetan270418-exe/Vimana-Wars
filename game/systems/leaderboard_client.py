"""
game/systems/leaderboard_client.py
Asynchronous network client for the Vimana Wars Leaderboard API.
Executes all HTTP calls on background daemon threads so the game thread
never drops frames or freezes on network latency/offline mode.
"""
import threading
import requests
from constants import LEADERBOARD_API_URL, NETWORK_TIMEOUT


class LeaderboardClient:
    """
    Non-blocking client for online score submissions and queries.
    """

    def __init__(self, api_url: str = LEADERBOARD_API_URL):
        self.api_url = api_url.rstrip("/")
        self.is_loading = False
        self.last_error: str | None = None
        self.top_scores: list[dict] = []
        self.submission_success = False

    def fetch_top(self, limit: int = 10, difficulty: str | None = None, on_complete=None) -> None:
        """
        Fetch top leaderboard records asynchronously.
        """
        self.is_loading = True
        self.last_error = None

        def _worker():
            try:
                params = {"limit": limit}
                if difficulty:
                    params["difficulty"] = difficulty

                resp = requests.get(
                    f"{self.api_url}/scores/top",
                    params=params,
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 200:
                    data = resp.json()
                    self.top_scores = data.get("leaderboard", [])
                    self.last_error = None
                else:
                    self.last_error = f"Server returned {resp.status_code}"
            except requests.exceptions.RequestException:
                self.last_error = "Leaderboard offline (Could not connect to server)"
                self.top_scores = []
            finally:
                self.is_loading = False
                if on_complete:
                    on_complete(self.top_scores, self.last_error)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def submit_score(self, player_name: str, score: int, level_reached: int,
                     difficulty: str = "normal", on_complete=None) -> None:
        """
        Submit a score record asynchronously.
        """
        self.is_loading = True
        self.last_error = None
        self.submission_success = False

        def _worker():
            try:
                payload = {
                    "player_name": player_name,
                    "score": score,
                    "level_reached": level_reached,
                    "difficulty": difficulty,
                }
                resp = requests.post(
                    f"{self.api_url}/scores",
                    json=payload,
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 201:
                    self.submission_success = True
                    self.last_error = None
                else:
                    self.submission_success = False
                    self.last_error = f"Submission error {resp.status_code}"
            except requests.exceptions.RequestException:
                self.submission_success = False
                self.last_error = "Server offline — score saved locally"
            finally:
                self.is_loading = False
                if on_complete:
                    on_complete(self.submission_success, self.last_error)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()


# Global singleton instance for easy access
leaderboard_client = LeaderboardClient()
