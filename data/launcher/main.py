# data\launcher\main.py

from .scenes.initial_scene import InitialScene
from engine.config_loader import load_config
from engine.core import Core

def main():
    config = load_config()
    game = Core(InitialScene, config)
    game.run()
