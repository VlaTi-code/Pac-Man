import pygame
from settings import *


class Player:
    def __init__(self, pos, angle, map_level_walls, map_level_points, rect_list):
        self.x, self.y = pos
        self.angle = angle
        self.map_level_walls = map_level_walls
        self.map_level_points = map_level_points
        self.rect_list = rect_list
        self.surface = pygame.Surface((20, 20))

    def movement(self):
        keys = pygame.key.get_pressed()
        waiting_for_angle = -1

        if self.angle == 90:
            self.y -= player_speed
        elif self.angle == 180:
            self.x += player_speed
        elif self.angle == 270:
            self.y += player_speed
        elif self.angle == 0:
            self.x -= player_speed


