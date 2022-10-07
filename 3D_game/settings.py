import math

# game settings
WIDTH = 1000
HEIGHT = 600
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 50
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 333
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 2 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# sprite settings
DOUBLE_PI = math.pi * 2
CENTER_RAY = NUM_RAYS // 2 - 1


# texture settings (W * W)
TEXTURE_WIDTH = 1000
TEXTURE_HEIGHT = 1000
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# player settings
player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 2

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
YELLOW = (220, 220, 0)
BLUE = (0, 0, 220)
DARKGREY = (100, 80, 90)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
