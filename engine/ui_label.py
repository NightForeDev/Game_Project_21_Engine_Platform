# engine/ui_label.py

import pygame
from engine.ui_element import UIElement

class UILabel(UIElement):
    """
    UI label for displaying text.

    Attributes:
        text (str): Text content.
        font (pygame.font.Font): Font used for rendering text.
        color (tuple): Text color.
        align (str): "left" | "center" | "right"
    """
    def __init__(self, name, text="", x=0, y=0, w=100, h=30,
                 font=None, color=(255, 255, 255), align="left", **kwargs):
        super().__init__(name, x, y, w, h, **kwargs)
        self.text = text
        self.font = font or pygame.font.SysFont(None, 24)
        self.color = color
        self.align = align

    def render(self, surface):
        if not self.visible:
            return

        # Render text and blit according to alignment
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect()
        if self.align == "center":
            text_rect.center = self.rect.center
        elif self.align == "right":
            text_rect.midright = self.rect.midright
        else:  # left
            text_rect.midleft = (self.rect.left + 4, self.rect.centery)
        surface.blit(text_surf, text_rect)

    def __repr__(self):
        return f"<UILabel name={self.name} text={self.text!r} rect={self.rect}>"