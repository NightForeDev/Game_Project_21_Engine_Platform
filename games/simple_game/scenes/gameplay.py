import pygame
from engine.scene import Scene
from games.simple_game.entities.player import Player

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(300, 220)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

    def render(self, surface):
        surface.fill((30, 30, 30))
        self.player.render(surface)
