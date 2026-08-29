"""
Vimana Wars — main entry point
Run this file to start the game.
"""
import arcade
from game.window import create_window


def main():
    create_window()
    arcade.run()


if __name__ == "__main__":
    main()
