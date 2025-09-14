# engine/base_manager.py

from abc import ABC, abstractmethod
from engine.config_loader import load_config

class BaseManager(ABC):
    """
    Abstract base class for managers.

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

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, core_manager=None, app_config=None):
        # Load application configuration if not provided
        if app_config is None:
            app_config = load_config()

        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config if app_config else {}
        self.config = self.app_config.get(self.class_name, {})

        # Manager Attributes
        if core_manager:
            self.core_manager = core_manager
            self.debug_manager = core_manager.debug_manager
            self.input_manager = core_manager.input_manager
            self.scene_manager = core_manager.scene_manager
            self.ui_manager = core_manager.ui_manager
            self.window_manager = core_manager.window_manager

        # Initialize
        self._setup()

    """
    Configuration
        _setup
        load_config
    """
    @abstractmethod
    def _setup(self):
        """
        Initialize components.
        """
        # Load configuration
        self.load_config(self.config)

        # Initialize components
        pass

    @abstractmethod
    def load_config(self, config):
        """
        Load settings from configuration.
        """
        # Early return if action is not applicable
        if config is None:
            return

        # Apply configuration values
        pass

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}: no debug info implemented.")

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
        pass

    def update(self, dt=None):
        """
        Update components.
        """
        pass

    def render(self, surface=None):
        """
        Render components.
        """
        pass
