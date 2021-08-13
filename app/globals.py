import json
import os

from mongoengine import connect

from .reverse_geocoding import GoogleGeocoder


def _load_config() -> dict:
    config_file_path = os.getenv("CONFIG_FILE_PATH", "app/config.json")
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


app_config = _load_config()
mongo_config = app_config.get("db")
reverse_geocoding_config = app_config.get("reverse_geocoding")

reverse_geocoder = GoogleGeocoder(**reverse_geocoding_config)

connect(**mongo_config)
