import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()

def get_test_prompt_mode():
    return config.get("test_prompt_mode", "both").lower()

