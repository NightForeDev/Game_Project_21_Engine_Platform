import pygame
from engine.entity import Entity

class Player(Entity):
    WIDTH = 40
    HEIGHT = 60
    GRAVITY = 900  # pixels per second squared
    JUMP_VELOCITY = -450
    MOVE_SPEED = 250

    def __init__(self, x, y):
        super().__init__(x, y)
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self, dt, move_left, move_right, jump, ground_y):
        self.vx = 0
        if move_left:
            self.vx = -self.MOVE_SPEED
        elif move_right:
            self.vx = self.MOVE_SPEED

        if jump and self.on_ground:
            self.vy = self.JUMP_VELOCITY
            self.on_ground = False

        self.vy += self.GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.y + self.HEIGHT >= ground_y:
            self.y = ground_y - self.HEIGHT
            self.vy = 0
            self.on_ground = True

        self.x = max(0, min(self.x, 640 - self.WIDTH))

    def render(self, surface):
        color = (255, 100, 100) if self.on_ground else (255, 180, 180)
        pygame.draw.rect(surface, color, (int(self.x), int(self.y), self.WIDTH, self.HEIGHT))
