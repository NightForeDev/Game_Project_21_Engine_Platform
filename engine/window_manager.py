# engine\window_manager.py
import os

import pygame

class WindowManager:
    def __init__(self, app_config):
        class_name = self.__class__.__name__
        self.config = app_config[class_name]

        self.title = self.config["title"]
        self.base_width = self.config["width"]
        self.base_height = self.config["height"]
        self.fullscreen = False
        self.is_maximized = False

        self.flags = pygame.RESIZABLE
        if self.fullscreen:
            self.flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode((self.base_width, self.base_height), self.flags)
        pygame.display.set_caption(self.title)

        self.zoom_level = 1.0
        self.virtual_surface = pygame.Surface((self.base_width, self.base_height))

        test = False
        if test:
            # Common Attributes

            # Set the environment variable to center the game window.
            os.environ['SDL_VIDEO_CENTERED'] = '1'

            # Game Attributes
            self.title = None
            self.game_size = None

            # Display Attributes
            self.screen_info = pygame.display.Info()
            self.screen_scaled = None
            self.screen_gap = None
            self.display_factor = 1
            self.display = pygame.display.set_mode((0, 0), pygame.HIDDEN)
            self.surface = pygame.Surface((0, 0))

            # Flags Attributes
            self.is_fullscreen = None
            self.is_resizable = None
            self.is_maximized = None
            self.flags = None

    def get_size(self):
        return int(self.base_width * self.zoom_level), int(self.base_height * self.zoom_level)

    def set_caption(self, title):
        self.title = title
        pygame.display.set_caption(title)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.base_width, self.base_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.base_width, self.base_height), pygame.RESIZABLE)

    def toggle_maximize_restore(self):
        if self.is_maximized:
            self.restore()
        else:
            self.maximize()

    def maximize(self):
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.RESIZABLE)
        self.is_maximized = True

    def restore(self):
        self.screen = pygame.display.set_mode((self.base_width, self.base_height), pygame.RESIZABLE)
        self.is_maximized = False

    def iconify(self):
        pygame.display.iconify()

    def set_zoom(self, zoom_level):
        self.zoom_level = zoom_level

    def render(self, render_func):
        render_func(self.virtual_surface)

        if self.zoom_level != 1.0:
            scaled_surface = pygame.transform.smoothscale(
                self.virtual_surface,
                (int(self.base_width * self.zoom_level), int(self.base_height * self.zoom_level))
            )
            self.screen.blit(scaled_surface, (0, 0))
        else:
            self.screen.blit(self.virtual_surface, (0, 0))

        pygame.display.flip()
