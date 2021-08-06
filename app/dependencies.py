import json
import os


def _load_config() -> dict:
    config_file_path = os.getenv("CONFIG_FILE_PATH", "app/default_config.json")
    with open(config_file_path, "r") as f:
        config = json.load(f)
    return config


app_config = _load_config()
mongo_config = app_config.get("db")
