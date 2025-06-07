# engine\core.py

import pygame
from engine.config_loader import load_config
from engine.window_manager import WindowManager
from engine.input_manager import InputManager

class Core:
    def __init__(self, initial_scene_class):
        pygame.init()
        self.app_config = load_config()
        self.config = self.app_config[self.__class__.__name__]

        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = None
        self.previous_scene = None


        self.fps = self.config["fps"]

        self.window_manager = WindowManager(self.app_config)
        self.input_manager = InputManager()

        self.setup_shortcuts()
        self.current_scene = initial_scene_class(self)

    def setup_shortcuts(self):
        self.input_manager.bind_key(pygame.K_ESCAPE, self.quit_game)
        self.input_manager.bind_key(pygame.K_F11, self.window_manager.toggle_fullscreen)
        self.input_manager.bind_key(pygame.K_F5, self.window_manager.toggle_maximize_restore)

    def change_scene(self, scene_class):
        self.previous_scene = self.current_scene
        self.current_scene = scene_class(self)

    def return_to_previous_scene(self):
        self.current_scene = self.previous_scene

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                self.input_manager.handle_event(event)

            self.current_scene.handle_events(events)
            self.current_scene.update(dt)
            self.window_manager.render(self.current_scene.render)

        pygame.quit()
