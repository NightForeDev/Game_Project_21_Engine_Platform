# data\platformer_game\main.py

from .scenes.initial_scene import InitialScene
from engine.core import Core

def main():
    Core(InitialScene)
