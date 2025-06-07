# engine\config_loader.py

import json
import inspect
import os
from collections.abc import Mapping

def deep_merge_dicts(a, b):
    """Recursively merge dict b into dict a (b overrides a)."""
    for key, value in b.items():
        if isinstance(value, Mapping) and key in a and isinstance(a[key], Mapping):
            deep_merge_dicts(a[key], value)
        else:
            a[key] = value
    return a

def load_config():
    # Detect folder of the caller
    caller_file = inspect.stack()[1].filename
    caller_dir = os.path.dirname(caller_file)

    config_path = os.path.join(caller_dir, "config.json")
    config = load_json(config_path)

    return config

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}
