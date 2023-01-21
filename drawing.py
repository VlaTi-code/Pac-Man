import pygame
from settings import *
from button import Button
from level_1_sprites import *


pygame.init()


class Drawing(object):
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)

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

    def drawing_level(self, level, player):
        if level == 1:
            points_sprites.draw(self.screen)
            all_sprites_1.draw(self.screen)
            pygame.draw.rect(self.screen, BLACK, (0, 265, 15, 50))
            pygame.draw.rect(self.screen, BLACK, (540, 265, 20, 50))
            pygame.draw.rect(self.screen, BLUE, (0, 0, 560, 620), 5)

            score = str(player.score)
            render = self.font.render(score, False, RED)
            self.screen.blit(render, (WIDTH - 100, 5))

    def drawing_fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, RED)
        self.screen.blit(render, (WIDTH - 40, 5))
