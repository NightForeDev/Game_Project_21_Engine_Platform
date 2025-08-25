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
        self.borderless = None
        self.fullscreen = None

        # Size Attributes
        self.render_size = None
        self.scaled_size = None
        self.windowed_size = None

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
        self.set_flags(self.config['resizable'], self.config['borderless'], self.config['fullscreen'])
        self.set_render_size(self.config['render_width'], self.config['render_height'])
        self.set_scaled_size(self.config['scaled_width'], self.config['scaled_height'])
        self.windowed_size = self.scaled_size
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
    """
    def set_flags(self, resizable=None, borderless=None, fullscreen=None):
        """
        Sets the display surface flags.

        Args:
            resizable (bool): Enable or disable window resizing
            borderless (bool): Enable or disable borderless mode
            fullscreen (bool): Enable or disable fullscreen mode
        """
        # Update flag state
        if resizable is not None:
            self.resizable = resizable
        if borderless is not None:
            self.borderless = borderless
        if fullscreen is not None:
            self.fullscreen = fullscreen

        # Compute Pygame flags
        self.flags = self._compute_flags()

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
    @staticmethod
    def _calculate_aspect_ratio_fit(reference_size, target_size):
        """
        Calculates the largest size that fits within the target while preserving the aspect ratio of the reference.
        """
        # Unpack the reference and target sizes
        ref_w, ref_h = reference_size
        tgt_w, tgt_h = target_size

        # Calculate relative change per dimension
        delta_w = abs(1 - tgt_w / ref_w)
        delta_h = abs(1 - tgt_h / ref_h)

        # Choose the scaling factor based on the more restrictive dimension
        if delta_w < delta_h:
            # Scale height to match width
            scale_factor = tgt_w / ref_w
            return tgt_w, int(ref_h * scale_factor)
        else:
            # Scale width to match height
            scale_factor = tgt_h / ref_h
            return int(ref_w * scale_factor), tgt_h

    def adjust_aspect_ratio(self):
        """
        Adjusts the scaled surface size to maintain the render aspect ratio.
        """
        # Get current display and render sizes
        display_size = self.display_surface.get_size()
        render_size = self.render_surface.get_size()

        # Compute scaled dimensions that maintain aspect ratio
        self.scaled_size = self._calculate_aspect_ratio_fit(render_size, display_size)

    def adjust_display_size(self):
        """
        Adjusts the display surface size based on the scaled size and display gaps.
        """
        # Calculate display dimensions
        display_w = self.scaled_size[0] + self.display_gap[0] * 2
        display_h = self.scaled_size[1] + self.display_gap[1] * 2
        self.windowed_size = display_w, display_h

    def _detect_maximized(self):
        """
        Detect whether the window is currently maximized.
        """
        # Get the primary monitor size (desktop resolution)
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]

        # Get current window size
        window_width, window_height = pygame.display.get_window_size()

        # Determine if the window is maximized
        height_threshold = 0.90 * desktop_height

        # Update maximized state
        self.maximized = window_width == desktop_width and window_height >= height_threshold

    def adjust_maximized(self):
        """
        Adjust the scaled content for a maximized window.
        """
        # Get current window size
        window_width, window_height = pygame.display.get_window_size()

        # Update scaled size to fit the window while maintaining render aspect ratio
        self.set_scaled_size(window_width, window_height)
        self.adjust_aspect_ratio()

        # Center content by setting gaps
        gap_x = (window_width - self.scaled_size[0]) // 2
        gap_y = (window_height - self.scaled_size[1]) // 2
        self.display_gap = gap_x, gap_y

        # Clear display surface
        self.display_surface.fill((0, 0, 0))

    def resize(self):
        self._detect_maximized()

        if self.maximized or self.borderless:
            self.adjust_maximized()
        else:
            self.display_gap = (0, 0)

            # Adjust aspect ratio based on current display size
            self.adjust_aspect_ratio()

            # Adjust the display based on new settings
            self.adjust_display_size()

            # Updates the display surface with the adjusted dimensions
            self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)

    """
    Window State Management
        _compute_flags
        _restore_window
        _maximize_window
        toggle_maximized
        toggle_borderless
        toggle_resizable
        toggle_fullscreen
    """
    def _compute_flags(self):
        """
        Computes the Pygame display flags based on current state.

        Returns:
            flags (int): Bitmask of Pygame display flags
        """
        # Start with no flags set
        flags = 0

        # Add flags according to window state
        if self.resizable and not self.fullscreen:
            flags |= pygame.RESIZABLE
        if self.borderless:
            flags |= pygame.NOFRAME
        if self.fullscreen:
            flags |= pygame.FULLSCREEN

        return flags

    def _restore_window(self):
        """
        Restores the window from maximized state.
        """
        self.maximized = False
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, SW_RESTORE)

    def _maximize_window(self):
        """
        Maximizes the window to fill the screen.
        """
        self.maximized = True
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)

    def toggle_resizable(self):
        """
        Toggles resizable window mode.
        """
        # Update Pygame display flags
        self.resizable = not self.resizable
        self.flags = self._compute_flags()
        self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)

    def toggle_borderless(self):
        """
        Toggles borderless window mode.
        """
        # Early return if action is not applicable
        if not self.resizable:
            return

        # Restore maximized state to apply NOFRAME properly
        hwnd = pygame.display.get_wm_info()['window']
        is_maximized = ctypes.windll.user32.IsZoomed(hwnd)
        if is_maximized:
            self._restore_window()

        # Update Pygame display flags
        self.borderless = not self.borderless
        self.fullscreen = False
        self.flags = self._compute_flags()
        self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

        # Maximize if borderless to apply borderless fullscreen
        if self.borderless:
            self._maximize_window()

    def toggle_maximized(self):
        """
        Toggle between maximized and restored states.
        """
        # Early return if action is not applicable
        if not self.resizable or self.borderless or self.fullscreen:
            return

        # Toggle maximize/restore state
        if sys.platform.startswith("win"):
            # Get native window handle
            hwnd = pygame.display.get_wm_info()['window']

            # Check if the window is currently maximized
            is_maximized = ctypes.windll.user32.IsZoomed(hwnd)

            if is_maximized:
                # Restore the window
                self._restore_window()
            else:
                # Maximize the window
                self._maximize_window()

    def toggle_fullscreen(self):
        """
        Toggles fullscreen window mode.
        """
        # Update Pygame display flags
        self.fullscreen = not self.fullscreen
        self.borderless = False
        self.flags = self._compute_flags()

        if self.fullscreen:
            render_size = self.render_surface.get_size()
            display_size = pygame.display.get_desktop_sizes()[0]
            target_size = self._calculate_aspect_ratio_fit(render_size, display_size)
            self.display_gap = (0, 0)
            self.display_surface = pygame.display.set_mode(target_size, self.flags)
            self.adjust_aspect_ratio()
        else:
            self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

    def debug(self):
        print(self.render_size)
        print(self.scaled_size)
        print(self.windowed_size)
        print(self.display_surface.get_size())
        print(pygame.display.get_surface().get_size())
        print(pygame.display.get_window_size())
        print(pygame.display.Info().current_w, pygame.display.Info().current_h)
        print(pygame.display.get_desktop_sizes())
        print()

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

    def render(self):
        """
        Renders surface
        """
        scaled_surface = pygame.transform.scale(self.render_surface, self.scaled_size)
        self.display_surface.blit(scaled_surface, self.display_gap)
        pygame.display.flip()
