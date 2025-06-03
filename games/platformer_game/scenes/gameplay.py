import pygame
from engine.scene import Scene
from games.platformer_game.entities.player import Player

class GameplayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player = Player(100, 300)
        self.ground_y = 400  # y position of the floor

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys, self.ground_y)

    def render(self, surface):
        surface.fill((135, 206, 235))  # Sky blue background

        # Draw ground platform
        pygame.draw.rect(surface, (50, 205, 50), (0, self.ground_y, 640, 80))

        self.player.render(surface)
