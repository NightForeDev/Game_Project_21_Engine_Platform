# data\launcher\scenes\initial_scene.py

import os
import sys
import subprocess
import pygame

from data.shared.constants import SHARED_FOLDER, DATA_FOLDER
from engine.base_scene import BaseScene
from engine.ui_manager import UIManager

CURRENT_FOLDER = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
IGNORE_FOLDERS = {CURRENT_FOLDER, SHARED_FOLDER}

class InitialScene(BaseScene):
    def __init__(self, core, debug=False):
        super().__init__(core)

        self.font = pygame.font.SysFont(None, 28)
        self.bg_color = (40, 40, 40)
        self.text_color = (220, 220, 220)
        self.highlight_color = (70, 130, 180)

        self.games = self.list_games()
        self.launched_games = {}
        self.debug = debug

        self.selected_index = 0

        self.ui = UIManager(self.core.app_config if hasattr(self, "core") else None)
        self._setup_ui()

        self._setup_input()

    """
    Configuration
        _setup
        _setup_input
        _setup_ui
    """
    def _setup(self, run):
        """
        Initialize and prepare all components.
        """
        # Initialize components
        self._setup_input()
        self._setup_ui()

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key": pygame.K_UP, "callback": self.select_up},
                {"key": pygame.K_DOWN, "callback": self.select_down},
                {"key": pygame.K_RETURN, "callback": self.select_confirm}
            ]
        }
        self.input_manager.load_config(input_config)

    @staticmethod
    def list_games():
        return [
            name for name in os.listdir(DATA_FOLDER)
            if os.path.isdir(os.path.join(DATA_FOLDER, name)) and name not in IGNORE_FOLDERS
        ]

    def _setup_ui(self):
        """
        Build title label and buttons for each game plus a Quit button.
        Buttons call launch_game(name) when clicked.
        """
        # Title label
        title_h = 40
        label = {
            "type": "UILabel",
            "text": "Select a game to launch:",
            "x": 20,
            "y": 10,
            "w": 600,
            "h": title_h,
            "font": self.font,
            "color": self.text_color,
            "align": "left",
        }
        self.ui.create_element("title", "UILabel", **label)

        # Buttons area
        start_y = 60
        btn_w = 300
        btn_h = 32
        gap = 6

        # Create a button for each game
        for i, game in enumerate(self.games):
            name = f"game_btn_{i}"
            cfg = {
                "type": "UIButton",
                "text": game,
                "x": 40,
                "y": start_y + i * (btn_h + gap),
                "w": btn_w,
                "h": btn_h,
                "font": pygame.font.SysFont(None, 22),
                "bg_color": (60, 60, 60),
                "text_color": self.text_color,
                "callback": self._make_launch_callback(game),
            }
            self.ui.create_element(name, "UIButton", **cfg)

        # Quit button placed after game list
        quit_y = start_y + len(self.games) * (btn_h + gap)
        quit_cfg = {
            "type": "UIButton",
            "text": "Quit",
            "x": 40,
            "y": quit_y,
            "w": btn_w,
            "h": btn_h,
            "font": pygame.font.SysFont(None, 22),
            "bg_color": (60, 60, 60),
            "text_color": self.text_color,
            "callback": self.quit_game,
        }
        self.ui.create_element("quit_btn", "UIButton", **quit_cfg)

        # Ensure initial highlight
        self._update_highlight()

    def _make_launch_callback(self, game_name):
        """Return a callback that launches the given game."""
        def _cb():
            self.launch_game(game_name)
        return _cb

    """
    Selection helpers
    """
    def _update_highlight(self):
        """
        Update button highlight according to selected_index.
        selected_index from 0..len(games) => last index is Quit button.
        """
        total = len(self.games) + 1
        self.selected_index %= total

        # clear all highlights
        for i in range(len(self.games)):
            btn = self.ui.elements.get(f"game_btn_{i}")
            if btn:
                btn.set_highlighted(False)

        # quit button
        quit_btn = self.ui.elements.get("quit_btn")
        if quit_btn:
            quit_btn.set_highlighted(False)

        # set highlight on currently selected
        if self.selected_index < len(self.games):
            btn = self.ui.elements.get(f"game_btn_{self.selected_index}")
            if btn:
                btn.set_highlighted(True)
        else:
            if quit_btn:
                quit_btn.set_highlighted(True)

    def select_up(self):
        self.selected_index = (self.selected_index - 1) % (len(self.games) + 1)
        self._update_highlight()

    def select_down(self):
        self.selected_index = (self.selected_index + 1) % (len(self.games) + 1)
        self._update_highlight()

    def select_confirm(self):
        if self.selected_index < len(self.games):
            game = self.games[self.selected_index]
            self.launch_game(game)
        else:
            self.quit_game()

    def launch_game(self, game_name):
        if not self.debug and self.launched_games:
            print("A game is already running.")
            return

        proc = self.launched_games.get(game_name)
        if proc and proc.poll() is None:
            print(f"Game '{game_name}' is already running.")
            return

        print(f"Launching game '{game_name}'...")
        run_path = os.path.abspath(sys.argv[0])
        proc = subprocess.Popen([sys.executable, run_path, game_name])
        self.launched_games[game_name] = proc

        # Minimize the window
        if not self.debug:
            pygame.display.iconify()

    """
    Operations
        events
        update
        render
    """
    def events(self, events):
        """
        Process components events.
        """
        pass

    def update(self, dt=None):
        """
        Update components.
        """
        self.ui.update()

    def render(self, surface=None):
        """
        Render components.
        """
        surface.fill(self.bg_color)
        self.ui.render(surface)
