import pygame
from engine.entity import Entity

class Player(Entity):
    SPEED = 200  # pixels per second

    def update(self, dt, move_left, move_right, move_up, move_down):
        if move_left:
            self.x -= self.SPEED * dt
        if move_right:
            self.x += self.SPEED * dt
        if move_up:
            self.y -= self.SPEED * dt
        if move_down:
            self.y += self.SPEED * dt

        # Keep inside screen bounds (640x480)
        self.x = max(0, min(self.x, 640 - 50))
        self.y = max(0, min(self.y, 480 - 50))

    def render(self, surface):
        pygame.draw.rect(surface, (200, 50, 50), (int(self.x), int(self.y), 50, 50))
