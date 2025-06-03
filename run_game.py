# run_game.py
import os
import importlib

GAMES_FOLDER = "games"

def list_games():
    # List all directories inside games/
    return [name for name in os.listdir(GAMES_FOLDER) if os.path.isdir(os.path.join(GAMES_FOLDER, name))]

def run_game(name):
    try:
        game_module = importlib.import_module(f"{GAMES_FOLDER}.{name}.main")
        game_module.main()
    except ModuleNotFoundError:
        print(f"Game '{name}' not found.")
    except AttributeError:
        print(f"Game '{name}' has no main() function.")

if __name__ == "__main__":
    import sys
    available_games = list_games()
    if len(sys.argv) > 1 and sys.argv[1] in available_games:
        run_game(sys.argv[1])
    else:
        print("Usage: python run_game.py <game_name>")
        print("Available games:", available_games)
