# data\platformer_game\main.py

from .scenes.initial_scene import InitialScene
from engine.core_manager import CoreManager

def main():
    CoreManager(InitialScene)
