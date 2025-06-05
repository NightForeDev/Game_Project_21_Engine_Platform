# data\platformer_game\main.py

from engine.core import Core
from data.platformer_game.scenes.gameplay import GameplayScene

class Config:
    RESOLUTION = (640, 480)
    TITLE = "Simple Platformer"
    FPS = 60

def main():
    game = Core(GameplayScene, Config)
    game.run()

if __name__ == "__main__":
    main()
