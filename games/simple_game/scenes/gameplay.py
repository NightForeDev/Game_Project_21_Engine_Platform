import pygame
from engine.scene import Scene
from games.simple_game.entities.player import Player

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(300, 220)
        self.input_manager = game.input_manager

        self.input_manager.bind_key(pygame.K_ESCAPE, self.quit_game)

    def quit_game(self):
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            self.input_manager.handle_event(event)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

    def render(self, surface):
        surface.fill((30, 30, 30))
        self.player.render(surface)
