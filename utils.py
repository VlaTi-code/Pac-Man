import os
from pathlib import Path
import random
import sys
import typing

import pygame
import yaml


Color = tuple[int, int, int]
Font = pygame.font.Font
Image = pygame.surface.Surface
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


TOP_LEFT_CORNER = -1
LEFT_MB = 1


def parse_config(path: str | Path):
    with open(path) as file:
        return yaml.safe_load(file)


def init_from_config(config, cls: type):
    return cls(**config.get(cls.__name__, {}))


def ignore_callback(*args: typing.Any, **kwargs: typing.Any) -> None:
    pass


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


def render_text(screen: Image,
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


def load_sound(filename: str | Path) -> Sound:
    path = resource_path(os.path.join('sounds', filename))
    if not os.path.isfile(path):
        print(f'Файл со звуком {path} не найден.')
        sys.exit(1)
    return Sound(path)


def load_image(filename: str | Path,
               colorkey: Color | int | None = None,
               ) -> Image:
    path = resource_path(os.path.join('images', filename))
    if not os.path.isfile(path):
        print(f'Файл с изображением {path} не найден.')
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


def load_sprite(filename: str | Path,
                colorkey: Color | int | None = None,
                xy: tuple[int, int] = (0, 0),
                ) -> Sprite:
    sprite = Sprite()
    sprite.image = load_image(filename, colorkey)
    sprite.rect = sprite.image.get_rect(topleft=xy)
    return sprite
