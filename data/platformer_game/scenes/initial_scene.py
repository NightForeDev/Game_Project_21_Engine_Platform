# data\platformer_game\scenes\initial_scene.py

import pygame
from engine.base_scene import BaseScene
from data.platformer_game.entities.player import Player
from data.platformer_game.scenes.menu_scene import MenuScene

class InitialScene(BaseScene):
    def __init__(self, core_manager):
        self.player = Player(100, 300)
        self.ground_y = 400

        # Initialize BaseScene and components
        super().__init__(core_manager)

    """
    Configuration
        enter
        exit
        _setup
        _setup_input
    """
    def enter(self):
        super().enter()

    def exit(self):
        super().exit()

    def _setup(self):
        """
        Initialize components.
        """
        super()._setup()

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key_down": pygame.K_m, "callback": lambda: self.scene_manager.push_scene(MenuScene)}
            ],
            "map": {
                "move_left": {"key": pygame.K_LEFT},
                "move_right": {"key": pygame.K_RIGHT},
                "jump": {"key": pygame.K_SPACE}
            }
        }

        self.input_manager.load_config(input_config)


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
        move_left = self.input_manager.is_action_active('move_left')
        move_right = self.input_manager.is_action_active('move_right')
        jump = self.input_manager.is_action_active('jump')
        self.player.update(dt, move_left, move_right, jump, self.ground_y)

    def render(self, surface=None):
        """
        Render components.
        """
        surface.fill((135, 206, 235))  # Sky blue background

        # Draw ground platform
        pygame.draw.rect(surface, (50, 205, 50), (0, self.ground_y, 640, 80))

        self.player.render(surface)
