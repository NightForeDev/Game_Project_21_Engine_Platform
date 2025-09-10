# engine/ui_element.py

import pygame

class UIElement:
    """
    Base class for UI elements.

    Attributes:
        name (str): Element identifier.
        rect (pygame.Rect): Position and size of the element.
        visible (bool): Whether the element is visible.

    Methods:
        update(): Update the element.
        render(surface): Render the element to the given surface.
    """
    def __init__(self, name: str, x=0, y=0, w=100, h=30, visible=True, **kwargs):
        self.name = name
        self.rect = pygame.Rect(int(x), int(y), int(w), int(h))
        self.visible = visible

    def update(self):
        """Update element state."""
        pass

    def render(self, surface):
        """Render element base (debug outline)."""
        if self.visible:
            pygame.draw.rect(surface, (120, 120, 120), self.rect, 1)

    def __repr__(self):
        return f"<UIElement name={self.name} rect={self.rect} visible={self.visible}>"