import pygame

class InputManager:
    def __init__(self):
        self.key_bindings = {}   # action -> key
        self.key_states = {}     # key -> bool (pressed)
        self.callbacks = {}      # key -> function
        self.action_to_key = {}
        self.key_to_action = {}

    def bind_key(self, key, callback):
        self.callbacks[key] = callback

    def clear_callbacks(self):
        self.callbacks.clear()

    def map_action(self, action_name, key):
        old_key = self.action_to_key.get(action_name)
        if old_key:
            self.key_to_action.pop(old_key, None)

        self.key_bindings[action_name] = key
        self.action_to_key[action_name] = key
        self.key_to_action[key] = action_name

    def is_action_active(self, action_name):
        key = self.key_bindings.get(action_name)
        return self.key_states.get(key, False) if key else False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_states[event.key] = True
            if event.key in self.callbacks:
                self.callbacks[event.key]()
        elif event.type == pygame.KEYUP:
            self.key_states[event.key] = False
