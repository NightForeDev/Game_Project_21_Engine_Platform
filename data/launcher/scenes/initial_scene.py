# data\launcher\scenes\initial_scene.py

import os
import sys
import subprocess
import pygame

from data.shared.constants import SHARED_FOLDER, DATA_FOLDER
from engine.scene import Scene

CURRENT_FOLDER = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
IGNORE_FOLDERS = {CURRENT_FOLDER, SHARED_FOLDER}

class InitialScene(Scene):
    def __init__(self, game, debug=False):
        super().__init__(game)

        self.font = pygame.font.SysFont(None, 28)
        self.bg_color = (40, 40, 40)
        self.text_color = (220, 220, 220)
        self.highlight_color = (70, 130, 180)
        self.selected_index = 0

        self.games = self.list_games()

        self.launched_games = {}
        self.debug = debug

        self.setup_input()

    """
    Input Methods
        setup_input
    """

    def setup_input\
                    (self):
        """Bind and map keys and mouse buttons to actions or callbacks."""
        input_config = {
            "bind": [
                {"mouse": 1, "callback": self.mouse_left_click},
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

    def mouse_left_click(self):
        mx, my = pygame.mouse.get_pos()
        start_y = 50
        for i, game in enumerate(self.games):
            rect = pygame.Rect(40, start_y + i * 30, 200, 28)
            if rect.collidepoint(mx, my):
                self.launch_game(game)
                return
        if pygame.Rect(40, start_y + len(self.games) * 30, 100, 28).collidepoint(mx, my):
            self.quit_game()

    def select_up(self):
        self.selected_index = (self.selected_index - 1) % (len(self.games) + 1)

    def select_down(self):
        self.selected_index = (self.selected_index + 1) % (len(self.games) + 1)

    def select_confirm(self):
        if self.selected_index != len(self.games):
            self.launch_game(self.games[self.selected_index])
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

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill(self.bg_color)
        title_surf = self.font.render("Select a game to launch:", True, self.text_color)
        surface.blit(title_surf, (20, 10))

        start_y = 50
        for i, game in enumerate(self.games):
            color = self.highlight_color if i == self.selected_index else self.text_color
            text_surf = self.font.render(game, True, color)
            surface.blit(text_surf, (40, start_y + i * 30))

        quit_color = self.highlight_color if self.selected_index == len(self.games) else self.text_color
        quit_surf = self.font.render("Quit", True, quit_color)
        surface.blit(quit_surf, (40, start_y + len(self.games) * 30))
