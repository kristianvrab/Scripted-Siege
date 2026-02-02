WIDTH = 1280
HEIGHT = 720
FPS = 60
TILE_SIZE = 80
GRID_WIDTH = (WIDTH - 200) // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
STARTING_MONEY = 100
BASE_HP = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)
BLUE = (0, 150, 255)
ORANGE = (255, 100, 0)
CYAN = (0, 255, 255)
PURPLE = (180, 0, 255)

TOWER_TYPES = {
    "basic": {"cost": 10, "range": 200, "cooldown": 50, "color": BLUE, "label": "B"},
    "double": {"cost": 25, "range": 200, "cooldown": 30, "color": PURPLE, "label": "D"},
    "fire": {"cost": 35, "range": 150, "cooldown": 40, "color": ORANGE, "label": "F"},
    "freeze": {"cost": 30, "range": 150, "cooldown": 50, "color": CYAN, "label": "S"}
}
ENEMY_TYPES = {
    "soldier": {"hp": 51, "speed": 2.5, "dmg": 2, "reward": 4, "color": (0, 180, 0)},
    "vehicle": {"hp": 250, "speed": 3.5, "dmg": 10, "reward": 15, "color": (150, 150, 0)},
    "tank": {"hp": 500, "speed": 1.2, "dmg": 25, "reward": 60, "color": (50, 50, 50)},
    "boss": {"hp": 4719, "speed": 0.6, "dmg": 100, "reward": 500, "color": (255, 0, 255)}
}