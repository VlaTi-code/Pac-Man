'''Utility functions'''

import logging
import os
from pathlib import Path
import random
import sys
from typing import Any

import pygame
import yaml


logger = logging.getLogger(__name__)


__all__ = (
    'TOP_LEFT_CORNER',
    'LEFT_MB',
    'EPS',

    'parse_config',
    'init_from_config',

    'ignore_callback',
    'singleton',

    'get_random',
    'roll_dice',
    'draw_text',
    'draw_sprite',

    'load_font',
    'load_image',
    'load_sound',
    'load_sprite',
    'load_level',
)


Color = tuple[int, int, int]
ConfigType = dict[str, Any]
Font = pygame.font.Font
Image = pygame.surface.Surface
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


TOP_LEFT_CORNER = -1
LEFT_MB = 1
EPS = 1e-2


def parse_config(path: str | Path) -> ConfigType:
    '''
    Safely parse a YAML config

    :param path: path to a configuration file
    '''

    with open(path) as file:
        return yaml.safe_load(file)


def init_from_config(config: ConfigType, cls: type, **kwargs: Any) -> Any:
    '''
    Instantiate a class using config data

    :param config: a config object
    :param cls: a class to be instantiated
    '''

    return cls(**config.get(cls.__name__, {}), **kwargs)


def ignore_callback(*args: Any, **kwargs: Any) -> None:
    '''An empty callback mock'''

    pass


def singleton(cls: type) -> type:
    '''A singleton decorator for classes'''

    instances: dict[type, Any] = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper  # type: ignore


def get_random(from_: float, to: float) -> float:
    '''
    Generate a random float number uniformly from an interval [from; to)

    :param from_: lower interval bound
    :param to: upper interval bound
    '''

    return from_ + (to - from_) * random.random()


def roll_dice(prob: float) -> bool:
    '''
    Draw a Bernoulli distributed r.v.

    :param prob: parameter p of Be(p) distribution
    '''

    return random.random() < prob


def draw_text(screen: Image,
              font: Font,
              text: str,
              color: Color | str,
              pos: tuple[int, int],
              *,
              centered: bool = True,
              ) -> None:
    '''
    Render a text on a screen

    :param screen: surface to render the text on
    :param font: font object
    :param text: single-line text to render
    :param color: text color
    :param pos: position of the text to render (top left or center)
    :param centered: whether to treat pos as a center or as a top left coordinate of text object
    '''

    eff_color = pygame.Color(color) if isinstance(color, str) else color
    rendered = font.render(text, True, eff_color)  # type: ignore
    x, y = pos
    if centered:
        width, height = rendered.get_rect().size
        x -= width // 2
        y -= height // 2
    screen.blit(rendered, (x, y))


def draw_sprite(screen: Image, sprite: Sprite) -> None:
    '''
    Render a single sprite on a screen

    :param screen: surface to draw the sprite on
    :param sprite: sprite to render
    '''

    screen.blit(sprite.image, sprite.rect)  # type: ignore


def load_sound(path: str | Path) -> Sound:
    '''
    Sound loader function

    :param path: path to a source file to load
    '''

    if not os.path.isfile(path):
        logger.error('Sound source %s not found.', path)
        sys.exit(1)
    return Sound(path)


def load_image(path: str | Path,
               colorkey: Color | int | None = None,
               ) -> Image:
    '''
    Souns loader function

    :param path: path to a source file to load
    :param colorkey: key of a color to cut off as a background (color or TOP_LEFT_CORNER const, optional)
    '''

    if not os.path.isfile(path):
        logger.error('Image source %s not found.', path)
        sys.exit(1)
    image = pygame.image.load(path)

    if colorkey is not None:
        image = image.convert()
        if colorkey == TOP_LEFT_CORNER:
            colorkey = image.get_at((0, 0))  # type: ignore
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image


def load_sprite(path: str | Path,
                colorkey: Color | int | None = None,
                xy: tuple[int, int] = (0, 0),
                ) -> Sprite:
    '''
    Sprite loader function

    :param path: path to a source file to load
    :param colorkey: key of a color to cut off as a background (color or TOP_LEFT_CORNER const, optional)
    :param xy: sprite top-left corner position
    '''

    sprite = Sprite()
    sprite.image = load_image(path, colorkey)
    sprite.rect = sprite.image.get_rect(topleft=xy)
    return sprite


def load_font(path: str | Path) -> Font:
    '''
    Font loader function

    :param path: path to a source file to load
    '''

    raise NotImplementedError()


def load_level(path: str | Path) -> list[str]:
    '''
    Level map loader function

    :param path: path to a source file to load
    '''

    with open(path, 'r', encoding='utf-8') as file:
        return [line.rstrip() for line in file]
