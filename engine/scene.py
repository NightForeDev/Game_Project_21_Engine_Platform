# engine\scene.py

class Scene:
    def __init__(self, game):
        self.game = game
        self.input_manager = game.input_manager

    def quit_game(self):
        self.game.quit_game()

    def update(self, dt):
        pass

    def render(self, surface):
        pass
