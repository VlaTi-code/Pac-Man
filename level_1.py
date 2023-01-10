import pygame
from settings import *
from drawing import Drawing
from player import Player


pygame.init()


def level_1_main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    drawer = Drawing(screen)
    player = Player((13.5 * TILE, 23 * TILE), 0, beta_walls_map_l1, points_map_l1, rect_list)  # !!!!!!!!!!!!!!

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        drawer.drawing_map(walls_map_l1, points_map_l1)
        drawer.drawing_player(player)
        # player.movement()

        pygame.display.flip()


map_text = [
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

points_map_l1 = set()
walls_map_l1 = set()
beta_walls_map_l1 = set()
rect_list = list()

for j, row in enumerate(map_text):
    for i, char in enumerate(row):
        if char == '.':
            points_map_l1.add((i * TILE, j * TILE))
        elif char in "12345678abcd":
            walls_map_l1.add((i * TILE, j * TILE, char))
            beta_walls_map_l1.add((i * TILE, j * TILE))
            rect = WALLS_NUMBERS[char].get_rect()
            rect_list.append(rect)
