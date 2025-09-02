# engine\core.py

import random
import pygame

from engine.config_loader import load_config
from engine.debug_manager import DebugManager
from engine.window_manager import WindowManager
from engine.input_manager import InputManager

class Core:
    """
    Core engine class responsible for managing the application.

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
            running (bool): Controls whether the main loop is active.

        Scene Attributes:
            initial_scene_class (type): Class reference to the initial scene.
            current_scene (Scene): Currently active scene instance.
            previous_scene (Scene): Previously active scene instance.

    Methods:
        Initialization:
            _setup(run): Initialize and prepare all components.
            _setup_input(): Configure key bindings and action mappings.
            setup_initial_engine(): Initialize core engine systems and managers.
            setup_initial_scene(): Set the initial scene instance.

        Scene Management:
            change_scene(scene_class): Switch to a new scene.
            return_scene(): Return to the previous scene.

        Runtime:
            _run(): Executes the main loop.
            _events(): Process pygame and user events.
            quit_game(): Exit the game.

        Operations:
            update(): Update all components.
            render(): Render all components.
    """
    def __init__(self, initial_scene_class, app_config=None, run=True):
        """
        Initialize the class.

        Args:
            initial_scene_class (type): Class reference to the initial scene.
            app_config (dict, optional): Preloaded application config.
            run (bool): Whether to start the main loop after setup.
        """
        # Load application configuration if not provided
        if app_config is None:
            app_config = load_config()

        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config
        self.config = self.app_config[self.class_name]

        # Time Attributes
        self.fps = None
        self.clock = None
        self.dt = None
        self.total_play_time = None

        # Manager Attributes
        self.debug_manager = None
        self.window_manager = None
        self.input_manager = None

        # State Attributes
        self.running = None

        # Scene Attributes
        self.initial_scene_class = initial_scene_class
        self.current_scene = None
        self.previous_scene = None

        # Initialize all components
        self._setup(run)

    """
    Initialization
        _setup
        _setup_input
        setup_initial_engine
        setup_initial_scene
    """
    def _setup(self, run):
        """
        Initialize and prepare all components.

        Args:
            run (bool): Whether to start the main loop after setup.
        """
        # Initialize components
        self.setup_initial_engine()

        # Start process
        if run:
            self._run()

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key": pygame.K_ESCAPE, "callback": self.quit_game, "global": True},
                {"key": pygame.K_F1, "callback": self.debug_manager.toggle, "global": True},
                {"key": pygame.K_F3, "callback": self.window_manager.toggle_borderless, "global": True},
                {"key": pygame.K_F4, "callback": self.window_manager.toggle_maximized, "global": True},
                {"key": pygame.K_F5, "callback": self.setup_initial_engine, "global": True},
                {"key": pygame.K_F6, "callback": self.window_manager.toggle_resizable, "global": True},
                {"key": pygame.K_F10, "callback": self.input_manager.debug, "global": True},
                {"key": pygame.K_F11, "callback": self.window_manager.toggle_fullscreen, "global": True},
                {"key": pygame.K_F12, "callback": self.setup_initial_scene, "global": True},
            ],
            "map": {
            }
        }
        self.input_manager.load_config(input_config)

    def setup_initial_engine(self):
        """
        Initialize core engine systems and managers.
        """
        # Initialize pygame and random seed
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

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

        # Prepare remaining components
        self.setup_initial_scene()
        self._setup_input()

    def setup_initial_scene(self):
        """
        Set the initial scene instance.
        """
        self.previous_scene = None
        self.current_scene = self.initial_scene_class(self)

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
    Runtime
        _run
        _events
        quit_game
    """
    def _run(self):
        """
        Executes the main loop.
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
        Update all components.
        """
        self.window_manager.update()
        self.current_scene.update(self.dt)
        self.debug_manager.update()

    def render(self):
        """
        Render all components.
        """
        self.current_scene.render(self.window_manager.render_surface)
        self.debug_manager.draw(self.window_manager.render_surface)
        self.window_manager.render()
