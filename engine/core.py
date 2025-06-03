import pygame
from engine.window_manager import WindowManager  # import our new WindowManager class

class Game:
    def __init__(self, initial_scene_class, config):
        pygame.init()
        self.window = WindowManager(config.RESOLUTION[0], config.RESOLUTION[1], config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = initial_scene_class(self)
        self.config = config

    def run(self):
        while self.running:
            dt = self.clock.tick(self.config.FPS) / 1000
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_scene.handle_events(events)
            self.current_scene.update(dt)

            # Use window.draw() with the scene's render function
            # The render method should draw to the window's virtual surface
            self.window.draw(self.current_scene.render)

        pygame.quit()
