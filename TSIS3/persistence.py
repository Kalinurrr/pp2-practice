import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": False,
    "car_color": "red",
    "difficulty": "normal"
}

DIFFICULTY = {
    "easy": {
        "speed": 4,
        "traffic_chance": 0.012,
        "obstacle_chance": 0.008,
        "powerup_chance": 0.005
    },
    "normal": {
        "speed": 5,
        "traffic_chance": 0.018,
        "obstacle_chance": 0.012,
        "powerup_chance": 0.006
    },
    "hard": {
        "speed": 6,
        "traffic_chance": 0.025,
        "obstacle_chance": 0.018,
        "powerup_chance": 0.008
    }
}

CAR_COLORS = {
    "red": (231, 76, 60),
    "white": (245, 245, 245),
    "black": (30, 30, 30)
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except:
        settings = DEFAULT_SETTINGS.copy()

    for key in DEFAULT_SETTINGS:
        if key not in settings:
            settings[key] = DEFAULT_SETTINGS[key]

    if settings["car_color"] not in CAR_COLORS:
        settings["car_color"] = "red"

    if settings["difficulty"] not in DIFFICULTY:
        settings["difficulty"] = "normal"

    settings["sound"] = False
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except:
        pass

    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_score(name, score, distance, coins):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name if name else "Player",
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)
    leaderboard = leaderboard[:10]

    save_leaderboard(leaderboard)
    
    

