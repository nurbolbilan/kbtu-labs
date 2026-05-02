import json

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "default",
    "difficulty": "normal"
}

def load_data(filename, default):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def update_leaderboard(name, score, distance, coins=0):
    leaderboard = load_data("leaderboard.json", [])
    leaderboard.append({
        "name": name,
        "score": score,
        "distance": int(distance),
        "coins": coins
    })
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_data("leaderboard.json", leaderboard)

def load_settings():
    settings = load_data("settings.json", DEFAULT_SETTINGS.copy())
    for k, v in DEFAULT_SETTINGS.items():
        if k not in settings:
            settings[k] = v
    return settings

def save_settings(settings):
    save_data("settings.json", settings)