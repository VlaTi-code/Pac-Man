import pygame


pygame.init()
# ALL THE GAME SETTINGS

all_sprites_1 = pygame.sprite.Group()
points_sprites = pygame.sprite.Group()

level_1_map = [
    "b333333333333cb333333333333c",
    "2............42............4",
    "2.6117.61117.42.61117.6117.4",
    "2O4  2.4   2.42.4   2.4  2O4",
    "2.5338.53338.58.53338.5338.4",
    "2..........................4",
    "2.6117.67.61111117.67.6117.4",
    "2.5338.42.533cb338.42.5338.4",
    "2......42....42....42......4",
    "a11117.4a117 42 611d2.61111d",
    "     2.4b338 58 533c2.4     ",
    "     2.42          42.4     ",
    "     2.42 611--117 42.4     ",
    "333338.58 4      2 58.533333",
    "      .   4      2   .      ",
    "111117.67 4      2 67.611111",
    "     2.42 53333338 42.4     ",
    "     2.42          42.4     ",
    "     2.42 61111117 42.4     ",
    "b33338.58 533cb338 58.53333c",
    "2............42............4",
    "2.6117.61117.42.61117.6117.4",
    "2.53c2.53338.58.53338.4b38.4",
    "2O..42................42..O4",
    "a17.42.67.61111117.67.42.61d",
    "b38.58.42.533cb338.42.58.53c",
    "2......42....42....42......4",
    "2.61111da117.42.611da11117.4",
    "2.5333333338.58.5333333338.4",
    "2..........................4",
    "a11111111111111111111111111d"
]


# Walls textures
WALLS_NUMBERS = {
    '1': pygame.image.load("images/wall_up.png"),
    '2': pygame.image.load("images/wall_right.png"),
    '3': pygame.image.load("images/wall_down.png"),
    '4': pygame.image.load("images/wall_left.png"),
    '5': pygame.image.load("images/wall_turn_up-right.png"),
    '6': pygame.image.load("images/wall_turn_right-down.png"),
    '7': pygame.image.load("images/wall_turn_down-left.png"),
    '8': pygame.image.load("images/wall_turn_left-up.png"),
    'a': pygame.image.load("images/wall_corner_up-right.png"),
    'b': pygame.image.load("images/wall_corner_right-down.png"),
    'c': pygame.image.load("images/wall_corner_down-left.png"),
    'd': pygame.image.load("images/wall_corner_left-up.png")
}

POINTS_NUMBERS = {
    '.': pygame.image.load("images/small_point.png"),
    'O': pygame.image.load("images/big_point.png"),
}

# Player settings
PLAYER_ANIMATION = {
    0: pygame.transform.scale(pygame.image.load("images/pacman_opened.png"), (20, 20)),
    1: pygame.transform.scale(pygame.image.load("images/pacman_closed.png"), (20, 20))
}
player_speed = 3

# Main window settings
WIDTH_MAP = 700
HEIGHT_MAP = 775
WIDTH = 800
HEIGHT = 775
TILE = 20
HALF_HEIGHT_MAP = HEIGHT_MAP // 2
HALF_WIDTH_MAP = WIDTH_MAP // 2
FPS = 100

# Colors
BLINKY = (168, 22, 0)
PINKY = (216, 182, 242)
INKY = (63, 188, 250)
CLYDE = (232, 93, 13)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Button settings
WID = 200
HEI = 50
