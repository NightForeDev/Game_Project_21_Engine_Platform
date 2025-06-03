import pygame

class InputManager:
    def __init__(self):
        self.key_bindings = {}
        self.active_keys = set()

    def bind_key(self, key, callback):
        self.key_bindings[key] = callback

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_bindings:
                self.key_bindings[event.key]()
                self.active_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.active_keys.discard(event.key)
