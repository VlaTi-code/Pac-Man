import pygame

from settings import *


class Wall(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = WALLS_NUMBERS[level_1_map[x][y]]
        self.rect = self.image.get_rect()
        self.rect.x = y * TILE
        self.rect.y = x * TILE

class Point(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = POINTS_NUMBERS[level_1_map[x][y]]
        self.rect = self.image.get_rect()
        self.rect.x = y * TILE
        self.rect.y = x * TILE


for x in range(len(level_1_map)):
    for y in range(len(level_1_map[0])):
        if level_1_map[x][y] not in '.-O ':
            Wall(all_sprites_1, x, y)
        if level_1_map[x][y] == '.' or level_1_map[x][y] == 'O':
            Point(points_sprites, x, y)
