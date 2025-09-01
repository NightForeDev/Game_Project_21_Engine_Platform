# engine\core.py

import random
import pygame

from engine.config_loader import load_config
from engine.debug_manager import DebugManager
from engine.window_manager import WindowManager
from engine.input_manager import InputManager

class Core:
    """
    Core engine class responsible for events, updating logic, and rendering frames.

    Attributes:
        Class Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        Time Attributes:
            fps (int): Frames per second target.
            clock (pygame.time.Clock): Clock to track time.
            dt (float): Delta time for the current frame (seconds).
            total_play_time (float): Total time elapsed (seconds).

        Manager Attributes:
            debug_manager (DebugManager): Debug utility for overlay and diagnostics.
            window_manager (WindowManager): Handles window and rendering surface.
            input_manager (InputManager): Handles input state and callbacks.

        State Attributes:
            running (bool): Flag controlling the main loop.

        Scene Attributes:
            current_scene (Scene): Currently active scene.
            previous_scene (Scene): Previously active scene.
            initial_scene (type): Class reference for the initial scene.

    Methods:
        Initialization:
            setup_input(): Configure input bindings.

        Scene Management:
            change_scene(scene_class): Switch to a new scene.
            return_scene(): Return to the previous scene.

        Main Loop:
            run(): Main game loop.
            _events(): Process pygame and user events.

        System:
            restart_game(): Restart the game from the initial scene.
            quit_game(): Exit the game.

        Operations:
            update(): Updates the class.
            render(): Renders the class.
    """
    def __init__(self, initial_scene_class):
        """Set up the game."""
        # Initialize pygame and random seed
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()
        app_config = load_config()

        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config
        self.config = self.app_config[self.class_name]

        # Time Attributes
        self.fps = self.config["fps"]
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps) / 1000
        self.total_play_time = 0

        # Manager Attributes
        self.debug_manager = DebugManager(self)
        self.window_manager = WindowManager(self.app_config, self.clock)
        self.input_manager = InputManager(self.app_config)

        # State Attributes
        self.running = True

        # Scene Attributes
        self.current_scene = None
        self.previous_scene = None
        self.initial_scene = initial_scene_class

        # Initialization
        self.setup_input()
        self.restart_game()

    """
    Initialization
        setup_input
    """
    def setup_input(self):
        """
        Bind and map keys and mouse buttons to actions or callbacks.
        """
        input_config = {
            "bind": [
                {"key": pygame.K_ESCAPE, "callback": self.quit_game, "global": True},
                {"key": pygame.K_F1, "callback": self.debug_manager.toggle, "global": True},
                {"key": pygame.K_F3, "callback": self.window_manager.toggle_borderless, "global": True},
                {"key": pygame.K_F4, "callback": self.window_manager.toggle_maximized, "global": True},
                {"key": pygame.K_F5, "callback": self.restart_game, "global": True},
                {"key": pygame.K_F6, "callback": self.window_manager.toggle_resizable, "global": True},
                {"key": pygame.K_F11, "callback": self.window_manager.toggle_fullscreen, "global": True},
                {"key": pygame.K_F12, "callback": self.input_manager.debug, "global": True},
            ]
        }
        self.input_manager.load_config(input_config)

    """
    Scene Management
        change_scene
        return_scene
    """
    def change_scene(self, scene_class):
        """
        Switch to a new scene.
        """
        self.previous_scene = self.current_scene
        self.current_scene = scene_class(self)

    def return_scene(self):
        """
        Return to the previous scene.
        """
        self.current_scene = self.previous_scene

    """
    Main Loop
        run
        _events
    """
    def run(self):
        """
        Main loop.
        """
        while self.running:
            # Update time (seconds)
            self.dt = self.clock.tick(self.fps) / 1000
            self.total_play_time += self.dt

            # Handle logic
            self._events()
            self.update()
            self.render()

    def _events(self):
        """
        Process pygame and user events.
        """
        events = pygame.event.get()
        for event in events:
            # Pygame events
            if event.type == pygame.VIDEORESIZE:
                self.window_manager.resize()
            if event.type == pygame.QUIT:
                self.quit_game()

            # Input events
            self.input_manager.handle_event(event)

        # Scene-level events
        self.current_scene.handle_events(events)

    """
    System
        restart_game
        quit_game
    """
    def restart_game(self):
        """
        Restart from the initial scene.
        """
        self.__init__(self.initial_scene)

    def quit_game(self):
        """
        Exit the game.
        """
        self.running = False
        pygame.quit()
        quit()

    """
    Operations
        update
        render
    """
    def update(self):
        """
        Update the class.
        """
        self.window_manager.update()
        self.current_scene.update(self.dt)
        self.debug_manager.update()

    def render(self):
        """
        Render the class.
        """
        self.current_scene.render(self.window_manager.render_surface)
        self.debug_manager.draw(self.window_manager.render_surface)
        self.window_manager.render()
