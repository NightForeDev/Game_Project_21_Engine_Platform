# data\launcher\main.py

from .scenes.initial_scene import InitialScene
from engine.core import Core

def main():
    game = Core(InitialScene)
    game.run()
