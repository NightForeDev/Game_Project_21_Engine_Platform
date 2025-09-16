# engine/input_manager.py

import pygame
from engine.base_manager import BaseManager

class InputManager(BaseManager):
    """
    Manage input state and callbacks.

    Attributes:
        State Attributes:
            key_state (dict[int, bool]): Current pressed state of keyboard keys.
            mouse_state (dict[int, bool]): Current pressed state of mouse buttons.

        Local Bindings:
            local_key_down_callbacks (dict[int, Callable]): Functions bound to key press events locally.
            local_key_up_callbacks (dict[int, Callable]): Functions bound to key release events locally.
            local_mouse_down_callbacks (dict[int, Callable]): Functions bound to mouse press events locally.
            local_mouse_up_callbacks (dict[int, Callable]): Functions bound to mouse release events locally.

        Global Bindings:
            global_key_down_callbacks (dict[int, Callable]): Functions bound to key press events globally.
            global_key_up_callbacks (dict[int, Callable]): Functions bound to key release events globally.
            global_mouse_down_callbacks (dict[int, Callable]): Functions bound to mouse press events globally.
            global_mouse_up_callbacks (dict[int, Callable]): Functions bound to mouse release events globally.

        Action Mappings:
            action_to_key (dict[str, int]): Maps action names to keyboard keys.
            action_to_mouse (dict[str, int]): Maps action names to mouse buttons.

        Persisted Input:
            persisted_input (dict): Stores all mappings and bindings for persistence across reloads.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        Mapping Methods:
            map_action_to_key(key, action): Map an action to a keyboard key.
            map_action_to_mouse(button, action): Map an action to a mouse button.

        Binding Methods:
            bind_key_down(key, callback, global_=False): Bind a callback to a key press.
            bind_key_up(key, callback, global_=False): Bind a callback to a key release.
            bind_mouse_down(button, callback, global_=False): Bind a callback to a mouse button press.
            bind_mouse_up(button, callback, global_=False): Bind a callback to a mouse button release.

        Input Utilities:
            is_action_active(action): Check if an action is currently active (held).
            clear_local_callbacks(): Remove all local callbacks.
            clear_all_callbacks(): Remove all callbacks.

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
    """
    def __init__(self, core_manager=None, app_config=None):
        # State Attributes
        self.key_state = {}
        self.mouse_state = {}

        # Local Bindings
        self.local_key_down_callbacks = {}
        self.local_key_up_callbacks = {}
        self.local_mouse_down_callbacks = {}
        self.local_mouse_up_callbacks = {}

        # Global Bindings
        self.global_key_down_callbacks = {}
        self.global_key_up_callbacks = {}
        self.global_mouse_down_callbacks = {}
        self.global_mouse_up_callbacks = {}

        # Action Mappings
        self.action_to_key = {}
        self.action_to_mouse = {}

        # Persisted Input
        self.persisted_input = {"bind": [], "map": {}}

        # Initialize BaseManager and components
        super().__init__(core_manager, app_config)

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
        # Early return if action is not applicable
        if config is None:
            return

        # Bind callbacks
        for bind in config.get("bind", []):
            # Get binding info
            callback = bind["callback"]
            global_ = bind.get("global", False)

            # Check persisted input
            persisted_bind = None
            for b in self.persisted_input["bind"]:
                if b["callback"] == callback:
                    persisted_bind = b
                    break

            if persisted_bind:
                key = persisted_bind.get("key")
                button = persisted_bind.get("button")

            # Fallback to config
            else:
                key = bind.get("key")
                button = bind.get("button")

            # Apply bindings
            if key and callback:
                self.bind_key_down(key, callback, global_=global_)
            if button and callback:
                self.bind_mouse_down(button, callback, global_=global_)

            # WIP
            # Add 'up' event support

        # Map actions
        for action, mapping in config.get("map", {}).items():
            # Check persisted input
            if action in self.persisted_input.get("map", {}):
                key = self.persisted_input["map"][action].get("key")
                mouse = self.persisted_input["map"][action].get("mouse")

            # Fallback to config
            else:
                key = mapping.get("key")
                mouse = mapping.get("mouse")

            # Apply mappings
            if key is not None:
                self.map_action_to_key(key, action)
            if mouse is not None:
                self.map_action_to_mouse(mouse, action)

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
        # Register
        if global_:
            self.global_key_down_callbacks[key] = callback
        else:
            self.local_key_down_callbacks[key] = callback

        # Persist
        self.persisted_input["bind"].append({
            "key": key,
            "callback": callback,
            "global": global_,
        })

    def bind_key_up(self, key, callback, global_=False):
        """
        Bind a callback to a key release.
        """
        # Register
        if global_:
            self.global_key_up_callbacks[key] = callback
        else:
            self.local_key_up_callbacks[key] = callback

        # Persist
        self.persisted_input["bind"].append({
            "key": key,
            "callback": callback,
            "global": global_,
        })

    def bind_mouse_down(self, button, callback, global_=False):
        """
        Bind a callback to a mouse button press.
        """
        # Register
        if global_:
            self.global_mouse_down_callbacks[button] = callback
        else:
            self.local_mouse_down_callbacks[button] = callback

        # Persist
        self.persisted_input["bind"].append({
            "button": button,
            "callback": callback,
            "global": global_,
        })

    def bind_mouse_up(self, button, callback, global_=False):
        """
        Bind a callback to a mouse button release.
        """
        # Register
        if global_:
            self.global_mouse_up_callbacks[button] = callback
        else:
            self.local_mouse_up_callbacks[button] = callback

        # Persist
        self.persisted_input["bind"].append({
            "button": button,
            "callback": callback,
            "global": global_,
        })

    """
    Mapping Methods
        map_action_to_key
        map_action_to_mouse
    """
    def map_action_to_key(self, key, action):
        """
        Bind an action to a keyboard key.
        """
        # Register
        self.action_to_key[action] = key

        # Persist
        self.persisted_input["map"][action] = {"key": key}

    def map_action_to_mouse(self, button, action):
        """
        Bind an action to a mouse button.
        """
        # Register
        self.action_to_mouse[button] = action

        # Persist
        self.persisted_input["map"][action] = {"mouse": button}

    """
    Input Utilities
        is_action_active
        clear_local_callbacks
        clear_all_callbacks
    """
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
    Debug
        debug
    """
    def debug(self):
        """
        Print debug information.
        """
        print(f"{self.class_name}")
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

    """
    Operations
        events
    """
    def events(self, event):
        """
        Process components events.
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
