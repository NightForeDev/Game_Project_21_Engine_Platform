# run.py

import sys
import importlib

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # First argument is the game/launcher folder name
        name = sys.argv[1]

        try:
            # Try to import the main.py module from the specified folder inside 'data'
            game_module = importlib.import_module(f"data.{name}.main")
            game_module.main()
        except ModuleNotFoundError:
            print(f"Module 'data.{name}.main' not found.")
        except AttributeError:
            print(f"'data.{name}.main' has no main() function.")
    else:
        # No args: launch the launcher by default
        try:
            launcher_module = importlib.import_module("data.launcher.main")
            launcher_module.main()
        except Exception as e:
            print(f"Failed to launch launcher: {e}")
