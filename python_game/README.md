# Vimana Wars — Python Edition (Arcade)

This directory contains the original Python Arcade edition of **Vimana Wars**, including all entity definitions, game systems, custom UI components, views, tests, and backend services.

---

## Structure
- `game/`: Python game package (entities, systems, UI, views, window).
- `backend/`: Flask REST API backend + Socket.IO duel server.
- `tests/`: Automated unit tests for entities, systems, and backend.
- `main.py`: Main entry point (`python main.py`).
- `constants.py`: Vedic cyberpunk color palette, ship balance, and wave configurations.
- `vimana_wars_python_all_in_one.py`: **Single-file consolidated archive** containing all 77 Python source files in one monolithic file with Table of Contents.
- `start_python_game.bat`: 1-click batch launcher.
- `requirements.txt`: Python dependencies (`arcade`, `flask`, `flask-socketio`, etc.).

---

## Quick Start
```bash
pip install -r requirements.txt
python main.py
```
Or double-click `start_python_game.bat`.
