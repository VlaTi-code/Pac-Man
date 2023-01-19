'''Core module for resource management and BaseRoom description'''

import logging
import os
from pathlib import Path
from typing import Any, Callable

import attr
import pygame

from sprites import CursorSprite
from utils import *  # noqa


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
    '''Singleton manager over all game resources and config files'''

    def __init__(self, config_path: str | Path = 'configs/config.yml'):
        '''
        Initialization of ResourceManager instance

        :param config_path: path to a configuration file
        '''

        logger.warning('ResourceManager initialization')
        pygame.init()

        self.images: dict[str, Image] = {}
        self.sounds: dict[str, Sound] = {}
        self.sprites: dict[str, Sprite] = {}
        self.levels: dict[str, list[str]] = {}
        self.config = parse_config(config_path)

        screen_params = self.config['Screen']
        screen_size = screen_params['width'], screen_params['height']
        pygame.display.set_mode(screen_size)
        pygame.mouse.set_visible(False)

        self._load_folder('images', self.images, load_image)
        # self._load_folder('sounds', self.sounds, load_sound)
        self._load_folder('sprites', self.sprites, load_sprite)
        self._load_folder('levels', self.levels, load_level)

    def _load_folder(self,
                     folder_name: str | Path,
                     target_dict: dict[str, Any],
                     loader: Callable) -> None:
        '''
        Helper function for autoloading a subfolder of resources/

        :param folder_name: name of a folder to be loaded
        :param target_dict: target attribute to be filled with data
        :param loader: object loading function
        '''

        resources_path = self.config.get('resources_path', 'resources')
        path = os.path.join(resources_path, folder_name)
        if os.path.isdir(path):
            for cur_dir, _, files in os.walk(path):
                for filename in files:
                    obj = loader(os.path.join(cur_dir, filename))
                    key = os.path.join(cur_dir[len(path) + 1:], filename)
                    target_dict[key] = obj
        else:
            logger.warning('Folder %s is missing', folder_name)

    def get_font(self, font_name: str, size: int) -> Font:
        '''
        Returns a font object

        :param font_name: fontname
        :param size: fontsize in points
        '''

        return pygame.font.SysFont(font_name, size)

    def get_image(self, image_name: str) -> Image:
        '''
        Returns an image (pygame.Surface)

        :param image_name: path to an image, relative to resources/images/ folder
        '''

        return self.images[image_name]

    def get_sound(self, sound_name: str) -> Sound:
        '''
        Returns a sound object

        :param sound_name: path to a sound, relative to resources/sounds/ folder
        '''

        return self.sounds[sound_name]

    def get_sprite(self, sprite_name: str) -> Sprite:
        '''
        Returns a sprite object

        :param sprite_name: path to a sprite image, relative to resources/sprites/ folder
        '''

        return self.sprites[sprite_name]

    def get_level_map(self, level_name: str) -> list[str]:
        '''
        Returns a level text map

        :param level_name: path to a map file, relative to resources/levels/ folder
        '''

        return self.levels[level_name]

    def get_config(self) -> dict[str, Any]:
        '''
        Returns parsed YAML configuration object
        '''

        return self.config

    def __del__(self):
        '''
        Destruction of ResourceManager instance
        '''

        logger.warning('ResourceManager destruction')
        pygame.quit()


@attr.s(slots=True, kw_only=True)
class BaseRoom:
    '''
    Base class for all rooms (menus and levels)
    '''

    background_name: str | Path = attr.ib(default=None)

    next_room: 'BaseRoom' = attr.ib(
        default=attr.Factory(lambda self: self, takes_self=True),
        init=False,
    )
    sprites = attr.ib(factory=pygame.sprite.Group, init=False)
    cursor: CursorSprite = attr.ib(factory=CursorSprite, init=False)

    def __attrs_post_init__(self):
        '''
        Post-initialization
        '''

        manager = ResourceManager()
        background = manager.get_sprite(os.path.join('backgrounds', self.background_name))
        self.sprites.add(background)
        self.sprites.add(self.cursor)

    def handle_event(self, event: Event | None = None) -> None:
        '''
        Event handler method

        :param event: an event to handle (optional)
        '''

        self.sprites.update(event)

    def set_next_room(self, next_room: 'BaseRoom') -> None:
        '''
        Set the next room to show

        :param next_room: room object
        '''

        self.next_room = next_room

    def get_next_room(self) -> 'BaseRoom':
        '''
        Returns the next room to show

        :returns: room object
        '''

        return self.next_room

    def step(self, delta_time: float) -> None:
        '''
        Update internal objects' state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        self.cursor.step(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        '''
        Drawing method

        :param screen: a surface to draw the room on
        '''

        self.sprites.draw(screen)
