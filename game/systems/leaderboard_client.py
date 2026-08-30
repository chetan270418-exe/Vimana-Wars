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

    @staticmethod
    def _auth_headers() -> dict:
        from game.systems import save_system
        token = save_system.load().get("auth_token", "")
        return {"Authorization": f"Bearer {token}"} if token else {}

    @staticmethod
    def _merge_profile(profile: dict) -> None:
        from game.systems import save_system
        if not isinstance(profile, dict):
            return
        data = save_system.load()
        for key in save_system.profile_for_sync().keys():
            if key in profile:
                data[key] = profile[key]
        save_system.save(data)

    @staticmethod
    def _save_account(token: str, user: dict) -> None:
        from game.systems import save_system
        data = save_system.load()
        data["auth_token"] = token
        data["game_id"] = user.get("game_id", "")
        data["account_email"] = user.get("email", "")
        if user.get("player_name"):
            data["player_name"] = user["player_name"]
        save_system.save(data)

    @staticmethod
    def current_account() -> dict | None:
        from game.systems import save_system
        data = save_system.load()
        if not data.get("auth_token") or not data.get("game_id"):
            return None
        return {
            "game_id": data.get("game_id", ""),
            "email": data.get("account_email", ""),
            "player_name": data.get("player_name", "Warrior"),
        }

    def _account_request(self, endpoint: str, payload: dict, on_complete=None) -> None:
        """Run register/login without blocking the Arcade render thread."""
        with self._lock:
            self.is_loading = True
            self.last_error = None

        def _worker():
            success = False
            error = None
            user = None
            try:
                resp = requests.post(
                    f"{self.api_url}{endpoint}",
                    json=payload,
                    timeout=NETWORK_TIMEOUT,
                )
                body = resp.json() if resp.content else {}
                if resp.status_code in (200, 201) and body.get("token"):
                    success = True
                    user = body.get("user") or {}
                    self._save_account(body["token"], user)
                    # Pull cloud progression after authentication. This runs
                    # independently so login remains fast when the profile is empty.
                    self.sync_profile()
                else:
                    error = body.get("error", f"Account request failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                error = "Account server offline — guest mode is still available"
            finally:
                with self._lock:
                    self.last_error = error
                    self.is_loading = False
                if on_complete:
                    on_complete(success, error, user)

        threading.Thread(target=_worker, daemon=True).start()

    def register(self, email: str, password: str, player_name: str,
                 on_complete=None) -> None:
        self._account_request(
            "/auth/register",
            {"email": email, "password": password, "player_name": player_name},
            on_complete,
        )

    def login(self, email: str, password: str, on_complete=None) -> None:
        self._account_request(
            "/auth/login", {"email": email, "password": password}, on_complete
        )

    def logout(self, on_complete=None) -> None:
        """Clear the local session even if the server is unreachable."""
        from game.systems import save_system
        headers = self._auth_headers()
        data = save_system.load()
        data["auth_token"] = ""
        data["game_id"] = ""
        data["account_email"] = ""
        save_system.save(data)

        def _worker():
            error = None
            try:
                requests.post(f"{self.api_url}/auth/logout", headers=headers, timeout=NETWORK_TIMEOUT)
            except requests.exceptions.RequestException:
                error = "Signed out locally"
            if on_complete:
                on_complete(error)
        threading.Thread(target=_worker, daemon=True).start()

    def sync_profile(self, on_complete=None) -> None:
        """Pull authenticated progression/achievements into the local save."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(False, "Not signed in", None)
            return

        def _worker():
            success, error, profile = False, None, None
            try:
                resp = requests.get(f"{self.api_url}/account/profile", headers=headers, timeout=NETWORK_TIMEOUT)
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    profile = body.get("profile") or {}
                    self._merge_profile(profile)
                    success = True
                else:
                    error = body.get("error", f"Profile sync failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                error = "Cloud profile unavailable — local progress is safe"
            if on_complete:
                on_complete(success, error, profile)

        threading.Thread(target=_worker, daemon=True).start()

    def push_profile(self, on_complete=None) -> None:
        """Push the local gameplay profile to the authenticated account."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(False, "Not signed in")
            return
        from game.systems import save_system
        payload = {"profile": save_system.profile_for_sync()}

        def _worker():
            success, error = False, None
            try:
                resp = requests.put(
                    f"{self.api_url}/account/profile", json=payload,
                    headers=headers, timeout=NETWORK_TIMEOUT,
                )
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    success = True
                else:
                    error = body.get("error", f"Profile sync failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                error = "Cloud profile unavailable — local progress is safe"
            if on_complete:
                on_complete(success, error)

        threading.Thread(target=_worker, daemon=True).start()

    def fetch_account_stats(self, on_complete=None) -> None:
        """Fetch server-calculated stats for the signed-in account."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(None, "Not signed in")
            return

        def _worker():
            stats, error = None, None
            try:
                resp = requests.get(f"{self.api_url}/account/stats", headers=headers, timeout=NETWORK_TIMEOUT)
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    stats = body
                else:
                    error = body.get("error", f"Stats request failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                error = "Online stats unavailable"
            if on_complete:
                on_complete(stats, error)

        threading.Thread(target=_worker, daemon=True).start()

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
                     stats: dict | None = None,
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
                run_stats = stats or {}
                payload["kills"] = max(0, int(run_stats.get("kills", 0)))
                payload["total_damage"] = max(0, int(run_stats.get("total_damage", 0)))
                payload["duration_seconds"] = max(0.0, float(run_stats.get("duration_seconds", 0)))
                resp = requests.post(
                    f"{self.api_url}/scores",
                    json=payload,
                    headers=self._auth_headers(),
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 201:
                    success = True
                    err = None
                else:
                    success = False
                    try:
                        err = resp.json().get("error", f"Submission error {resp.status_code}")
                    except ValueError:
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
