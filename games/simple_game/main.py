from engine.core import Game
from games.simple_game.scenes.gameplay import GameplayScene

class Config:
    RESOLUTION = (640, 480)
    TITLE = "Simple Game"
    FPS = 60

def main():
    game = Game(GameplayScene, Config)
    game.run()

if __name__ == "__main__":
    main()
