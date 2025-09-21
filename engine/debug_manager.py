# engine\debug_manager.py

import pygame
from engine.base_manager import BaseManager
from .draw_utils import draw_text

class DebugManager(BaseManager):
    """
    Manage debug overlay, diagnostics, and performance metrics.

    Constants:
        FONT_NAME (str): Default font used for debug text.
        FONT_SIZE (int): Default font size.

    Attributes:
        State Attributes:
            visible (bool): Whether the debug overlay is visible.

        Debug Attributes:
            dt (float): Delta time of the last frame.
            fps (float): Current frames per second.

        Render Attributes:
            font (pygame.font.Font | None): Font object for rendering text.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        State Management:
            toggle(): Toggle visibility of the debug overlay.

        Debug:
            debug(): Print debug information.

        Operations:
            update(dt): Update performance metrics.
            render(surface): Render debug overlay to the surface.
    """
    # Constants
    FONT_NAME = "Consolas"
    FONT_SIZE = 16

    def __init__(self, core_manager=None, app_config=None):
        # Debug Attributes
        self.visible = False
        self.fps = None
        self.dt = None
        self.font = None

        # Initialize BaseManager and components
        super().__init__(core_manager, app_config)

    """
    Configuration
        _setup
        load_config
    """
    def _setup(self):
        """
        Initialize components.
        """
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration.
        """
        # Early return if action is not applicable
        if config is None:
            return

        # Apply configuration values
        self.font = pygame.font.SysFont(self.FONT_NAME, self.FONT_SIZE)
        self.visible = config.get("visible", self.visible)

    """
    State Management
        toggle
    """
    def toggle(self):
        """
        Toggle visibility of the debug overlay.
        """
        self.visible = not self.visible

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
        print(f"Visible: {self.visible}")
        print(f"FPS: {self.fps:.1f}")
        print()

    """
    Operations
        update
        render
    """
    def update(self, dt=None):
        """
        Update components.
        """
        # Update debug attributes
        self.dt = dt
        self.fps = self.core_manager.clock.get_fps()

    def render(self, surface=None):
        """
        Render components.
        """
        # Early return if not applicable
        if not self.visible:
            return

        # Collect overlay lines
        lines = [
            f"FPS: {self.fps:.1f}",
            f"Delta Time: {int(self.dt * 1000)} ms",
            f"Scene: {type(self.scene_manager.current_scene).__name__}",
            f"Render Size: {self.window_manager.render_size}",
            f"Scaled Size: {self.window_manager.scaled_size}",
            f"Windowed Size: {self.window_manager.windowed_size}",
        ]

        # Draw overlay text
        for i, line in enumerate(lines):
            draw_text(surface, line, (10, 10 + i * 20), font=self.font)
