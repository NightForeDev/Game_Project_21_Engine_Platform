# engine/template_manager.py

import pygame

class TemplateManager:
    """
    Manage ...

    Attributes:
        Class Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        Template Attributes:
            templates (...): ...

        State Attributes:
            ... (...): ...

    Methods:
        Configuration:
            _setup(): Initialize and prepare all components.
            load_config(config): Load settings from configuration and initialize attributes.

        Debug:
            debug(): Print the current internal state for debugging purposes.

        Operations:
            update(): Update all components.
            render(): Render all components.
    """
    def __init__(self, app_config=None):
        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config if app_config else {}
        self.config = self.app_config.get(self.class_name, {})

        # Template Attributes
        self.templates = None

        # State Attributes
        # (Reserved for future use)

        # Initialize
        self._setup()

    """
    Configuration
        _setup
        load_config
    """
    def _setup(self):
        """
        Initialize and prepare all components.
        """
        # Load configuration
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration and initialize attributes.
        """
        # Early return if action is not applicable
        if config is None:
            return

        # Apply configuration values
        for name, template in config.get("templates", {}).items():
            self.templates[name] = template

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name} Templates: {list(self.templates.keys())}")
        print()

    """
    Operations
        update
        render
    """
    def update(self):
        """
        Update all components.
        """
        pass

    def render(self):
        """
        Render all components.
        """
        pass
