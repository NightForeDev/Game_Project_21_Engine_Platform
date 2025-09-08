# engine/ui_manager.py

import pygame
from typing import Callable

class UIManager:
    """
    Manage all UI elements including creation, configuration, state handling,
    and rendering.

    Attributes:
        Class Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        UI Attributes:
            elements (dict[str, UIElement]): Dictionary of UI elements by name.

        State Attributes:
            active (bool): Whether the UIManager is active.

    Methods:
        Configuration:
            _setup(): Initialize and prepare all components.
            load_config(config): Load settings from configuration and initialize attributes.
            create_element(name, element_type, **kwargs): Create and register a new UI element.

        Debug:
            debug(): Print the current internal state for debugging purposes.

        Operations:
            update(): Update all components.
            render(surface): Render all components to the given surface.
    """

    def __init__(self, app_config=None):
        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config if app_config else {}
        self.config = self.app_config.get(self.class_name, {})

        # UI Attributes
        self.elements = {}

        # State Attributes
        self.active = True

        # Initialize
        self._setup()

    """
    Configuration
        _setup
        load_config
        create_element
    """
    def _setup(self):
        """
        Initialize and prepare all components.
        """
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration and initialize attributes.

        Config example:
            {
                "elements": {
                    "title": {"type": "UILabel", "text": "Hello", "x": 10, "y": 10},
                    "start_btn": {"type": "UIButton", "text": "Start", "x": 20, "y": 60}
                }
            }
        """
        if not config:
            return

        for name, element_cfg in config.get("elements", {}).items():
            element_type = element_cfg.get("type", "UIElement")
            self.create_element(name, element_type, **element_cfg)

    def create_element(self, name: str, element_type: str, **kwargs):
        """
        Create and register a new UI element.

        Args:
            name (str): Identifier for the element.
            element_type (str): One of "UIElement", "UILabel", "UIButton".
            **kwargs: forwarded to element constructor.
        """
        element_class = {
            "UIElement": UIElement,
            "UILabel": UILabel,
            "UIButton": UIButton,
        }.get(element_type, UIElement)

        self.elements[name] = element_class(name=name, **kwargs)

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name} Active: {self.active}")
        print(f"Registered Elements: {list(self.elements.keys())}")
        for k, e in self.elements.items():
            print(f"  {k}: {e}")
        print()

    """
    Operations
        update
        render
    """
    def update(self):
        """
        Update all components.
        """
        if not self.active:
            return

        for element in list(self.elements.values()):
            element.update()

    def render(self, surface):
        """
        Render all components.
        """
        if not self.active:
            return

        for element in list(self.elements.values()):
            element.render(surface)


# --------------------------------------------------------------------------
# Base UI Element
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# UI Label
# --------------------------------------------------------------------------
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


# --------------------------------------------------------------------------
# UI Button
# --------------------------------------------------------------------------
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

    def render(self, surface):
        if not self.visible:
            return

        # base background
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
