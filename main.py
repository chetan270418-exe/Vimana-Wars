"""
Vimana Wars — Root Python Launcher.
Delegates to python_game/main.py.

For the native high-performance C++ engine, run start.bat or cpp_game/bin/VimanaWars.exe.
"""
import os
import sys
from pathlib import Path

# Add python_game directory to Python module search path
PYTHON_GAME_DIR = Path(__file__).resolve().parent / "python_game"
sys.path.insert(0, str(PYTHON_GAME_DIR))

if __name__ == "__main__":
    from game.window import create_window
    import arcade
    create_window()
    arcade.run()
