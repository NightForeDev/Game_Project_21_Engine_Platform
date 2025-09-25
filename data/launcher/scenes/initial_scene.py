# data\launcher\scenes\initial_scene.py

import os
import sys
import subprocess
import pygame

from data.shared.constants import SHARED_FOLDER, DATA_FOLDER
from engine.base_scene import BaseScene

CURRENT_FOLDER = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
IGNORE_FOLDERS = {CURRENT_FOLDER, SHARED_FOLDER}


class InitialScene(BaseScene):
    def __init__(self, core_manager, debug=False):
        self.font = pygame.font.SysFont(None, 28)
        self.bg_color = (40, 40, 40)
        self.text_color = (220, 220, 220)
        self.games = self.list_games()
        self.launched_games = {}
        self.debug = debug

        # Initialize BaseScene and components
        super().__init__(core_manager)

    """
    Configuration
        _setup
        enter
        exit
        _setup_input
        _setup_ui
    """
    def _setup(self):
        """
        Initialize components.
        """
        super()._setup()

        # Initialize components
        self._setup_ui()

    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key_down": pygame.K_UP, "callback": self.ui_manager.focus_prev, "global": True},
                {"key_down": pygame.K_DOWN, "callback": self.ui_manager.focus_next, "global": True},
                {"key_down": pygame.K_RETURN, "callback": self.ui_manager.activate_focused, "global": True},
            ]
        }
        self.input_manager.load_config(input_config)

    def _setup_ui(self):
        """
        Build title label and buttons for each game plus a Quit button.
        """
        # Title label
        self.ui_manager.create_element(
            name="title",
            element_type="UILabel",
            text="Select a game to launch:",
            x=20, y=10, w=600, h=40,
            font=self.font,
            color=self.text_color,
            align="left",
            layer="background"
        )

        # Buttons area
        start_y = 60
        btn_w = 300
        btn_h = 32
        gap = 6

        # Create a button for each game
        for i, game in enumerate(self.games):
            name = f"game_btn_{i}"
            self.ui_manager.create_element(
                name, "UIButton",
                text=game,
                x=40, y=start_y + i * (btn_h + gap),
                w=btn_w, h=btn_h,
                font=pygame.font.SysFont(None, 22),
                bg_color=(60, 60, 60),
                text_color=self.text_color,
                callback=self._make_launch_callback(game),
                focusable=True,
                layer="ui"
            )

        # Quit button placed after game list
        quit_y = start_y + len(self.games) * (btn_h + gap)
        self.ui_manager.create_element(
            "quit_btn", "UIButton",
            text="Quit",
            x=40, y=quit_y,
            w=btn_w, h=btn_h,
            font=pygame.font.SysFont(None, 22),
            bg_color=(60, 60, 60),
            text_color=self.text_color,
            callback=self.core_manager.quit_game,
            focusable=True,
            layer="ui"
        )

        # Ensure initial focus
        if self.games:
            self.ui_manager.focus("game_btn_0")
        else:
            self.ui_manager.focus("quit_btn")

    """
    Helpers
    """
    @staticmethod
    def list_games():
        """Return list of available game folders."""
        return [
            name for name in os.listdir(DATA_FOLDER)
            if os.path.isdir(os.path.join(DATA_FOLDER, name)) and name not in IGNORE_FOLDERS
        ]

    def _make_launch_callback(self, game_name):
        """Return a callback that launches the given game."""
        def _cb():
            self.launch_game(game_name)
        return _cb

    def launch_game(self, game_name):
        """Launch the given game in a new subprocess."""
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
        pass

    def render(self, surface=None):
        """
        Render components.
        """
        surface.fill(self.bg_color)
