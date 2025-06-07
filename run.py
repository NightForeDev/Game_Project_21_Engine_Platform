# run.py

import sys
import importlib
import traceback

from data.shared.constants import DATA_FOLDER, DEFAULT_STARTUP_APP_NAME, DEFAULT_APP_FILE_NAME


def load_main_module(name):
    """Import the main module from a given game folder."""
    module_path = f"{DATA_FOLDER}.{name}.{DEFAULT_APP_FILE_NAME}"
    try:
        return importlib.import_module(module_path)
    except Exception:
        print(f"[ERROR] Unexpected error while importing '{module_path}':\n{traceback.format_exc()}")
    return None


def run_main_module(module, name):
    """Run the 'main()' function from the imported module."""
    try:
        module.main()
        return True
    except Exception:
        print(f"[ERROR] Exception occurred while running '{DATA_FOLDER}.{name}.{DEFAULT_APP_FILE_NAME}.main()':\n{traceback.format_exc()}")
    return False

def run(name):
    """Load and run the module."""
    module = load_main_module(name)
    run_main_module(module, name)


if __name__ == "__main__":
    target_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STARTUP_APP_NAME
    run(target_name)
