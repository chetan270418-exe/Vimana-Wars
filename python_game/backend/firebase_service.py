"""
backend/firebase_service.py
Google Service Account (GSA) & Firebase Admin Integration for Vimana Wars.

Supports:
- Firebase Firestore NoSQL Database for Users, Leaderboards, Match History, and Cloud Saves.
- Authenticates using Google Service Account (GSA) credentials:
  1. File path: `serviceAccountKey.json` in backend/ or repository root.
  2. Environment variable: `GOOGLE_APPLICATION_CREDENTIALS` path.
  3. Environment variable: `FIREBASE_SERVICE_ACCOUNT_JSON` containing inline JSON string.
- Dual-mode architecture: seamlessly synchronizes when GSA is present,
  gracefully operates in local mode when awaiting GSA key.
"""
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger("vimana.firebase")

_firebase_app = None
_firestore_db = None
_initialized = False
_init_error: Optional[str] = None


def get_gsa_credential_path() -> Optional[Path]:
    """Locate Google Service Account key file if present."""
    # 1. Check standard Google env var
    env_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    # 2. Check local backend directory
    backend_dir = Path(__file__).resolve().parent
    candidates = [
        backend_dir / "serviceAccountKey.json",
        backend_dir / "firebase-service-account.json",
        backend_dir / "gsa_key.json",
        backend_dir.parent / "serviceAccountKey.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def init_firebase() -> bool:
    """Initialize Firebase Admin SDK using Google Service Account (GSA)."""
    global _firebase_app, _firestore_db, _initialized, _init_error

    if _initialized:
        return _firestore_db is not None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError:
        _init_error = "firebase-admin library not installed. Run: pip install firebase-admin"
        logger.info(_init_error)
        _initialized = True
        return False

    try:
        # Check for inline JSON credentials in environment variable
        raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        cred = None

        if raw_json:
            try:
                cert_dict = json.loads(raw_json)
                cred = credentials.Certificate(cert_dict)
                logger.info("Loaded GSA credentials from FIREBASE_SERVICE_ACCOUNT_JSON")
            except Exception as e:
                logger.warning("Failed to parse FIREBASE_SERVICE_ACCOUNT_JSON: %s", e)

        if cred is None:
            key_path = get_gsa_credential_path()
            if key_path:
                cred = credentials.Certificate(str(key_path))
                logger.info("Loaded GSA credentials from file: %s", key_path)

        if cred is None:
            _init_error = (
                "Google Service Account (GSA) key not found. "
                "Place serviceAccountKey.json in backend/ or set GOOGLE_APPLICATION_CREDENTIALS."
            )
            logger.info("Firebase: %s (operating in SQLite/Postgres mode)", _init_error)
            _initialized = True
            return False

        if not firebase_admin._apps:
            _firebase_app = firebase_admin.initialize_app(cred)
        else:
            _firebase_app = firebase_admin.get_app()

        _firestore_db = firestore.client()
        _initialized = True
        logger.info("Firebase Firestore connected successfully via Google Service Account!")
        return True

    except Exception as exc:
        _init_error = f"Firebase initialization failed: {exc}"
        logger.warning(_init_error)
        _initialized = True
        return False


def is_firebase_active() -> bool:
    """Check if Firebase Firestore is active and ready."""
    if not _initialized:
        init_firebase()
    return _firestore_db is not None


def get_firebase_status() -> Dict[str, Any]:
    """Return current Firebase GSA connection status for system health reports."""
    if not _initialized:
        init_firebase()
    return {
        "active": _firestore_db is not None,
        "gsa_key_detected": get_gsa_credential_path() is not None or bool(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")),
        "error": _init_error,
    }


# ── Firestore Synchronization Operations ──────────────────────────────────────

def save_user_to_firebase(user_dict: Dict[str, Any]) -> bool:
    """Save or update user record in Firestore 'users' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        game_id = user_dict.get("game_id")
        if not game_id:
            return False
        doc_ref = _firestore_db.collection("users").document(game_id)
        payload = {
            "game_id": game_id,
            "email": user_dict.get("email", ""),
            "player_name": user_dict.get("player_name", "Warrior"),
            "email_verified": bool(user_dict.get("email_verified", False)),
            "updated_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload, merge=True)
        return True
    except Exception as exc:
        logger.error("Error saving user to Firestore: %s", exc)
        return False


def save_score_to_firebase(score_dict: Dict[str, Any]) -> bool:
    """Record high score entry in Firestore 'leaderboard' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        doc_ref = _firestore_db.collection("leaderboard").document()
        payload = {
            "player_name": score_dict.get("player_name", "Warrior"),
            "game_id": score_dict.get("game_id", ""),
            "score": int(score_dict.get("score", 0)),
            "wave": int(score_dict.get("level_reached", score_dict.get("wave", 1))),
            "difficulty": str(score_dict.get("difficulty", "normal")).lower(),
            "ship_class": str(score_dict.get("ship_class", "pushpaka")),
            "kills": int(score_dict.get("kills", 0)),
            "created_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload)
        return True
    except Exception as exc:
        logger.error("Error saving score to Firestore: %s", exc)
        return False


def get_firebase_leaderboard(limit: int = 50) -> List[Dict[str, Any]]:
    """Query top scores from Firestore."""
    if not is_firebase_active():
        return []
    try:
        from google.cloud import firestore as gc_firestore
        scores_ref = (
            _firestore_db.collection("leaderboard")
            .order_by("score", direction=gc_firestore.Query.DESCENDING)
            .limit(limit)
        )
        results = []
        for rank, doc in enumerate(scores_ref.stream(), 1):
            data = doc.to_dict()
            results.append({
                "rank": rank,
                "player_name": data.get("player_name", "Warrior"),
                "game_id": data.get("game_id", ""),
                "score": data.get("score", 0),
                "wave": data.get("wave", 1),
                "difficulty": data.get("difficulty", "normal"),
                "ship_class": data.get("ship_class", "pushpaka"),
            })
        return results
    except Exception as exc:
        logger.error("Error fetching Firestore leaderboard: %s", exc)
        return []


def save_cloud_save_to_firebase(game_id: str, save_data: Dict[str, Any]) -> bool:
    """Save persistent player progression to Firestore 'cloud_saves' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        doc_ref = _firestore_db.collection("cloud_saves").document(game_id)
        payload = {
            "game_id": game_id,
            "save_data": save_data,
            "updated_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload, merge=True)
        return True
    except Exception as exc:
        logger.error("Error saving cloud save to Firestore: %s", exc)
        return False


def get_cloud_save_from_firebase(game_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve player cloud save from Firestore."""
    if not is_firebase_active():
        return None
    try:
        doc = _firestore_db.collection("cloud_saves").document(game_id).get()
        if doc.exists:
            data = doc.to_dict()
            return data.get("save_data")
        return None
    except Exception as exc:
        logger.error("Error retrieving cloud save from Firestore: %s", exc)
        return None

