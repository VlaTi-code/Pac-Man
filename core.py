import logging
import os
from pathlib import Path
from typing import Any, Callable

import attr
import pygame

from sprites import CursorSprite
from utils import *    # noqa


logger = logging.getLogger(__name__)


Event = pygame.event.EventType
Font = pygame.font.Font
Image = pygame.surface.Surface
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


__all__ = (
    'ResourceManager',
    'BaseRoom',
)


@singleton
class ResourceManager:
    def __init__(self, config_path: str | Path = 'configs/config.yml'):
        logger.warning('ResourceManager initialization')
        pygame.init()

        self.images: dict[str, Image] = {}
        self.sounds: dict[str, Sound] = {}
        self.sprites: dict[str, Sprite] = {}
        self.config = parse_config(config_path)

        screen_params = self.config['Screen']
        screen_size = screen_params['width'], screen_params['height']
        pygame.display.set_mode(screen_size)
        pygame.mouse.set_visible(False)

        self._load_folder('images', self.images, load_image)
        # self._load_folder('sounds', self.sounds, load_sound)
        self._load_folder('sprites', self.sprites, load_sprite)

    def _load_folder(self,
                     folder_name: str | Path,
                     target_dict: dict[str, Any],
                     loader: Callable) -> None:
        resources_path = self.config.get('resources_path', 'resources')  # TODO: populate resources/
        path = os.path.join(resources_path, folder_name)
        if os.path.isdir(path):
            for cur_dir, _, files in os.walk(path):
                for filename in files:
                    obj = loader(os.path.join(cur_dir, filename))
                    key = os.path.join(cur_dir[len(path) + 1:], filename)
                    target_dict[key] = obj
        else:
            logger.warning('Folder %s is missing', folder_name)

    def __attrs_post_init__(self):
        if self.__initialized:
            return

    def get_font(self, name: str, size: int) -> Font:
        return pygame.font.SysFont(name, size)

    def get_image(self, filename: str) -> Image:
        return self.images[filename]

    def get_sound(self, filename: str) -> Sound:
        return self.sounds[filename]

    def get_sprite(self, filename: str) -> Sprite:
        return self.sprites[filename]

    def get_config(self) -> dict[str, Any]:
        return self.config

    def __del__(self):
        logger.warning('ResourceManager destruction')
        pygame.quit()


@attr.s(slots=True, kw_only=True)
class BaseRoom:
    next_room: 'BaseRoom' = attr.ib(default=attr.Factory(lambda self: self, takes_self=True))
    sprites = attr.ib(factory=pygame.sprite.Group)

    background_name: str | Path = None
    cursor: CursorSprite = attr.ib(factory=CursorSprite)

    def __attrs_post_init__(self):
        manager = ResourceManager()
        background = manager.get_sprite(os.path.join('backgrounds', self.background_name))
        self.sprites.add(background)
        self.sprites.add(self.cursor)

    def handle_event(self, event: Event | None = None) -> None:
        self.sprites.update(event)

    def set_next_room(self, next_room: 'BaseRoom') -> None:
        self.next_room = next_room

    def get_next_room(self) -> 'BaseRoom':
        return self.next_room

    def step(self, delta_time: float) -> None:
        self.cursor.step(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        self.sprites.draw(screen)
