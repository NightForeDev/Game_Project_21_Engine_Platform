# engine\window_manager.py

import ctypes
import os
import sys
import pygame

SW_MAXIMIZE = 3
SW_RESTORE = 9

class WindowManager:
    """
    WindowManager handles Pygame window creation, configuration, and state

    Attributes:
        Class Attributes:
            class_name (str): Name of the class
            config (dict): Loaded configuration dictionary
            clock (pygame.time.Clock): Pygame clock instance

        Caption Attributes:
            tag (str): Pre-title label
            title (str): Window title
            version (str): Application version
            display_tag (bool): Whether to show the tag
            display_version (bool): Whether to show the version
            display_fps (bool): Whether to show the FPS

        Flags Attributes:
            resizable (bool): Whether window is resizable
            fullscreen (bool): Whether fullscreen mode is active

        Size Attributes:

        Window Attributes:
            flags (int): Bitmask of Pygame display flags
            maximized (bool): Whether window is maximized
            render_surface (pygame.Surface): Rendering surface used for drawing.
            display_surface (pygame.Surface): Display surface shown on the window.

        Debug Attributes:
            display_gap (tuple): Gaps from scaling

    Methods:
        Configuration:
            _load_config: Loads configuration from a dictionary
            set_caption: Sets the window caption
            set_render_size: Sets the render surface size
            set_scaled_size: Sets the scaled surface size

        State Management:
            _compute_flags: Computes the Pygame display flags based on current state
            set_flags: Sets the display surface flags
            toggle_resizable: Toggles resizable flag
            toggle_fullscreen: Toggles fullscreen flag
            toggle_maximize_restore: Toggles between maximized and restored window states

        Operations:
            _update_caption: Updates the window caption
            _update_window: Updates the window surface
            resize: Resizes the window to the specified dimensions

        Main Loop:
            update: Updates state
            render: Renders surface
    """
    def __init__(self, app_config, clock=None):
        # Class Attributes
        self.class_name = self.__class__.__name__
        self.config = app_config[self.class_name]
        self.clock = clock

        # Caption Attributes
        self.tag = None
        self.version = None
        self.title = None
        self.display_tag = None
        self.display_version = None
        self.display_fps = None

        # Flags Attributes
        self.resizable = None
        self.fullscreen = None

        # Size Attributes
        self.render_size = None
        self.scaled_size = None
        self.display_size = None

        # Window Attributes
        self.flags = None
        self.maximized = None
        self.render_surface = None
        self.display_surface = None

        # Debug Attributes
        self.display_gap = (0, 0)
        self.scale_factor = None

        # Set the environment variable to center the game window.
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialize
        self._load_config()

    """
    Configuration
        _load_config
        set_caption
        set_render_size
        set_scaled_size
    """
    def _load_config(self):
        """
        Loads configuration from a dictionary
        """
        self.set_caption(self.config['tag'], self.config['title'], self.config['version'], self.config['display_tag'], self.config['display_version'], self.config['display_fps'])
        self.set_flags(self.config['resizable'], self.config['fullscreen'])
        self.set_render_size(self.config['render_width'], self.config['render_height'])
        self.set_scaled_size(self.config['scaled_width'], self.config['scaled_height'])
        self._update_surface()

    def set_caption(self, tag=None, title=None, version=None, display_tag=None, display_version=None, display_fps=None):
        """
        Sets the window caption.

        Args:
            tag (str): Pre-title label
            title (str): Window title
            version (str): Application version
            display_tag (bool): Whether to show the tag
            display_version (bool): Whether to show the version
            display_fps (bool): Whether to show the FPS
        """
        # Early return if action is not applicable
        if tag is None and title is None and version is None and display_tag is None and display_version is None and display_fps is None:
            return

        # Update caption attributes
        if tag is not None:
            self.tag = tag
        if title is not None:
            self.title = title
        if version is not None:
            self.version = version
        if display_tag is not None:
            self.display_tag = display_tag
        if display_version is not None:
            self.display_version = display_version
        if display_fps is not None:
            self.display_fps = display_fps

    def set_render_size(self, width=None, height=None):
        """
        Sets the render surface size.

        Args:
            width (int): Width of the render surface in pixels. If None, keeps current width.
            height (int): Height of the render surface in pixels. If None, keeps current height.
        """
        # Early return if action is not applicable
        if width is None and height is None:
            return

        # Use current size if not provided
        width = width or self.render_size[0]
        height = height or self.render_size[1]

        # Update surface size
        self.render_size = width, height

    def set_scaled_size(self, width=None, height=None):
        """
        Sets the scaled surface size.

        Args:
            width (int): Width of the scaled surface in pixels. If None, keeps current width.
            height (int): Height of the scaled surface in pixels. If None, keeps current height.
        """
        # Early return if action is not applicable
        if width is None and height is None:
            return

        # Use current size if not provided
        width = width or self.scaled_size[0]
        height = height or self.scaled_size[1]

        # Update surface size
        self.scaled_size = width, height

    """
    State Management
        _compute_flags
        set_flags
        toggle_resizable
        toggle_fullscreen
        toggle_maximize_restore
    """
    def _compute_flags(self):
        """
        Computes the Pygame display flags based on current state.

        Returns:
            flags (int): Bitmask of Pygame display flags
        """
        # Initialize flags
        flags = 0

        # Resizable flag
        if self.resizable and not self.fullscreen:
            flags |= pygame.RESIZABLE

        # Fullscreen flag
        if self.fullscreen:
            flags |= pygame.FULLSCREEN

        # Return Pygame flags
        return flags

    def set_flags(self, resizable=None, fullscreen=None):
        """
        Sets the display surface flags.

        Args:
            resizable (bool): Enable or disable window resizing
            fullscreen (bool): Enable or disable fullscreen mode
        """
        # Update flag state
        if resizable is not None:
            self.resizable = resizable
        if fullscreen is not None:
            self.fullscreen = fullscreen

        # Compute Pygame flags
        self.flags = self._compute_flags()

    def toggle_resizable(self):
        """
        Toggles resizable flag.
        """
        # Flip flag state
        self.resizable = not self.resizable

        # Update flags
        self.flags = self._compute_flags()

        # Apply new flag
        self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)

    def toggle_fullscreen(self):
        """
        Toggles fullscreen flag.
        """
        # Flip flag state
        self.fullscreen = not self.fullscreen

        # Update flags
        self.flags = self._compute_flags()

        # Apply new flag
        self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)

    def toggle_maximize_restore(self):
        """
        Toggles between maximized and restored window states.
        """
        # Early return if action is not applicable
        if not self.resizable or self.fullscreen:
            return

        # Windows-specific maximize/restore
        if sys.platform.startswith("win"):
            # Get native window handle
            hwnd = pygame.display.get_wm_info()['window']

            # Check if the window is currently maximized
            is_maximized = ctypes.windll.user32.IsZoomed(hwnd)

            if is_maximized:
                # Restore window
                self.maximized = False
                ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)
            else:
                # Maximize the window
                self.maximized = True
                ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)

    """
    Operations
        _update_caption
        _update_surface
        resize
    """
    def _update_caption(self):
        """
        Updates the window caption.
        """
        parts = []

        # Optional tag display
        if self.display_tag and self.tag:
            parts.append(f"{self.tag}")

        # Window title
        parts.append(self.title)

        # Optional version display
        if self.display_version and self.version:
            parts.append(f"{self.version}")

        # Optional FPS display
        if self.display_fps and self.clock:
            parts.append(f"({int(self.clock.get_fps())} FPS)")

        # Update new caption
        pygame.display.set_caption(" ".join(parts))

    def _update_surface(self):
        """
        Updates the display surface.
        """
        self.render_surface = pygame.Surface((self.render_size[0], self.render_size[1]))
        self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)

    """
    WIP
        get_size
    """
    def adjust_scaled_size(self):
        """
        Adjusts the scaled surface size to maintain the render aspect ratio.
        """
        # Get the surface sizes
        ds_w, ds_h = self.display_surface.get_size()
        rs_w, rs_h = self.render_surface.get_size()

        # Calculate relative change per dimension
        delta_w = abs(1 - ds_w / rs_w)
        delta_h = abs(1 - ds_h / rs_h)

        # Adjust scaled surface size to maintain aspect ratio
        if delta_w < delta_h:
            # Adjust height based on width change
            self.scale_factor = ds_w / rs_w
            self.scaled_size = ds_w, int(rs_h * self.scale_factor)
        else:
            # Adjust width based on height change
            self.scale_factor = ds_h / rs_h
            self.scaled_size = int(rs_w * self.scale_factor), ds_h

    def adjust_display_size(self):
        """
        Adjusts the display surface size based on the scaled size and display gaps.
        """
        # Calculate display dimensions
        display_w = self.scaled_size[0] + self.display_gap[0] * 2
        display_h = self.scaled_size[1] + self.display_gap[1] * 2
        self.display_size = display_w, display_h

    def resize(self):
        """
        """
        if not self.maximized:
            # Adjust aspect ratio based on current display size
            self.adjust_scaled_size()

            # Adjust the display based on new settings
            self.adjust_display_size()

            # Updates the display surface with the adjusted dimensions
            self.display_surface = pygame.display.set_mode(self.display_size, self.flags)

    def get_size(self):
        return self.render_size[0], self.render_size[1]

    """
    Main Loop
        update
        render
    """
    def update(self):
        """
        Updates state.
        """
        if self.display_fps and self.clock:
            self._update_caption()

    def render(self, render_func):
        """
        Renders surface
        """
        render_func(self.render_surface)
        render_surface_scaled = pygame.transform.scale(self.render_surface, self.scaled_size)

        self.display_surface.blit(render_surface_scaled, (0, 0))

        pygame.display.flip()
