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
        self._lock = threading.Lock()
        self.is_loading = False
        self.last_error: str | None = None
        self.top_scores: list[dict] = []
        self.submission_success = False

    def fetch_top(self, limit: int = 10, difficulty: str | None = None, on_complete=None) -> None:
        """
        Fetch top leaderboard records asynchronously.
        """
        with self._lock:
            self.is_loading = True
            self.last_error = None

        def _worker():
            scores = []
            err = None
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
                    scores = list(data.get("leaderboard", []))
                    err = None
                else:
                    err = f"Server returned {resp.status_code}"
            except requests.exceptions.RequestException:
                err = "Leaderboard offline (Could not connect to server)"
                scores = []
            finally:
                with self._lock:
                    self.top_scores = list(scores)
                    self.last_error = err
                    self.is_loading = False
                if on_complete:
                    on_complete(scores, err)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def submit_score(self, player_name: str, score: int, level_reached: int,
                     difficulty: str = "normal", ship_class: str = "pushpaka",
                     on_complete=None) -> None:
        """
        Submit a score record asynchronously.
        """
        with self._lock:
            self.is_loading = True
            self.last_error = None
            self.submission_success = False

        def _worker():
            success = False
            err = None
            try:
                payload = {
                    "player_name": player_name,
                    "score": score,
                    "level_reached": level_reached,
                    "difficulty": difficulty,
                    "ship_class": ship_class,
                }
                resp = requests.post(
                    f"{self.api_url}/scores",
                    json=payload,
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 201:
                    success = True
                    err = None
                else:
                    success = False
                    err = f"Submission error {resp.status_code}"
            except requests.exceptions.RequestException:
                success = False
                err = "Server offline — score saved locally"
            finally:
                with self._lock:
                    self.submission_success = success
                    self.last_error = err
                    self.is_loading = False
                if on_complete:
                    on_complete(success, err)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()


# Global singleton instance for easy access
leaderboard_client = LeaderboardClient()
