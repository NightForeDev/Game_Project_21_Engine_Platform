# engine\config_loader.py

import json
import inspect
import os
from collections.abc import Mapping

from data.shared.constants import CONFIG_FILENAME, SHARED_FOLDER


def deep_merge_dicts(a, b):
    """Recursively merge dict b into dict a (b overrides a)."""
    for key, value in b.items():
        if isinstance(value, Mapping) and key in a and isinstance(a[key], Mapping):
            deep_merge_dicts(a[key], value)
        else:
            a[key] = value
    return a

def load_config():
    # Detect folder of the caller (engine\config_loader.py -> engine\core.py -> data\{app}\main.py)
    caller_file = inspect.stack()[2].filename
    app_path = os.path.dirname(caller_file)

    # Load app-specific config
    local_config_path = os.path.join(app_path, CONFIG_FILENAME)
    local_config = load_json(local_config_path)

    # Load shared config (data/shared/config.json)
    data_root = os.path.dirname(app_path)
    shared_config_path = os.path.join(data_root, SHARED_FOLDER, CONFIG_FILENAME)
    shared_config = load_json(shared_config_path)

    # Merge shared into local (local overrides shared)
    return deep_merge_dicts(shared_config, local_config)

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}
