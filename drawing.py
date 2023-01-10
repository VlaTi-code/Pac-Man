import pygame
from settings import *
from button import Button


pygame.init()


class Drawing(object):
    def __init__(self, screen):
        self.screen = screen

    def drawing_main_menu(self, color_count):
        text_surface = pygame.Surface((WIDTH, 275))
        font = pygame.font.Font(None, 100)
        text_pm = font.render("Pac-Man", True, (color_count, 0, 0))
        pos = text_pm.get_rect(center=(WIDTH // 2, 275 // 2))
        text_surface.blit(text_pm, pos)
        self.screen.blit(text_surface, (0, 0))

    def drawing_level_menu(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 80)
        text_surface = pygame.Surface((WIDTH, 175))
        text_chl = font.render("Choose level", True, WHITE)
        pos = text_chl.get_rect(center=(WIDTH // 2, 175 // 2))
        text_surface.blit(text_chl, pos)
        self.screen.blit(text_surface, (0, 0))

    def drawing_button(self, button):
        button_surface = pygame.Surface((button.width, button.height))
        pygame.draw.rect(button_surface, button.color, (0, 0, button.width, button.height), 5, button.rounding)
        font = pygame.font.SysFont('arial', 20)
        text_button = font.render(button.text, True, button.color_text)
        pos = text_button.get_rect(center=(button.width // 2, button.height // 2 - 1))
        button_surface.blit(text_button, pos)
        self.screen.blit(button_surface, (button.x, button.y))

    def drawing_settings(self):
        pass

    def drawing_pause(self):
        pass

    def drawing_map(self, walls_map_level, points_map_level):
        self.screen.fill(BLACK)
        for i in walls_map_level:
            self.screen.blit(WALLS_NUMBERS[i[2]], (i[0], i[1]))

    def drawing_player(self, player):
        img = pygame.transform.scale(PLAYER_IMAGES[int((player.x + player.y)) % 2], (20, 20))
        pos = img.get_rect(center=(TILE // 2, TILE // 2))
        player.surface.blit(img, pos)
        self.screen.blit(player.surface, (player.x, player.y))
