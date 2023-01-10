import pygame
from settings import *

pygame.init()


class Button:
    def __init__(self, position, width, height, text, rounding):
        self.x, self.y = position
        self.width = width
        self.height = height
        self.text = text
        self.color_text = GRAY
        self.color = GRAY
        self.rounding = rounding

    def motion(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        x_mouse, y_mouse = mouse_pos
        if self.x <= x_mouse <= self.x + WID and self.y <= y_mouse <= self.y + HEI:
            self.color = WHITE
            self.color_text = WHITE
        else:
            self.color = GRAY
            self.color_text = GRAY
        if (mouse_pressed[0] and
                self.x <= x_mouse <= self.x + self.width and self.y <= y_mouse <= self.y + self.height):
            return True
        return False
