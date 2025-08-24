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
            version (str): Application version
            title (str): Window title
            display_version (bool): Show version in caption
            display_fps (bool): Show FPS in caption

        Flags Attributes:
            resizable (bool): Whether window is resizable
            fullscreen (bool): Whether fullscreen mode is active

        Size Attributes:
            base_width (int): Base width in pixels
            base_height (int): Base height in pixels
            width (int): Current window width
            height (int): Current window height

        Display Attributes:
            aspect_ratio (float): Base aspect ratio
            scale_w (float): Horizontal scaling factor
            scale_h (float): Vertical scaling factor

        Window Attributes:
            flags (int): Current Pygame display flags
            maximized (bool): Whether window is maximized
            render_surface (pygame.Surface): Rendering surface used for drawing.
            window_surface (pygame.Surface): Display surface shown on the window.

        Debug Attributes:
            screen_info (pygame.display.Info): Monitor info
            screen_scaled (tuple): Scaled screen size
            screen_gap (tuple): Gaps from scaling

    Methods:
        Configuration:
            _load_config: Loads configuration from a dictionary
            set_caption: Sets the window caption
            set_base_size: Sets the base size
            set_window_size: Sets the window size

        State Management:
            _compute_flags: Computes the Pygame display flags based on current state
            set_flags: Sets the window flags
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
        self.version = None
        self.title = None
        self.display_version = None
        self.display_fps = None

        # Flags Attributes
        self.resizable = None
        self.fullscreen = None

        # Size Attributes
        self.base_width = None
        self.base_height = None
        self.width = None
        self.height = None

        # Display Attributes
        self.aspect_ratio = None
        self.scale_w = None
        self.scale_h = None

        # Window Attributes
        self.flags = None
        self.maximized = None
        self.render_surface = None
        self.window_surface = None

        # Debug Attributes
        self.screen_info = pygame.display.Info()
        self.screen_scaled = None
        self.screen_gap = (0, 0)
        self.scale_factor = None

        # Set the environment variable to center the game window.
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialize
        self._load_config()
    """
    Configuration
        _load_config
        set_caption
        set_base_size
        set_window_size
    """
    def _load_config(self):
        """
        Loads configuration from a dictionary
        """
        self.set_caption(self.config['version'], self.config['title'], self.config['display_version'], self.config['display_fps'])
        self.set_flags(self.config['resizable'], self.config['fullscreen'])
        self.set_base_size(self.config['base_width'], self.config['base_height'])
        self.set_window_size(self.config['width'], self.config['height'])
        self.window_surface = pygame.display.set_mode((self.width, self.height), self.flags)

    def set_caption(self, version=None, title=None, display_version=None, display_fps=None):
        """
        Sets the window caption.

        Args:
            version (str): App version
            title (str): Window title
            display_version (bool): Show version
            display_fps (bool): Show FPS
        """
        # Early return if action is not applicable
        if title is None and version is None and display_version is None and display_fps is None:
            return

        # Update caption
        if title is not None:
            self.title = title
        if version is not None:
            self.version = version
        if display_version is not None:
            self.display_version = display_version
        if display_fps is not None:
            self.display_fps = display_fps

        # Apply the new caption
        self._update_caption()

    def set_base_size(self, width=None, height=None):
        """
        Sets the base size.

        Args:
            width (int): Base width in pixels
            height (int): Base height in pixels
        """
        # Early return if action is not applicable
        if width is None and height is None:
            return

        # Update base size
        if width is not None:
            self.base_width = width
        if height is not None:
            self.base_height = height

        # Update aspect ratio
        self.aspect_ratio = self.base_width / self.base_height

        # Apply the new base size
        self.set_window_size(self.width, self.height, keep_aspect_ratio=True)

    def set_window_size(self, width=None, height=None, keep_aspect_ratio=True):
        """
        Sets the window size.

        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
            keep_aspect_ratio (bool): Maintain the base aspect ratio
        """
        # Early return if action is not applicable
        if width is None and height is None:
            return

        # Calculate size based on aspect ratio
        if keep_aspect_ratio:
            # Calculate height (Width provided)
            if width is not None and height is None:
                height = int(width / self.aspect_ratio)

            # Calculate width (Height provided)
            elif height is not None and width is None:
                width = int(height * self.aspect_ratio)

            # Scale to fit (Both provided)
            elif width is not None and height is not None:
                scale_w = width / self.base_width
                scale_h = height / self.base_height

                if scale_w < scale_h:
                    height = int(self.base_height * scale_w)
                else:
                    width = int(self.base_width * scale_h)

        # Update window size
        self.width = width
        self.height = height

        # Apply the new window size
        self._update_surface()

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
        Sets the window flags.

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
        self.window_surface = pygame.display.set_mode((self.width, self.height), self.flags)

    def toggle_fullscreen(self):
        """
        Toggles fullscreen flag.
        """
        # Flip flag state
        self.fullscreen = not self.fullscreen

        # Update flags
        self.flags = self._compute_flags()

        # Apply new flag
        self.window_surface = pygame.display.set_mode((self.width, self.height), self.flags)

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
        _update_window
        resize
    """
    def _update_caption(self):
        """
        Updates the window caption.
        """
        parts = []

        # Optional version display
        if self.display_version and self.version:
            parts.append(f"[{self.version}]")

        # Window title
        parts.append(self.title)

        # Optional FPS display
        if self.display_fps and self.clock:
            parts.append(f"({int(self.clock.get_fps())} FPS)")

        # Update new caption
        pygame.display.set_caption(" ".join(parts))

    def _update_surface(self):
        """
        Updates the window surface.
        """
        self.render_surface = pygame.Surface((self.base_width, self.base_height))
        self.window_surface = pygame.display.set_mode((self.width, self.height), self.flags)

    """
    WIP
        get_size
    """
    def adjust_window_surface(self):
        """
        Adjust the window display based on current settings.
        """
        # Calculate screen dimensions
        screen_w = self.width + self.screen_gap[0] * 2
        screen_h = self.height + self.screen_gap[1] * 2
        screen_size = screen_w, screen_h

        # Set the display mode with the calculated dimensions and provided flags.
        self.window_surface = pygame.display.set_mode(screen_size, self.flags)

    def adjust_aspect_ratio(self):
        """
        Adjust size to maintain aspect ratio.
        """
        # Get the surface sizes
        ws_w, ws_h = self.window_surface.get_size() if self.window_surface else (self.base_width, self.base_height)
        rs_w, rs_h = self.render_surface.get_size() if self.render_surface else (self.width, self.height)

        # Calculate relative change per dimension
        delta_w = abs(1 - ws_w / rs_w)
        delta_h = abs(1 - ws_h / rs_h)

        # Adjust window size to maintain aspect ratio
        if delta_w < delta_h:
            # Adjust height based on width change
            self.scale_factor = ws_w / rs_w
            self.width, self.height = ws_w, int(rs_h * self.scale_factor)
        else:
            # Adjust width based on height change
            self.scale_factor = ws_h / rs_h
            self.width, self.height = int(rs_w * self.scale_factor), ws_h

    def resize(self):
        """
        Resize the window while considering maximize and screen width.
        """
        if not self.maximized:
            # Adjust aspect ratio based on current display size
            self.adjust_aspect_ratio()

            # Adjust the display based on new settings
            self.adjust_window_surface()

    def get_size(self):
        return self.base_width, self.base_height

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
        render_surface_scaled = pygame.transform.scale(self.render_surface, (self.width, self.height))

        self.window_surface.blit(render_surface_scaled, (0, 0))

        pygame.display.flip()
