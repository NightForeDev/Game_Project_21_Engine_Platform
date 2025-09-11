# data\platformer_game\scenes\initial_scene.py

import pygame
from engine.base_scene import BaseScene
from data.platformer_game.entities.player import Player
from data.platformer_game.scenes.menu import MenuScene

class InitialScene(BaseScene):
    def __init__(self, core):
        super().__init__(core)
        self.player = Player(100, 300)
        self.ground_y = 400
        self.input_manager = core.input_manager
        self.input_manager.clear_local_callbacks()

        self.setup_input()

    """
    Input Methods
        setup_input
    """
    def setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key": pygame.K_m, "callback": self.open_menu}
            ],
            "map": {
                "move_left": {"key": pygame.K_LEFT},
                "move_right": {"key": pygame.K_RIGHT},
                "jump": {"key": pygame.K_SPACE}
            }
        }

        self.input_manager.load_config(input_config)

    def open_menu(self):
        self.game.change_scene(MenuScene)

    def events(self, events):
        pass

    def update(self, dt=None):
        # Instead of raw keys, query actions:
        move_left = self.input_manager.is_action_active('move_left')
        move_right = self.input_manager.is_action_active('move_right')
        jump = self.input_manager.is_action_active('jump')

        self.player.update(dt, move_left, move_right, jump, self.ground_y)

    def render(self, surface=None):
        surface.fill((135, 206, 235))  # Sky blue background

        # Draw ground platform
        pygame.draw.rect(surface, (50, 205, 50), (0, self.ground_y, 640, 80))

        self.player.render(surface)
