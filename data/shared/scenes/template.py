# data\shared\template.py

from engine.scene import Scene

class TemplateScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def update(self, dt):
        super().update(dt)

    def render(self, surface):
        super().render(surface)
