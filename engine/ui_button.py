# engine/ui_label.py

import pygame
from engine.ui_element import UIElement
from typing import Callable

class UIButton(UIElement):
    """
    UI button with callback support.

    Attributes:
        text (str): Button label.
        font (pygame.font.Font): Font used for rendering text.
        bg_color (tuple): Background color.
        text_color (tuple): Text color.
        callback (Callable): Function to call when pressed.
        highlighted (bool): Visual highlighted state.
    """
    def __init__(self, name, text="Button", x=0, y=0, w=120, h=40,
                 font=None, bg_color=(70, 70, 70), text_color=(255, 255, 255),
                 callback: Callable = None, highlighted=False, **kwargs):
        super().__init__(name, x, y, w, h, **kwargs)
        self.text = text
        self.font = font or pygame.font.SysFont(None, 22)
        self.bg_color = bg_color
        self.text_color = text_color
        self.callback = callback
        self.highlighted = highlighted
        self.focused = False

        # Internal state for edge detection of mouse button
        self._mouse_was_down = False

    def set_highlighted(self, state: bool):
        """Set visual highlighted state."""
        self.highlighted = bool(state)

    def update(self):
        if not self.visible:
            self._mouse_was_down = False
            return

        mx, my = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        # If mouse is pressed now and wasn't pressed previously and pointer is inside -> trigger
        if mouse_down and not self._mouse_was_down and self.rect.collidepoint(mx, my):
            if self.callback:
                try:
                    self.callback()
                except Exception:
                    # swallow exceptions — caller can log if needed
                    pass

        # update edge state
        self._mouse_was_down = mouse_down

    def set_focus(self, state):
        self.focused = state

    def render(self, surface):
        if not self.visible:
            return

        # base background
        self.highlighted = self.focused
        bg = self.bg_color
        if self.highlighted:
            # slightly brighter when highlighted
            bg = (min(255, bg[0] + 30), min(255, bg[1] + 30), min(255, bg[2] + 30))

        pygame.draw.rect(surface, bg, self.rect)

        # text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def __repr__(self):
        return f"<UIButton name={self.name} text={self.text!r} rect={self.rect} highlighted={self.highlighted}>"
