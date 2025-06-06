# engine\scene.py

class Scene:
    def __init__(self, game):
        self.game = game
        self.input_manager = game.input_manager
        self.window_manager = game.window_manager

    def quit_game(self):
        self.game.quit_game()

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass
