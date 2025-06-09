# engine\draw_utils.py

import pygame

def draw_text(surface, text, pos, font=None, color=(255, 255, 255)):
    if font is None:
        font = pygame.font.SysFont("Consolas", 16)
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)
