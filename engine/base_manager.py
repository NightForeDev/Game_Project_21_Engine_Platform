# engine/base_manager.py

from abc import ABC, abstractmethod
from engine.config_loader import load_config

class BaseManager(ABC):
    """
    Abstract base class for managers.

    Attributes:
        Class Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

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
    def __init__(self, app_config=None):
        # Load application configuration if not provided
        if app_config is None:
            app_config = load_config()

        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config if app_config else {}
        self.config = self.app_config.get(self.class_name, {})

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
    @abstractmethod
    def events(self, events):
        """Process components events."""
        pass

    @abstractmethod
    def update(self, dt):
        """Update components."""
        pass

    @abstractmethod
    def render(self, surface):
        """Render components."""
        pass
