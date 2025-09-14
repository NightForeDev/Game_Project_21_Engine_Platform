# engine/scene_manager.py

from engine.base_manager import BaseManager

class SceneManager(BaseManager):
    """
    Manage active scenes in the application.

    Attributes:
        Base Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        Manager Attributes:
            core_manager (CoreManager): Manage application.
            debug_manager (DebugManager): Manage debug overlay and diagnostics.
            input_manager (InputManager): Manage input state and callbacks.
            ui_manager (UIManager): Manage interface elements.
            window_manager (WindowManager): Manage window and rendering surface.

        State Attributes:
            scenes (list): Stack of active scenes.
            current_scene (BaseScene): Scene currently in focus.

        State Attributes:
            scenes (list[BaseScene]): Stack of scenes.
            current_scene (BaseScene): Currently active scene instance.
            previous_scene (BaseScene): Previously active scene instance.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        Scene Management:
            push_scene(scene): Push a new scene on top of the stack.
            pop_scene(): Pop the current scene off the stack.
            clear_scenes(): Remove all scenes.

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
            update(dt): Update components.
            render(surface): Render components.
    """
    def __init__(self, app_config=None, core_manager=None):
        # State Attributes
        self.scenes = []
        self.previous_scene = None
        self.current_scene = None

        # Initialize BaseManager and components
        super().__init__(app_config, core_manager)

    """
    Configuration
        _setup
        load_config
    """
    def _setup(self):
        """
        Initialize components.
        """
        # Load configuration
        self.load_config(self.config)

    def load_config(self, config):
        """
        Load settings from configuration.
        """
        if config is None:
            return

        # WIP: Preload scenes or set initial scene from config
        initial_scene = config.get("initial_scene")
        if initial_scene:
            self.push_scene(initial_scene)

    """
    Scene Management
        push_scene
        pop_scene
        clear_scenes
    """
    def push_scene(self, scene_class):
        """
        Push a new scene onto the stack.
        """
        self.previous_scene = self.current_scene
        self.current_scene = scene_class(self.core_manager)
        self.scenes.append(self.current_scene)

    def pop_scene(self):
        """
        Pop the current scene from the stack.
        """
        if not self.scenes:
            return
        self.scenes.pop()
        self.current_scene = self.scenes[-1] if self.scenes else None

    def clear_scenes(self):
        """
        Remove all scenes.
        """
        self.scenes.clear()
        self.current_scene = None
        self.previous_scene = None

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
        print("Scenes:", [scene.__class__.__name__ for scene in self.scenes])
        print("Current Scene:", self.current_scene.__class__.__name__ if self.current_scene else None)
        print("Previous Scene:", self.previous_scene.__class__.__name__ if self.previous_scene else None)
        print()

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
        # Process events on the active scene (top of the stack).
        if self.current_scene:
            self.current_scene.events(events)

    def update(self, dt=None):
        """
        Update components.
        """
        # Update the active scene (top of the stack).
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, surface=None):
        """
        Render components.
        """
        # Render all scenes in the stack in order.
        for scene in self.scenes:
            scene.render(surface)
