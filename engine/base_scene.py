# engine\base_scene.py

from abc import ABC, abstractmethod

class BaseScene(ABC):
    """
    Abstract base class for all scenes.

    Attributes:
        Base Attributes:
            class_name (str): Name of the class.

        Manager Attributes:
            core_manager (CoreManager): Manage application.
            debug_manager (DebugManager): Manage debug overlay and diagnostics.
            input_manager (InputManager): Manage input state and callbacks.
            scene_manager (SceneManager): Manage active scenes.
            ui_manager (UIManager): Manage interface elements.
            window_manager (WindowManager): Manage window and rendering surface.

    Methods:
        Configuration:
            _setup(): Internal initialization (calls _setup_input and setup).
            enter(): Called when scene becomes active (on set/push).
            exit(): Called when scene becomes inactive (on pop).
            _setup_input(): Configure input mapping and callbacks.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, core_manager):
        # Class Attributes
        self.class_name = self.__class__.__name__

        # Manager Attributes
        if core_manager:
            self.core_manager = core_manager
            self.debug_manager = core_manager.debug_manager
            self.input_manager = core_manager.input_manager
            self.scene_manager = core_manager.scene_manager
            self.ui_manager = core_manager.ui_manager
            self.window_manager = core_manager.window_manager

    """
    Configuration
        enter
        exit
        _setup
        _setup_input
    """
    @abstractmethod
    def enter(self):
        """
        Called when the scene becomes active (set/on push).
        """
        self._setup()

    @abstractmethod
    def exit(self):
        """
        Called when the scene is no longer active (on pop).
        """
        # Clear input callbacks from previous scene
        self.input_manager.clear_local_callbacks()

    @abstractmethod
    def _setup(self):
        """
        Initialize components.
        """
        # Initialize components
        self._setup_input()

    def _setup_input(self):
        """
        Configure key bindings and action mappings.
        """
        input_config = {
            "bind": [
                {}
            ],
            "map": {
            }
        }
        self.input_manager.load_config(input_config)

    """
    Operations
        events
        update
        render
    """
    @abstractmethod
    def events(self, events):
        """
        Process components events.
        """
        pass

    @abstractmethod
    def update(self, dt=None):
        """
        Update components.
        """
        pass

    @abstractmethod
    def render(self, surface=None):
        """
        Render components.
        """
        pass
