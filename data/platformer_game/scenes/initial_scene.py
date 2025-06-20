# data\platformer_game\scenes\initial_scene.py

import pygame
from engine.scene import Scene
from data.platformer_game.entities.player import Player
from data.platformer_game.scenes.menu import MenuScene

class InitialScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(100, 300)
        self.ground_y = 400
        self.input_manager = game.input_manager
        self.input_manager.clear_callbacks()

        self.input_manager.bind_key_down(pygame.K_m, self.open_menu)

        self.input_manager.map_action_to_key('move_left', pygame.K_LEFT)
        self.input_manager.map_action_to_key('move_right', pygame.K_RIGHT)
        self.input_manager.map_action_to_key('jump', pygame.K_SPACE)

    def open_menu(self):
        self.game.change_scene(MenuScene)

    def handle_events(self, events):
        pass

    def update(self, dt):
        # Instead of raw keys, query actions:
        move_left = self.input_manager.is_action_active('move_left')
        move_right = self.input_manager.is_action_active('move_right')
        jump = self.input_manager.is_action_active('jump')

        self.player.update(dt, move_left, move_right, jump, self.ground_y)

    def render(self, surface):
        surface.fill((135, 206, 235))  # Sky blue background

        # Draw ground platform
        pygame.draw.rect(surface, (50, 205, 50), (0, self.ground_y, 640, 80))

        self.player.render(surface)
