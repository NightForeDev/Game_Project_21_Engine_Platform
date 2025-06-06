import sys
import importlib
import traceback

def run_game_or_launcher(name):
    try:
        game_module = importlib.import_module(f"data.{name}.main")
    except ModuleNotFoundError as e:
        print(f"ERROR: Module 'data.{name}.main' not found.\n{e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to import 'data.{name}.main':\n{traceback.format_exc()}")
        return False

    if not hasattr(game_module, "main"):
        print(f"ERROR: Module 'data.{name}.main' does not have a 'main()' function.")
        return False

    try:
        game_module.main()
    except Exception as e:
        print(f"ERROR: Exception occurred while running 'data.{name}.main.main()':\n{traceback.format_exc()}")
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        success = run_game_or_launcher(name)
        if not success:
            print("Exiting due to previous errors.")
    else:
        # No args: launch the launcher by default
        success = run_game_or_launcher("launcher")
        if not success:
            print("Failed to launch the launcher, exiting.")
