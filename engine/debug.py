# engine\debug.py

import time

import pygame

from .draw_utils import draw_text

class Debug:
    def __init__(self, core):
        self.core = core
        self.visible = False
        self.fps = 0.0
        self._last_fps_update = time.time()
        self.font = None  # Lazy load if needed

    def toggle(self):
        self.visible = not self.visible

    def update(self):
        if time.time() - self._last_fps_update > 0.2:
            self.fps = self.core.clock.get_fps()
            self._last_fps_update = time.time()

    def draw(self, surface):
        if not self.visible:
            return
        if not self.font:
            self.font = pygame.font.SysFont("Consolas", 16)

        lines = [
            f"FPS: {self.fps:.1f}",
            f"Delta Time: {int(self.core.dt*1000)} ms",
            f"Scene: {type(self.core.current_scene).__name__}",
            f"Render Size: {self.core.window_manager.render_size}",
            f"Scaled Size: {self.core.window_manager.scaled_size}",
            f"Windowed Size: {self.core.window_manager.windowed_size}",
        ]
        for i, line in enumerate(lines):
            draw_text(surface, line, (10, 10 + i * 20), font=self.font)
