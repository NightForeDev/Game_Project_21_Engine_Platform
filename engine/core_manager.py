# engine\core.py

import random
import sys
import pygame
from engine.base_manager import BaseManager
from engine.debug_manager import DebugManager
from engine.input_manager import InputManager
from engine.scene_manager import SceneManager
from engine.ui_manager import UIManager
from engine.window_manager import WindowManager

class CoreManager(BaseManager):
    """
    Manage application.

    Attributes:
        Base Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        Manager Attributes:
            core_manager (CoreManager): Manage application.
            debug_manager (DebugManager): Manage debug overlay and diagnostics.
            input_manager (InputManager): Manage input state and callbacks.
            scene_manager (SceneManager): Manage active scenes.
            ui_manager (UIManager): Manage interface elements.
            window_manager (WindowManager): Manage window and rendering surface.

        Time Attributes:
            fps (int): Frames per second target.
            clock (pygame.time.Clock): Clock to track time.
            total_play_time (float): Total time elapsed (seconds).

        State Attributes:
            running (bool): Controls whether the main loop is active.

        Scene Attributes:
            initial_scene_class (type): Class reference to the initial scene.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.
            _setup_input(): Configure key bindings and action mappings.
            setup_initial_engine(): Initialize systems and managers.
            setup_initial_scene(): Initialize scene instance.

        Runtime:
            run(): Executes the main loop.
            quit_game(): Exit the game.

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, initial_scene_class, app_config=None, run=True):
        """
        Initialize the class.

        Args:
            initial_scene_class (type): Class reference to the initial scene.
            app_config (dict, optional): Preloaded application config.
            run (bool): Whether to start the main loop after setup.
        """
        # Manager Attributes
        self.core_manager = None
        self.debug_manager = None
        self.input_manager = None
        self.scene_manager = None
        self.ui_manager = None
        self.window_manager = None

        # Time Attributes
        self.fps = None
        self.clock = None
        self.total_play_time = None

        # State Attributes
        self.running = None

        # Scene Attributes
        self.initial_scene_class = initial_scene_class

        # Initialize BaseManager and components
        super().__init__(app_config)

        # Start the main loop
        if run:
            self.run()

    """
    Configuration
        _setup
        load_config
        _setup_input
        setup_initial_engine
        setup_initial_scene
    """
    def _setup(self):
        """
        Initialize components.
        """
        # Load configuration
        self.load_config(self.config)

        # Initialize components
        self.setup_initial_engine()

    def load_config(self, config):
        """
        Load settings from configuration.
        """
        # Early return if action is not applicable
        if config is None:
            return

        # Apply configuration values
        self.fps = self.config["fps"]

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {"key_down": pygame.K_ESCAPE, "callback": self.quit_game, "global": True},
                {"key_down": pygame.K_F1, "callback": self.debug_manager.toggle, "global": True},
                {"key_down": pygame.K_F3, "callback": self.window_manager.toggle_borderless, "global": True},
                {"key_down": pygame.K_F4, "callback": self.window_manager.toggle_maximized, "global": True},
                {"key_down": pygame.K_F5, "callback": self.setup_initial_engine, "global": True},
                {"key_down": pygame.K_F6, "callback": self.window_manager.toggle_resizable, "global": True},
                {"key_down": pygame.K_F11, "callback": self.window_manager.toggle_fullscreen, "global": True},
            ],
        }
        self.input_manager.load_config(input_config)

    def setup_initial_engine(self):
        """
        Initialize systems and managers.
        """
        # Initialize pygame and random seed
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        random.seed()

        # Time Attributes
        self.clock = pygame.time.Clock()
        self.total_play_time = 0

        # Manager Attributes
        self.core_manager = self
        self.debug_manager = DebugManager(core_manager=self)
        self.input_manager = InputManager(core_manager=self, app_config=self.app_config)
        self.scene_manager = SceneManager(core_manager=self, app_config=self.app_config)
        self.ui_manager = UIManager(core_manager=self, app_config=self.app_config)
        self.window_manager = WindowManager(core_manager=self, app_config=self.app_config, clock=self.clock)

        # State Attributes
        self.running = True

        # Prepare remaining components
        self._setup_input()
        self.scene_manager.set_scene(self.initial_scene_class)

    """
    Runtime
        run
        quit_game
    """
    def run(self):
        """
        Executes the main loop.
        """
        while self.running:
            # Update time (seconds)
            dt = self.clock.tick(self.fps) / 1000
            self.total_play_time += dt

            # Gather frame events
            events = pygame.event.get()

            surface = self.window_manager.render_surface

            # Handle logic
            self.events(events)
            self.update(dt)
            self.render(surface)

    def quit_game(self):
        """
        Exit the game.
        """
        self.running = False
        self.debug()
        pygame.quit()
        sys.exit()

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
        print(f"running={self.running}")
        print(f"fps={self.fps}")
        print(f"total_play_time={self.total_play_time:.2f}")
        print()

        self.input_manager.debug()
        self.scene_manager.debug()
        self.ui_manager.debug()
        self.window_manager.debug()

    """
    Operations
        events
        update
        render
    """
    def events(self, events):
        """
        Process components events.
        """
        for event in events:
            # Pygame events
            if event.type == pygame.VIDEORESIZE:
                self.window_manager.resize()
            if event.type == pygame.QUIT:
                self.quit_game()

            # Input events
            self.input_manager.events(event)

        # Scene-level events
        self.scene_manager.events(events)

    def update(self, dt=None):
        """
        Update components.
        """
        self.scene_manager.update(dt)
        self.debug_manager.update()
        self.ui_manager.update()
        self.window_manager.update()

    def render(self, surface=None):
        """
        Render components.
        """
        self.scene_manager.render(surface)
        self.debug_manager.draw(surface)
        self.ui_manager.render(surface)
        self.window_manager.render()
