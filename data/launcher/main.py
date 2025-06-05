# data\launcher\main.py

from engine.core import Core
from data.launcher.scenes.launcher_scene import LauncherScene

class Config:
    RESOLUTION = (640, 480)
    TITLE = "Launcher"
    FPS = 60

def main():
    game = Core(LauncherScene, Config)
    game.run()

if __name__ == "__main__":
    main()
