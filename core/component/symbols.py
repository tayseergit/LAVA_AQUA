# core/constants/symbols.py

# Map symbols
SYMBOLS = {
    "WALL": "#",
    "PLAYER": "●",
    "WATER_PLAYER": "⋆",
    "FIRE": "▲",
    "GOAL": "■",
    "EMPTY": "-",
    "WATER": "◘",
    "WATER_BALL": " ",
    "SINGLE_WALL":"◙",
    "SIMI_WALL_FIRE": "sF",
    "SIMI_WALL_WATER": "sW",
    "NUMBER_WALL": lambda n: str(n),
    "SIMI_WALL":"◌",
    "BUNUS":"◊",
    "MIXED":" "
}

# Colors (RGB)
COLORS = {
    SYMBOLS["WALL"]: (100, 200, 225),        # Wall
    SYMBOLS["PLAYER"]: (255, 165, 0),     # Player
    SYMBOLS["WATER_PLAYER"]: (255, 165, 0),     # Player
    SYMBOLS["FIRE"]: (255, 0, 0),         # Fire
    SYMBOLS["GOAL"]: (128, 0, 128),       # Goal
    SYMBOLS["EMPTY"]: (200, 200, 200),    # Free cell
    SYMBOLS["WATER"]: (60, 70, 200),      # Water
    SYMBOLS["WATER_BALL"]: (60, 70, 200),     # Player
    SYMBOLS["SINGLE_WALL"]: (120, 120, 120),      # wall
    SYMBOLS["NUMBER_WALL"]: (0, 200, 0),      # wall
    SYMBOLS["SIMI_WALL"]: (50, 150, 50),    
    SYMBOLS["SIMI_WALL_FIRE"]: (50, 150, 50),    
    SYMBOLS["SIMI_WALL_WATER"]: (50, 150, 50),     
    SYMBOLS["BUNUS"]: (128, 0, 128),    
}
DIRECTION = {
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "UP": (-1, 0),
    "RIGHT": (0, 1)
}
FIRE_SYMBOLS = {SYMBOLS["FIRE"], SYMBOLS["SIMI_WALL_FIRE"]}
WATER_SYMBOLS = {SYMBOLS["WATER"], SYMBOLS["SIMI_WALL_WATER"]}
