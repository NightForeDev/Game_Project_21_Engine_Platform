import pygame
from engine.window_manager import WindowManager
from engine.input_manager import InputManager

class Game:
    def __init__(self, initial_scene_class, config):
        pygame.init()
        self.config = config
        self.clock = pygame.time.Clock()
        self.running = True

        self.window_manager = WindowManager(self.config.RESOLUTION[0], self.config.RESOLUTION[1], self.config.TITLE)
        self.input_manager = InputManager()

        self.setup_shortcuts()
        self.current_scene = initial_scene_class(self)

    def setup_shortcuts(self):
        self.input_manager.bind_key(pygame.K_ESCAPE, self.quit)
        self.input_manager.bind_key(pygame.K_F11, self.window_manager.toggle_fullscreen)
        self.input_manager.bind_key(pygame.K_F5, self.window_manager.toggle_maximize_restore)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(self.config.FPS) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                self.input_manager.handle_event(event)

            self.current_scene.handle_events(events)
            self.current_scene.update(dt)
            self.window_manager.draw(self.current_scene.render)

        pygame.quit()
