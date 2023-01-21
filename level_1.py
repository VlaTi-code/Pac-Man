import pygame
from settings import *
from drawing import Drawing
from player import Player


def level_1_main():
    clock = pygame.time.Clock()
    player = Player(all_sprites_1, (270, 340))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 1")
    drawer = Drawing(screen)

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        drawer.drawing_level(1, player)
        drawer.drawing_fps(clock)
        player.update()
        pygame.display.flip()
        clock.tick(FPS)
