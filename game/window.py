"""
game/window.py
Creates the arcade window and shows the initial view.
"""
import arcade
from constants import WIDTH, HEIGHT, SCREEN_TITLE


def create_window() -> arcade.Window:
    window = arcade.Window(WIDTH, HEIGHT, SCREEN_TITLE, resizable=False)
    from game.views.menu_view import MenuView
    window.show_view(MenuView())
    return window
