# engine/input_manager.py

import pygame

class InputManager:
    """
    Manages input including state tracking, action mapping, and local/global callback handling.

    Attributes:
        Class Attributes:
            class_name (str): Name of the class.
            app_config (dict): Full application configuration.
            config (dict): Configuration specific to the class.

        State Attributes:
            key_state (dict[int, bool]): Current pressed state of keyboard keys.
            mouse_state (dict[int, bool]): Current pressed state of mouse buttons.

        Local Callbacks:
            local_key_down_callbacks (dict[int, Callable]): Functions bound to key press events locally.
            local_key_up_callbacks (dict[int, Callable]): Functions bound to key release events locally.
            local_mouse_down_callbacks (dict[int, Callable]): Functions bound to mouse press events locally.
            local_mouse_up_callbacks (dict[int, Callable]): Functions bound to mouse release events locally.

        Global Callbacks:
            global_key_down_callbacks (dict[int, Callable]): Functions bound to key press events globally.
            global_key_up_callbacks (dict[int, Callable]): Functions bound to key release events globally.
            global_mouse_down_callbacks (dict[int, Callable]): Functions bound to mouse press events globally.
            global_mouse_up_callbacks (dict[int, Callable]): Functions bound to mouse release events globally.

        Action Mappings:
            action_to_key (dict[str, int]): Maps action names to keyboard keys.
            action_to_mouse (dict[str, int]): Maps action names to mouse buttons.

    Methods:
        Configuration:
            _setup(): Initialize and prepare all components.
            load_config(config): Load settings from configuration and initialize attributes.

        Callback Management:
            clear_local_callbacks(): Remove all local callbacks.
            clear_all_callbacks(): Remove all callbacks.

        Binding Methods:
            bind_key_down(key, callback, global_=False): Bind a callback to a key press.
            bind_key_up(key, callback, global_=False): Bind a callback to a key release.
            bind_mouse_down(button, callback, global_=False): Bind a callback to a mouse button press.
            bind_mouse_up(button, callback, global_=False): Bind a callback to a mouse button release.

        Mapping Methods:
            map_action_to_key(key, action): Map an action to a keyboard key.
            map_action_to_mouse(button, action): Map an action to a mouse button.

        Event Handling:
            handle_event(event): Handle pygame events to update states and trigger callbacks.
            is_action_active(action): Check if an action is currently active (held).

        Debug:
            debug(): Print the current internal state for debugging purposes.
    """
    def __init__(self, app_config=None):
        # Class Attributes
        self.class_name = self.__class__.__name__
        self.app_config = app_config
        self.config = self.app_config[self.class_name]

        # State Attributes
        self.key_state = {}
        self.mouse_state = {}

        # Local Callbacks
        self.local_key_down_callbacks = {}
        self.local_key_up_callbacks = {}
        self.local_mouse_down_callbacks = {}
        self.local_mouse_up_callbacks = {}

        # Global Callbacks
        self.global_key_down_callbacks = {}
        self.global_key_up_callbacks = {}
        self.global_mouse_down_callbacks = {}
        self.global_mouse_up_callbacks = {}

        # Action Mappings
        self.action_to_key = {}
        self.action_to_mouse = {}

        # Initialize all components
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

        # Map actions
        for action, mapping in config.get("map", {}).items():
            key = mapping.get("key")
            mouse = mapping.get("mouse")

            if key is not None:
                self.map_action_to_key(key, action)
            if mouse is not None:
                self.map_action_to_mouse(mouse, action)

        # Bind callbacks
        for bind in config.get("bind", []):
            key = bind.get("key")
            button = bind.get("button")
            callback = bind.get("callback")
            global_ = bind.get("global", False)

            if key is not None and callback is not None:
                self.bind_key_down(key, callback, global_=global_)
            if button is not None and callback is not None:
                self.bind_mouse_down(button, callback, global_=global_)

    """
    Callback Management
        clear_local_callbacks
        clear_all_callbacks
    """
    def clear_local_callbacks(self):
        """
        Remove all local callbacks.
        """
        self.local_key_down_callbacks.clear()
        self.local_key_up_callbacks.clear()
        self.local_mouse_down_callbacks.clear()
        self.local_mouse_up_callbacks.clear()

    def clear_all_callbacks(self):
        """
        Remove all callbacks.
        """
        self.clear_local_callbacks()
        self.global_key_down_callbacks.clear()
        self.global_key_up_callbacks.clear()
        self.global_mouse_down_callbacks.clear()
        self.global_mouse_up_callbacks.clear()

    """
    Binding Methods
        bind_key_down
        bind_key_up
        bind_mouse_down
        bind_mouse_up
    """
    def bind_key_down(self, key, callback, global_=False):
        """
        Bind a callback to a key press.
        """
        if global_:
            self.global_key_down_callbacks[key] = callback
        else:
            self.local_key_down_callbacks[key] = callback

    def bind_key_up(self, key, callback, global_=False):
        """
        Bind a callback to a key release.
        """
        if global_:
            self.global_key_up_callbacks[key] = callback
        else:
            self.local_key_up_callbacks[key] = callback

    def bind_mouse_down(self, button, callback, global_=False):
        """
        Bind a callback to a mouse button press.
        """
        if global_:
            self.global_mouse_down_callbacks[button] = callback
        else:
            self.local_mouse_down_callbacks[button] = callback

    def bind_mouse_up(self, button, callback, global_=False):
        """
        Bind a callback to a mouse button release.
        """
        if global_:
            self.global_mouse_up_callbacks[button] = callback
        else:
            self.local_mouse_up_callbacks[button] = callback

    """
    Mapping Methods
        map_action_to_key
        map_action_to_mouse
    """
    def map_action_to_key(self, key, action):
        """
        Bind an action to a keyboard key.
        """
        self.action_to_key[action] = key

    def map_action_to_mouse(self, mouse, action):
        """
        Bind an action to a mouse button.
        """
        self.action_to_mouse[action] = mouse

    """
    Event handling
        handle_event
        is_action_active
    """
    def handle_event(self, event):
        """
        Handle pygame events to update states and trigger callbacks.
        """
        # Key pressed
        if event.type == pygame.KEYDOWN:
            self.key_state[event.key] = True
            if event.key in self.local_key_down_callbacks:
                self.local_key_down_callbacks[event.key]()
            elif event.key in self.global_key_down_callbacks:
                self.global_key_down_callbacks[event.key]()

        # Key released
        elif event.type == pygame.KEYUP:
            self.key_state[event.key] = False
            if event.key in self.local_key_up_callbacks:
                self.local_key_up_callbacks[event.key]()
            elif event.key in self.global_key_up_callbacks:
                self.global_key_up_callbacks[event.key]()

        # Mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_state[event.button] = True
            if event.button in self.local_mouse_down_callbacks:
                self.local_mouse_down_callbacks[event.button]()
            elif event.button in self.global_mouse_down_callbacks:
                self.global_mouse_down_callbacks[event.button]()

        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_state[event.button] = False
            if event.button in self.local_mouse_up_callbacks:
                self.local_mouse_up_callbacks[event.button]()
            elif event.button in self.global_mouse_up_callbacks:
                self.global_mouse_up_callbacks[event.button]()

    def is_action_active(self, action):
        """
        Check if an action is currently active (held).

        Returns True if the key or mouse button mapped to the action is currently held.
        """
        # Check mapped key
        key = self.action_to_key.get(action)
        if key and self.key_state.get(key, False):
            return True

        # Check mapped mouse button
        button = self.action_to_mouse.get(action)
        if button and self.mouse_state.get(button, False):
            return True

        # Not active
        return False

    """
    Debug
        debug
    """
    def debug(self):
        """
        Print the current internal state for debugging purposes.
        """
        print("Held Keys:", self.key_state)
        print("Held Mouse Buttons:", self.mouse_state)
        print("Action to Key:", self.action_to_key)
        print("Action to Mouse:", self.action_to_mouse)
        print("Local Key Down Callbacks:", list(self.local_key_down_callbacks.keys()))
        print("Local Key Up Callbacks:", list(self.local_key_up_callbacks.keys()))
        print("Local Mouse Down Callbacks:", list(self.local_mouse_down_callbacks.keys()))
        print("Local Mouse Up Callbacks:", list(self.local_mouse_up_callbacks.keys()))
        print("Global Key Down Callbacks:", list(self.global_key_down_callbacks.keys()))
        print("Global Key Up Callbacks:", list(self.global_key_up_callbacks.keys()))
        print("Global Mouse Down Callbacks:", list(self.global_mouse_down_callbacks.keys()))
        print("Global Mouse Up Callbacks:", list(self.global_mouse_up_callbacks.keys()))
        print()
