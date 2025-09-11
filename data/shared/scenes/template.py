# data\shared\template.py

from engine.base_scene import BaseScene

class TemplateScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

    def update(self, dt=None):
        super().update(dt)

    def render(self, surface=None):
        super().render(surface)
