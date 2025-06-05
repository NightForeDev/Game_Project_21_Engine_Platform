# engine\input_manager.py

import pygame

class InputManager:
    def __init__(self):
        self.key_bindings = {}      # action -> key
        self.key_states = {}        # key -> bool (pressed)
        self.key_callbacks = {}     # key -> function

        self.mouse_bindings = {}
        self.mouse_states = {}
        self.mouse_callbacks = {}

        self.action_to_key = {}
        self.key_to_action = {}

    def bind_key(self, key, callback):
        self.key_callbacks[key] = callback

    def bind_mouse(self, button, callback):
        self.mouse_callbacks[button] = callback

    def clear_callbacks(self):
        self.key_callbacks.clear()
        self.mouse_callbacks.clear()

    def map_key(self, action_name, key):
        old_key = self.action_to_key.get(action_name)
        if old_key:
            self.key_to_action.pop(old_key, None)

        self.key_bindings[action_name] = key
        self.action_to_key[action_name] = key
        self.key_to_action[key] = action_name

    def is_action_active(self, action_name):
        # Check keys
        key = self.key_bindings.get(action_name)
        if key is not None:
            return self.key_states.get(key, False)

        # Check mouse buttons
        button = self.mouse_bindings.get(action_name)
        if button is not None:
            return self.mouse_states.get(button, False)

    def handle_event(self, event):
        # Check key events
        if event.type == pygame.KEYDOWN:
            self.key_states[event.key] = True
            if event.key in self.key_callbacks and self.key_callbacks[event.key]:
                self.key_callbacks[event.key]()
        elif event.type == pygame.KEYUP:
            self.key_states[event.key] = False

        # Check mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_states[event.button] = True
            if event.button in self.mouse_callbacks and self.mouse_callbacks[event.button]:
                self.mouse_callbacks[event.button]()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_states[event.button] = False
