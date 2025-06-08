# engine/input_manager.py

import pygame

class InputManager:
    def __init__(self):
        # Global key/button callbacks
        self.global_key_down_callbacks = {}     # key -> function
        self.global_key_up_callbacks = {}       # key -> function
        self.global_mouse_down_callbacks = {}   # button -> function
        self.global_mouse_up_callbacks = {}     # button -> function

        # Local key/button callbacks
        self.key_down_callbacks = {}            # key -> function
        self.key_up_callbacks = {}              # key -> function
        self.mouse_down_callbacks = {}          # button -> function
        self.mouse_up_callbacks = {}            # button -> function

        # Action bindings
        self.action_to_key = {}                 # action -> key
        self.action_to_mouse = {}               # action -> button

        # Key/button states (held)
        self.key_state = {}                     # key -> held
        self.mouse_state = {}                   # button -> held

    def clear_callbacks(self):
        """Remove local callbacks."""
        self.key_down_callbacks.clear()
        self.key_up_callbacks.clear()
        self.mouse_down_callbacks.clear()
        self.mouse_up_callbacks.clear()

    def clear_all_callbacks(self):
        """Remove all callbacks."""
        self.clear_callbacks()
        self.global_key_down_callbacks.clear()
        self.global_key_up_callbacks.clear()

    """
    Global callbacks
    """
    def bind_key_down_global(self, key, callback):
        """Bind global callback to key press."""
        self.global_key_down_callbacks[key] = callback

    def bind_key_up_global(self, key, callback):
        """Bind global callback to key release."""
        self.global_key_up_callbacks[key] = callback

    def bind_mouse_down_global(self, button, callback):
        """Bind global callback to mouse press."""
        self.global_mouse_down_callbacks[button] = callback

    def bind_mouse_up_global(self, button, callback):
        """Bind global callback to mouse release."""
        self.global_mouse_up_callbacks[button] = callback

    """
    Local callbacks
    """
    def bind_key_down(self, key, callback):
        """Bind local callback to key press."""
        self.key_down_callbacks[key] = callback

    def bind_key_up(self, key, callback):
        """Bind local callback to key release."""
        self.key_up_callbacks[key] = callback

    def bind_mouse_down(self, button, callback):
        """Bind local callback to mouse press."""
        self.mouse_down_callbacks[button] = callback

    def bind_mouse_up(self, button, callback):
        """Bind local callback to mouse release."""
        self.mouse_up_callbacks[button] = callback

    """
    Key/Button states
    """
    def map_action_to_key(self, action, key):
        """Map action to a keyboard key."""
        self.action_to_key[action] = key

    def map_action_to_mouse(self, action, button):
        """Map action to a mouse button."""
        self.action_to_mouse[action] = button

    def is_action_active(self, action):
        """Check if the key or mouse button bound to an action is currently held down."""
        key = self.action_to_key.get(action)
        if key is not None and self.key_state.get(key, False):
            return True

        button = self.action_to_mouse.get(action)
        if button is not None and self.mouse_state.get(button, False):
            return True

        return False

    """
    Event handling
    """
    def handle_event(self, event):
        """Handle pygame input events."""
        if event.type == pygame.KEYDOWN:
            # Key state
            self.key_state[event.key] = True

            # Global callback
            if event.key in self.global_key_down_callbacks:
                self.global_key_down_callbacks[event.key]()

            # Local callback
            if event.key in self.key_down_callbacks:
                self.key_down_callbacks[event.key]()

        elif event.type == pygame.KEYUP:
            # Key state
            self.key_state[event.key] = False

            # Global callback
            if event.key in self.global_key_up_callbacks:
                self.global_key_up_callbacks[event.key]()

            # Local callback
            if event.key in self.key_up_callbacks:
                self.key_up_callbacks[event.key]()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Button state
            self.mouse_state[event.button] = True

            # Global callback
            if event.button in self.global_mouse_down_callbacks:
                self.global_mouse_down_callbacks[event.button]()

            # Local callback
            if event.button in self.mouse_down_callbacks:
                self.mouse_down_callbacks[event.button]()

        elif event.type == pygame.MOUSEBUTTONUP:
            # Button state
            self.mouse_state[event.button] = False

            # Global callback
            if event.button in self.global_mouse_up_callbacks:
                self.global_mouse_up_callbacks[event.button]()

            # Local callback
            if event.button in self.mouse_up_callbacks:
                self.mouse_up_callbacks[event.button]()
