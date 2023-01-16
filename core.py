import logging
import os
from pathlib import Path
from typing import Any, Callable

import attr
import pygame

from sprites import *  # noqa
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


class ResourceManager:  # TODO: separate Singleton into another utils.decorator
    __instance = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if cls.__instance is None:
            cls.__instance = super(ResourceManager, cls).__new__(cls, *args, *kwargs)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, config_path: str | Path = 'configs/config.yml'):
        if not self.__initialized:
            logger.warning('ResourceManager initialization')

            self.fonts: dict[str, Font] = {}
            self.images: dict[str, Image] = {}
            self.sounds: dict[str, Sound] = {}
            self.sprites: dict[str, Sprite] = {}
            self.config = parse_config(config_path)

            pygame.init()
            screen_params = self.config['Screen']
            screen_size = screen_params['width'], screen_params['height']
            pygame.display.set_mode(screen_size)

            self._load_folder('fonts', self.fonts, load_font)
            self._load_folder('images', self.images, load_image)
            self._load_folder('sounds', self.sounds, load_sound)
            self._load_folder('sprites', self.sprites, load_sprite)

            self.__initialized = True

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

    def get_font(self, filename: str) -> Font:
        return self.fonts[filename]

    def get_image(self, filename: str) -> Image:
        print(self.images.keys(), filename, filename in self.images)
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
    # TODO: cursor?

    def __attrs_post_init__(self):
        manager = ResourceManager()
        background = manager.get_sprite(os.path.join('backgrounds', self.background_name))
        self.sprites.add(background)

    def handle_event(self, event: Event | None = None) -> None:
        pass

    def set_next_room(self, next_room: 'BaseRoom') -> None:
        self.next_room = next_room

    def get_next_room(self) -> 'BaseRoom':
        return self.next_room

    def step(self, delta_time: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        self.sprites.draw(screen)
