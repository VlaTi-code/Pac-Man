import pygame


pygame.init()
# ALL THE GAME SETTINGS

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

# Player settings
PLAYER_IMAGES = {
    0: pygame.transform.scale(pygame.image.load("images/pacman_opened.png"), (25, 25)),
    1: pygame.transform.scale(pygame.image.load("images/pacman_closed.png"), (25, 25))
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
FPS = 60

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
