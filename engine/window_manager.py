# engine\window_manager.py

import ctypes
import os
import sys
import pygame
from engine.base_manager import BaseManager

SW_MAXIMIZE = 3
SW_RESTORE = 9

class WindowManager(BaseManager):
    """
    Manage window and rendering surface.

    Attributes:
        Time Attributes:
            clock (pygame.time.Clock): Optional clock for FPS display.

        Caption Attributes:
            tag (str): Optional pre-title label.
            title (str): Window title.
            version (str): Application version string.
            display_tag (bool): Whether to display the tag.
            display_version (bool): Whether to display the version.
            display_fps (bool): Whether to display FPS in caption.

        Flag Attributes:
            flags (int): Current Pygame display flags.
            maximized (bool): Whether the window is maximized.
            resizable (bool): Whether the window is resizable.
            borderless (bool): Whether the window is borderless.
            fullscreen (bool): Whether fullscreen mode is active.

        Size Attributes:
            render_size (tuple[int, int]): Logical size for rendering content.
            scaled_size (tuple[int, int]): Scaled size of the content on screen.
            windowed_size (tuple[int, int]): Size of the actual window in windowed mode.

        Surface Attributes:
            render_surface (pygame.Surface): Surface where all drawing occurs.
            display_surface (pygame.Surface): Surface displayed on the window.
            display_gap (tuple[int, int]): Gap for centering content when scaled.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.
            _apply_surface_sizes(): Apply current render and scaled sizes.
            set_caption(tag, title, version, display_tag, display_version, display_fps): Sets the window caption.
            set_flags(resizable, borderless, fullscreen): Sets the display surface flags.
            set_render_size(width, height): Sets the render surface size.
            set_scaled_size(width, height): Sets the scaled surface size.

        Resizing & Scaling:
            _detect_maximized(): Detects if the window is maximized.
            _calculate_aspect_ratio_fit(reference_size, target_size): Fits target size while preserving aspect ratio.
            _adjust_scaled_size(): Adjusts scaled surface size.
            _adjust_windowed_size(): Adjusts windowed surface size.
            _adjust_maximized(): Adjusts scaled surface and center content for maximized windows.
            resize(): Handles window resizing event and update surfaces.

        State Management:
            _compute_flags(): Computes pygame display flags from current state.
            _restore_window(): Restores the window from maximized state.
            _maximize_window(): Maximizes the window.
            toggle_maximized(): Toggles between maximized and restored states.
            toggle_borderless(): Toggles borderless window mode.
            toggle_resizable(): Toggles resizable window mode.
            toggle_fullscreen(): Toggles fullscreen window mode.

        Debug:
            debug(): Print debug information.

        Operations:
            _update_caption(): Updates the window caption.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, core_manager=None, app_config=None, clock=None):
        # Time Attributes
        self.clock = clock

        # Caption Attributes
        self.tag = None
        self.version = None
        self.title = None
        self.display_tag = None
        self.display_version = None
        self.display_fps = None

        # Flag Attributes
        self.flags = None
        self.maximized = None
        self.resizable = None
        self.borderless = None
        self.fullscreen = None

        # Size Attributes
        self.render_size = None
        self.scaled_size = None
        self.windowed_size = None

        # Surface Attributes
        self.render_surface = None
        self.display_surface = None
        self.display_gap = None

        # Initialize BaseManager and components
        super().__init__(core_manager, app_config)

    """
    Configuration
        _setup
        load_config
        _apply_surface_sizes
        set_caption
        set_flags
        set_render_size
        set_scaled_size
    """
    def _setup(self):
        """
        Initialize components.
        """
        # Set environment variable to center the game window
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialize attributes
        self.flags = 0

        # Load configuration
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration.
        """
        # Early return if action is not applicable
        if config is None:
            return

        # Apply configuration values
        self.set_caption(config['tag'], config['title'], config['version'], config['display_tag'], config['display_version'], config['display_fps'])
        self.set_render_size(config['render_width'], config['render_height'])
        self.set_scaled_size(config['scaled_width'], config['scaled_height'])
        self.toggle_resizable(config['resizable'])
        self.toggle_borderless(config['borderless'])
        self.toggle_fullscreen(config['fullscreen'])

    def _apply_surface_sizes(self):
        """
        Apply current render and scaled sizes
        """
        # Early return if either size is missing
        if not self.render_size or not self.scaled_size:
            return

        # Apply new settings
        self.render_surface = pygame.Surface(self.render_size)
        self.display_surface = pygame.display.set_mode(self.scaled_size, self.flags)
        self.resize()

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

        # Apply new settings
        self._update_caption()

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

        # Apply new settings
        self._apply_surface_sizes()

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

        # Apply new settings
        self._apply_surface_sizes()

    """
    Resizing & Scaling
        _detect_maximized
        _calculate_aspect_ratio_fit
        _adjust_scaled_size
        _adjust_windowed_size
        _adjust_maximized
        resize
    """
    def _detect_maximized(self):
        """
        Detects if the window is maximized.
        """
        # Get the primary monitor size (desktop resolution)
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]

        # Get current window size
        window_width, window_height = pygame.display.get_window_size()

        # Determine if the window is maximized
        height_threshold = 0.90 * desktop_height

        # Update maximized state
        self.maximized = window_width == desktop_width and window_height >= height_threshold

    @staticmethod
    def _calculate_aspect_ratio_fit(reference_size, target_size):
        """
        Fits target size while preserving aspect ratio.
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

    def _adjust_scaled_size(self):
        """
        Adjusts scaled surface size.
        """
        # Get render and display surface sizes
        render_size = self.render_surface.get_size()
        display_size = self.display_surface.get_size()

        # Adjust scaled surface while preserving the render surface aspect ratio
        self.scaled_size = self._calculate_aspect_ratio_fit(render_size, display_size)

    def _adjust_windowed_size(self):
        """
        Adjusts the windowed surface size.
        """
        # Compute windowed dimensions including display gaps
        window_width = self.scaled_size[0] + self.display_gap[0] * 2
        window_height = self.scaled_size[1] + self.display_gap[1] * 2
        self.windowed_size = window_width, window_height

    def _adjust_maximized(self):
        """
        Adjusts scaled surface and center content for maximized windows.
        """
        # Get current window size
        window_width, window_height = pygame.display.get_window_size()

        # Adjust scaled surface to fit the window while preserving aspect ratio
        self._adjust_scaled_size()

        # Center content by setting gaps
        gap_x = (window_width - self.scaled_size[0]) // 2
        gap_y = (window_height - self.scaled_size[1]) // 2
        self.display_gap = gap_x, gap_y

        # Clear display surface
        self.display_surface.fill((0, 0, 0))

    def resize(self):
        """
        Handles window resizing event and update surfaces.
        """
        # Detect if the window is currently maximized
        self._detect_maximized()

        if self.maximized or self.borderless:
            # Adjust scaled surface and center content
            self._adjust_maximized()

        elif not self.fullscreen:
            # Reset centering gaps for windowed mode
            self.display_gap = (0, 0)

            # Adjust scaled surface to fit the window while preserving aspect ratio
            self._adjust_scaled_size()

            # Update windowed size to match scaled content and gaps
            self._adjust_windowed_size()

            # Apply updated windowed size to the display surface
            self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

    """
    State Management
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
        Computes pygame display flags from current state.

        Returns:
            flags (int): Bitmask of Pygame display flags
        """
        # Start with no flags set
        flags = 0

        # Add flags according to window state
        if self.borderless:
            flags |= pygame.NOFRAME
        if self.resizable and not self.fullscreen:
            flags |= pygame.RESIZABLE
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

    def toggle_maximized(self):
        """
        Toggles between maximized and restored states.
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

    def toggle_borderless(self, state=None):
        """
        Toggles borderless window mode.

        Args:
            state (bool, optional): True to enable, False to disable, None to toggle.
        """
        # Early return if action is not applicable
        if state is not None and state == self.borderless or not self.resizable:
            return

        # Restore to apply new flags correctly
        hwnd = pygame.display.get_wm_info()['window']
        is_maximized = ctypes.windll.user32.IsZoomed(hwnd)
        if is_maximized:
            self._restore_window()

        # Update Pygame display flags
        self.borderless = not self.borderless if state is None else state
        self.fullscreen = False
        self.flags = self._compute_flags()
        self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

        # Maximize to apply borderless fullscreen
        if self.borderless:
            self._maximize_window()

    def toggle_resizable(self, state=None):
        """
        Toggles resizable window mode.

        Args:
            state (bool, optional): True to enable, False to disable, None to toggle.
        """
        # Early return if action is not applicable
        if state is not None and state == self.resizable or self.maximized or self.fullscreen:
            return

        # Update Pygame display flags
        self.resizable = not self.resizable if state is None else state
        self.flags = self._compute_flags()
        self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

    def toggle_fullscreen(self, state=None):
        """
        Toggles fullscreen window mode.

        Args:
            state (bool, optional): True to enable, False to disable, None to toggle.
        """
        # Early return if action is not applicable
        if state is not None and state == self.fullscreen:
            return

        # Update Pygame display flags
        self.fullscreen = not self.fullscreen if state is None else state
        self.borderless = False
        self.flags = self._compute_flags()

        if self.fullscreen:
            # Get sizes for fullscreen scaling
            render_size = self.render_surface.get_size()
            display_size = pygame.display.get_desktop_sizes()[0]

            # Compute target size preserving aspect ratio
            target_size = self._calculate_aspect_ratio_fit(render_size, display_size)

            # Apply fullscreen display mode
            self.display_surface = pygame.display.set_mode(target_size, self.flags)

            # Reset display gap and adjust content scaling
            self.display_gap = (0, 0)
            self._adjust_scaled_size()
        else:
            # Restore windowed display mode
            self.display_surface = pygame.display.set_mode(self.windowed_size, self.flags)

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
        print(f"render_size={self.render_size}")
        print(f"scaled_size={self.scaled_size}")
        print(f"windowed_size={self.windowed_size}")
        print(f"display_surface_size={self.display_surface.get_size()}")
        print(pygame.display.get_surface().get_size())
        print(pygame.display.get_window_size())
        print(pygame.display.Info().current_w, pygame.display.Info().current_h)
        print(pygame.display.get_desktop_sizes())
        print()

    """
    Operations
        _update_caption
        update
        render
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

    def update(self, dt=None):
        """
        Update components.
        """
        if self.display_fps and self.clock:
            self._update_caption()

    def render(self, surface=None):
        """
        Render components.
        """
        scaled_surface = pygame.transform.scale(self.render_surface, self.scaled_size)
        self.display_surface.blit(scaled_surface, self.display_gap)
        pygame.display.flip()
