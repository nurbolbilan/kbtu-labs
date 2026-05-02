import json
import os

SETTINGS_FILE = "settings.json"

# Default settings applied when no settings.json exists yet
DEFAULT_SETTINGS = {
    "snake_color": [0, 200, 0],   # RGB value for the snake body
    "grid_overlay": True,          # Whether to draw the background grid
    "sound": True,                 # Sound effects on/off (reserved for future use)
}

# Screen and grid constants
WIDTH      = 600   # Window width in pixels
HEIGHT     = 400   # Window height in pixels
BLOCK_SIZE = 20    # Size of one grid cell in pixels


def load_settings() -> dict:
    """Load settings from settings.json.
    Falls back to DEFAULT_SETTINGS if the file is missing or corrupted."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults so new keys are always present
                merged = DEFAULT_SETTINGS.copy()
                merged.update(data)
                return merged
        except (json.JSONDecodeError, IOError):
            # File is corrupted — start fresh with defaults
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict):
    """Persist settings to settings.json."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)