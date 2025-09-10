# engine/ui_manager.py

from engine.base_manager import BaseManager
from engine.ui_button import UIButton
from engine.ui_element import UIElement
from engine.ui_label import UILabel

class UIManager(BaseManager):
    """
    Manage all UI elements including creation, configuration, state handling and rendering.

    Attributes:
        Base Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        UI Attributes:
            elements (dict[str, UIElement]): Dictionary of UI elements by name.

        State Attributes:
            active (bool): Whether the UIManager is active.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        WIP:
            create_element(name, element_type, **kwargs): Create and register a new UI element.

        Debug:
            debug(): Print debug information.

        Operations:
            update(dt): Update components.
            render(surface): Render components.
    """

    def __init__(self, app_config=None):
        # UI Attributes
        self.elements = {}

        # State Attributes
        self.active = True

        # Initialize BaseManager and components
        super().__init__(app_config)

    """
    Configuration
        _setup
        load_config
    """
    def _setup(self):
        """
        Initialize and prepare all components.
        """
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration and initialize attributes.

        Config example:
            {
                "elements": {
                    "title": {"type": "UILabel", "text": "Hello", "x": 10, "y": 10},
                    "start_btn": {"type": "UIButton", "text": "Start", "x": 20, "y": 60}
                }
            }
        """
        if not config:
            return

        for name, element_cfg in config.get("elements", {}).items():
            element_type = element_cfg.get("type", "UIElement")
            self.create_element(name, element_type, **element_cfg)

    """
    WIP
    """
    def create_element(self, name: str, element_type: str, **kwargs):
        """
        Create and register a new UI element.

        Args:
            name (str): Identifier for the element.
            element_type (str): One of "UIElement", "UILabel", "UIButton".
            **kwargs: forwarded to element constructor.
        """
        element_class = {
            "UIElement": UIElement,
            "UILabel": UILabel,
            "UIButton": UIButton,
        }.get(element_type, UIElement)

        self.elements[name] = element_class(name=name, **kwargs)

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name} Active: {self.active}")
        print(f"Registered Elements: {list(self.elements.keys())}")
        for k, e in self.elements.items():
            print(f"  {k}: {e}")
        print()

    """
    Operations
        update
        render
    """
    def update(self, dt=None):
        """
        Update all components.
        """
        if not self.active:
            return

        for element in list(self.elements.values()):
            element.update()

    def render(self, surface=None):
        """
        Render all components.
        """
        if not self.active:
            return

        for element in list(self.elements.values()):
            element.render(surface)
