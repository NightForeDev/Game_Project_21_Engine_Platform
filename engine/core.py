# engine\core.py

import random
import pygame

from engine.config_loader import load_config
from engine.debug import Debug
from engine.window_manager import WindowManager
from engine.input_manager import InputManager

class Core:
    def __init__(self, initial_scene_class):
        """Set up the game."""
        # Initialize pygame and random seed
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

        # Common Attributes
        self.app_config = load_config()
        self.config = self.app_config[self.__class__.__name__]

        # Time Management Attributes
        self.fps = self.config["fps"]
        self.total_play_time = 0
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps) / 1000

        # Manager Attributes
        self.debug = Debug(self)
        self.window_manager = WindowManager(self.app_config)
        self.input_manager = InputManager()

        # Class Attributes
        self.running = True
        self.current_scene = None
        self.previous_scene = None

        # Class Initialization
        self.register_shortcuts()
        self.current_scene = initial_scene_class(self)

    def register_shortcuts(self):
        """Bind system keys."""
        self.input_manager.bind_key_down_global(pygame.K_ESCAPE, self.quit_game)
        self.input_manager.bind_key_down_global(pygame.K_F1, self.debug.toggle)
        self.input_manager.bind_key_down_global(pygame.K_F5, self.window_manager.toggle_maximize_restore)
        self.input_manager.bind_key_down_global(pygame.K_F11, self.window_manager.toggle_fullscreen)

    def change_scene(self, scene_class):
        """Switch to a new scene."""
        self.previous_scene = self.current_scene
        self.current_scene = scene_class(self)

    def return_scene(self):
        """Return to the previous scene."""
        self.current_scene = self.previous_scene

    def run(self):
        """Main game loop."""
        while self.running:
            # Update time (in seconds)
            self.dt = self.clock.tick(self.fps) / 1000
            self.total_play_time += self.dt

            # Handle game logic
            self.events()
            self.update()
            self.render()

    def events(self):
        """Process pygame and user events."""
        events = pygame.event.get()
        for event in events:
            # Handle quit event
            if event.type == pygame.QUIT:
                self.quit_game()

            # Handle user events
            self.input_manager.handle_event(event)

        # Handle scene events
        self.current_scene.handle_events(events)

    def update(self):
        """Update current scene."""
        self.current_scene.update(self.dt)
        self.debug.update()

    def render(self):
        """Render current scene."""
        self.window_manager.render(self.current_scene.render)
        self.window_manager.render(self.debug.draw)

    def quit_game(self):
        """Exit the game."""
        self.running = False
        pygame.quit()
        quit()
