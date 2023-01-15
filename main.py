import pygame

from core import ResourceManager
from rooms import MainMenu
from utils import init_from_config


def main():
    manager = ResourceManager()
    config = manager['config']
    room = init_from_config(config, MainMenu)

    common_params = config['Common']
    screen_params = config['Screen']
    screen_size = screen_params['width'], screen_params['height']

    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            room.handle_event(event)

        delta_time = clock.tick(common_params['fps'])
        room.step(delta_time)

        screen.fill('black')
        room.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
