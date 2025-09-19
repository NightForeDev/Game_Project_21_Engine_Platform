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

        Input Attributes:
            bindings (...): callback . event driven
            mappings (...): action . state driven

        Persisted Input:
            persisted_input (dict): Stores all mappings and bindings for persistence across reloads.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

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

        # Input Attributes
        self.bindings = {
            "local": {
                "key_down": {},
                "key_up": {},
                "mouse_down": {},
                "mouse_up": {}
            },
            "global": {
                "key_down": {},
                "key_up": {},
                "mouse_down": {},
                "mouse_up": {}
            }
        }

        self.mappings = {}

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

        # Process callback bindings
        for bind in config.get("bind", []):
            # Get binding info
            callback = bind["callback"]
            scope = "global" if bind.get("global", False) else "local"

            # Use persisted codes if they exist
            persisted_bind = next((b for b in self.persisted_input["bind"] if b.get("callback") == callback), {})

            # Apply bindings
            for event_type in ["key_down", "key_up", "mouse_down", "mouse_up"]:
                code = persisted_bind.get(event_type) or bind.get(event_type)
                self.bind_callback(scope, event_type, code, callback)

        # Process action mappings
        for action, mapping in config.get("map", {}).items():
            # Use persisted codes if they exist
            persisted_map = self.persisted_input.get("map", {}).get(action, {})

            # Apply mappings
            for device_type, code in mapping.items():
                code = persisted_map.get(device_type) or mapping.get(device_type)
                self.map_action(action, device_type, code)

    def bind_callback(self, scope, event_type, code, callback):
        """
        Bind a callback to an input event.

        Args:
            scope (str): Binding scope. Must be 'local' or 'global'.
            event_type (str): Type of input event. Must be 'key_down', 'key_up', 'mouse_down', 'mouse_up'.
            code (int): Key or mouse button code.
            callback (callable): Function to call when the event is triggered.
        """
        # Validate arguments
        if scope not in self.bindings:
            raise ValueError(f"Invalid scope '{scope}', expected 'local' or 'global'.")
        if event_type not in self.bindings[scope]:
            raise ValueError(f"Invalid event '{event_type}', expected key_down/up or mouse_down/up.")
        if not callable(callback):
            raise TypeError(f"Callback must be callable, got {type(callback).__name__}.")

        # Register the callback
        self.bindings[scope][event_type][code] = callback

        # Persist this binding
        self.persisted_input["bind"].append({
            "callback": callback,
            event_type: code,
            "global": scope == "global"
        })

    def map_action(self, action, device_type, code):
        """
        Map an action to an input state.

        Args:
            action (str): Name of the action.
            device_type (str): Type of input device. Must be 'key' or 'mouse'.
            code (int): Key or mouse button code.
        """
        # Validate arguments
        if device_type not in ["key", "mouse"]:
            raise ValueError(f"Invalid device '{device_type}', expected 'key' or 'mouse'.")

        # Register the action
        self.mappings[action] = {device_type: code}

        # Persist this mapping
        self.persisted_input["map"][action] = {device_type: code}

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
        # Get the mapping for the action
        mapping = self.mappings.get(action)
        if not mapping:
            return False

        # Check key mapping
        key_code = mapping.get("key")
        if key_code is not None and self.key_state.get(key_code, False):
            return True

        # Check mouse mapping
        mouse_code = mapping.get("mouse")
        if mouse_code is not None and self.mouse_state.get(mouse_code, False):
            return True

        # Action not active
        return False

    def clear_local_callbacks(self):
        """
        Remove all local callbacks.
        """
        for event_type in ["key_down", "key_up", "mouse_down", "mouse_up"]:
            self.bindings["local"][event_type].clear()

    def clear_all_callbacks(self):
        """
        Remove all callbacks.
        """
        self.clear_local_callbacks()
        for scope in ["local", "global"]:
            for event_type in ["key_down", "key_up", "mouse_down", "mouse_up"]:
                self.bindings[scope][event_type].clear()

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
        print()

    """
    Operations
        events
    """
    def events(self, event):
        """
        Process components events.
        """
        # Determine event
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            code = event.key
            state = event.type == pygame.KEYDOWN
            event_type = "key_down" if state else "key_up"
            state_dict = self.key_state
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            code = event.button
            state = event.type == pygame.MOUSEBUTTONDOWN
            event_type = "mouse_down" if state else "mouse_up"
            state_dict = self.mouse_state
        else:
            return

        # Binding
        if code in self.bindings["local"][event_type]:
            self.bindings["local"][event_type][code]()
        elif code in self.bindings["global"][event_type]:
            self.bindings["global"][event_type][code]()

        # Mapping
        state_dict[code] = event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)
