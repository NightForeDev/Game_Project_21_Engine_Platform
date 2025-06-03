import pygame
from engine.scene import Scene
from games.simple_game.entities.player import Player

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(300, 220)
        self.input_manager = game.input_manager

        # Bind quit key
        self.input_manager.bind_key(pygame.K_ESCAPE, self.quit_game)

        # Map movement keys to actions
        self.input_manager.map_action('move_left', pygame.K_LEFT)
        self.input_manager.map_action('move_right', pygame.K_RIGHT)
        self.input_manager.map_action('move_up', pygame.K_UP)
        self.input_manager.map_action('move_down', pygame.K_DOWN)

    def quit_game(self):
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            self.input_manager.handle_event(event)

    def update(self, dt):
        # Query input manager for actions
        move_left = self.input_manager.is_action_active('move_left')
        move_right = self.input_manager.is_action_active('move_right')
        move_up = self.input_manager.is_action_active('move_up')
        move_down = self.input_manager.is_action_active('move_down')

        self.player.update(dt, move_left, move_right, move_up, move_down)

    def render(self, surface):
        surface.fill((30, 30, 30))
        self.player.render(surface)
