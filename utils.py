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
Font = pygame.font.Font
Image = pygame.surface.Surface
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


TOP_LEFT_CORNER = -1
LEFT_MB = 1
EPS = 1e-2


def parse_config(path: str | Path) -> Any:
    with open(path) as file:
        return yaml.safe_load(file)


def init_from_config(config, cls: type, **kwargs: Any) -> Any:
    return cls(**config.get(cls.__name__, {}), **kwargs)


def ignore_callback(*args: Any, **kwargs: Any) -> None:
    pass


def singleton(cls: type) -> type:
    instances: dict[type, Any] = {}

    def wrapper(*args: Any, **kwargs: Any):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


def get_random(from_: float, to: float) -> float:
    return from_ + (to - from_) * random.random()


def roll_dice(prob: float) -> bool:
    return random.random() < prob


def resource_path(relative_path: str | Path) -> Path:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return Path(os.path.join(base_path, relative_path))


def draw_text(screen: Image,
              font: Font,
              text: str,
              color: Color | str,
              pos: tuple[int, int],
              ) -> None:
    eff_color = pygame.Color(color) if isinstance(color, str) else color
    rendered = font.render(text, True, eff_color)
    width, height = rendered.get_rect().size
    x, y = pos
    screen.blit(rendered, (x - width // 2, y - height // 2))


def draw_sprite(screen: pygame.Surface, sprite: Sprite) -> None:
    screen.blit(sprite.image, sprite.rect)


def load_sound(path: str | Path) -> Sound:
    if not os.path.isfile(path):
        logger.error('Sound source %s not found.', path)
        sys.exit(1)
    return Sound(path)


def load_image(path: str | Path,
               colorkey: Color | int | None = None,
               ) -> Image:
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
    sprite = Sprite()
    sprite.image = load_image(path, colorkey)
    sprite.rect = sprite.image.get_rect(topleft=xy)
    return sprite


def load_font(path: str | Path) -> Font:
    raise NotImplementedError()


def load_level(level_map_path: str | Path) -> list[str]:
    with open(level_map_path, 'r', encoding='utf-8') as file:
        return [line.rstrip() for line in file]
