# data\simple_game\main.py

from engine.core import Core
from data.simple_game.scenes.gameplay import GameplayScene

class Config:
    RESOLUTION = (640, 480)
    TITLE = "Simple Game"
    FPS = 60

def main():
    game = Core(GameplayScene, Config)
    game.run()

if __name__ == "__main__":
    main()
