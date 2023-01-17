import pygame

from core import ResourceManager
from rooms import MainMenu
from utils import init_from_config


def main():
    manager = ResourceManager()
    config = manager.get_config()
    room = init_from_config(config, MainMenu)

    common_params = config['Common']
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                room.handle_event(event)

        delta_time = clock.tick(common_params['fps']) / 1000  # seconds
        room.step(delta_time)

        screen.fill('black')
        room.render(screen)
        pygame.display.flip()

        room = room.get_next_room()
        if room is None:
            running = False


if __name__ == '__main__':
    main()
