import json
import os

CONFIG_FILE = "providers.json"

def init_storage():
    """Ensures structure exists cleanly in root runspace."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump([], f)

def read_config():
    init_storage()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            # Fresh state allocation logic
            for entry in data:
                entry["depleted"] = False
            return data
    except Exception:
        return []

def write_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"\n[!] Storage compilation write error: {e}")
