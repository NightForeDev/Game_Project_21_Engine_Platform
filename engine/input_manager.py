# engine/input_manager.py

import pygame
from engine.base_manager import BaseManager

class InputManager(BaseManager):
    """
    Manage input state, callback bindings, and action mappings.

    Constants:
        SCOPES (list[str]): Available binding scopes.
        DEVICES (list[str]): Available input devices.
        EVENT_TYPES (list[str]): Input event types.
        DEVICE_TO_EVENT (dict[str, tuple[str, str]]): Maps device to its down/up event types.

    Attributes:
        Input Attributes:
            bindings (dict): Stores all callback bindings by scope and event type.
            mappings (dict): Stores all action mappings by device type and input code.
            persisted_input (dict): Stores all bindings and mappings for persistence across reloads.
            input_state (dict[str, dict[int, bool]]): Current pressed state for all devices.

    Methods:
        Configuration:
            _setup(): Initialize components.
            load_config(config): Load settings from configuration.

        Input Handling:
            bind_callback(scope, event_type, code, callback): Bind a callback to an input event.
            map_action(action, device_type, code): Map an action to an input state.

        Input Utilities:
            is_action_active(action): Check if an action is currently active (held).
            clear_local_callbacks(): Remove all local callbacks.
            clear_all_callbacks(): Remove all callbacks.

        Debug:
            debug(): Print debug information.

        Operations:
            events(events): Process components events.
    """
    # Constants
    SCOPES = ["local", "global"]
    DEVICES = ["key", "mouse"]
    EVENT_TYPES = ["key_down", "key_up", "mouse_down", "mouse_up"]
    DEVICE_TO_EVENT = {
        "key": ("key_down", "key_up"),
        "mouse": ("mouse_down", "mouse_up")
    }

    def __init__(self, core_manager=None, app_config=None):
        # Input Attributes
        self.bindings = {scope: {event_type: {} for event_type in self.EVENT_TYPES} for scope in self.SCOPES}
        self.mappings = {}
        self.persisted_input = {"bind": [], "map": {}}
        self.input_state = {device: {} for device in self.DEVICES}

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
            # Extract info
            callback = bind["callback"]
            scope = "global" if bind.get("global", False) else "local"

            # Use persisted codes if they exist
            persisted_bind = next((b for b in self.persisted_input["bind"] if b.get("callback") == callback), {})

            # Apply bindings
            for event_type in self.EVENT_TYPES:
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

    """
    Input Handling
        bind_callback
        map_action
    """
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
        if scope not in self.SCOPES:
            raise ValueError(f"Invalid scope '{scope}', expected one of {self.SCOPES}.")
        if event_type not in self.EVENT_TYPES:
            raise ValueError(f"Invalid event '{event_type}', expected one of {self.EVENT_TYPES}.")
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
        if device_type not in self.DEVICES:
            raise ValueError(f"Invalid device '{device_type}', expected one of {self.DEVICES}.")

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
        Check if an action is currently active.

        Args:
            action (str): Name of the action.

        Returns:
            bool: True if mapped input is pressed, False otherwise.
        """
        # Get the mapping for the action
        mapping = self.mappings.get(action)
        if not mapping:
            return False

        # Check all mapped inputs
        for device_type, code in mapping.items():
            if self.input_state.get(device_type, {}).get(code, False):
                return True

        # Action not active
        return False

    def clear_local_callbacks(self):
        """
        Remove all local callbacks.
        """
        for event_type in self.EVENT_TYPES:
            self.bindings["local"][event_type].clear()

    def clear_all_callbacks(self):
        """
        Remove all callbacks.
        """
        for scope in self.SCOPES:
            for event_type in self.EVENT_TYPES:
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
        for device in self.DEVICES:
            print(f"Held {device.title()}s:", self.input_state[device])
        print()

    """
    Operations
        events
    """
    def events(self, event):
        """
        Process components events.
        """
        # Determine device type and code, set pressed state
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            device_type = "key"
            code = event.key
            state = event.type == pygame.KEYDOWN
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            device_type = "mouse"
            code = event.button
            state = event.type == pygame.MOUSEBUTTONDOWN
        else:
            return

        # Select event type based on state
        down_event, up_event = self.DEVICE_TO_EVENT[device_type]
        event_type = down_event if state else up_event

        # Execute first found callback
        for scope in self.SCOPES:
            callback = self.bindings[scope][event_type].get(code)
            if callback:
                callback()
                break

        # Update input state
        self.input_state[device_type][code] = state