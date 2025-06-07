import os

# Basic names and identifiers
DEFAULT_STARTUP_APP_NAME = "launcher"       # Default app to run (via run.py)
DEFAULT_APP_FILE_NAME = "main"              # Name of the main Python file for each app
CONFIG_FILENAME = "config.json"             # Standard config file name

# Folder names
DATA_FOLDER = "data"                        # Folder for all apps
SHARED_FOLDER = "shared"                    # Subfolder under DATA_FOLDER for shared assets/configs

# Absolute paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(PROJECT_ROOT, DATA_FOLDER)
SHARED_PATH = os.path.join(DATA_PATH, SHARED_FOLDER)
SHARED_CONFIG_PATH = os.path.join(SHARED_PATH, CONFIG_FILENAME)
