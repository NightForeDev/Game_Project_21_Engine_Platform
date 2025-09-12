# engine\base_scene.py

from abc import ABC, abstractmethod

class BaseScene(ABC):
    """
    Abstract base class for all scenes.

    Attributes:
        Manager Attributes:
            core_manager (CoreManager): Reference to the core application manager.
            debug_manager (DebugManager): Debug utility for overlay and diagnostics.
            input_manager (InputManager): Manage input state and callbacks.
            ui_manager (UIManager): Manage interface elements.
            window_manager (WindowManager): Manage window and rendering surface.

    Methods:
        Scene Management:
            change_scene(scene_class): Switch to a new scene.
            return_scene(): Return to the previous scene.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, core_manager):
        # Manager Attributes
        self.core_manager = core_manager
        self.debug_manager = core_manager.debug_manager
        self.input_manager = core_manager.input_manager
        self.ui_manager = core_manager.ui_manager
        self.window_manager = core_manager.window_manager

    """
    Scene Management
        change_scene
        return_scene
    """
    def change_scene(self, scene_class):
        """
        Switch to a new scene.
        """
        self.core_manager.change_scene(scene_class)

    def return_scene(self):
        """
        Return to the previous scene.
        """
        self.core_manager.return_scene()

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
