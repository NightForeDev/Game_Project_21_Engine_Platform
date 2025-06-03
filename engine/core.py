import pygame

class Game:
    def __init__(self, initial_scene_class, config):
        pygame.init()
        self.screen = pygame.display.set_mode(config.RESOLUTION)
        pygame.display.set_caption(config.TITLE)
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
            self.current_scene.render(self.screen)
            pygame.display.flip()

        pygame.quit()
