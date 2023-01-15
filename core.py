import typing

import attr
import pygame

from sprites import *  # noqa


Event = pygame.event.EventType
Font = pygame.font.Font
Image = pygame.surface.Surface
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


__all__ = (
    'ResourceManager',
    'BaseRoom',
    'BaseButton',
)


@attr.s(slots=True, kw_only=True)
class ResourceManager:
    _instance = None

    # resource attributes
    fonts: dict[str, Image] = attr.ib(init=False)
    images: dict[str, Image] = attr.ib(init=False)
    sounds: dict[str, Image] = attr.ib(init=False)
    sprites: dict[str, Image] = attr.ib(init=False)

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls, *args, *kwargs)
        return cls._instance

    def __attrs_post_init__(self):
        # load resources; paths should be set in config file
        ...

    def __getitem__(self, key: str) -> typing.Any:  # is it really needed?
        raise NotImplementedError()

    def get_font(self, filename: str) -> Font:
        raise NotImplementedError()

    def get_image(self, filename: str) -> Image:
        raise NotImplementedError()

    def get_sound(self, filename: str) -> Sound:
        raise NotImplementedError()

    def get_sprite(self, filename: str) -> Sprite:
        raise NotImplementedError()


class BaseRoom:
    next_room: 'BaseRoom' = attr.ib(default=attr.Factory(lambda self: self, takes_self=True))

    def handle_event(self, event: Event | None = None) -> None:
        raise NotImplementedError()

    def get_next_room(self) -> 'BaseRoom':
        return self.next_room

    def step(self, delta_time: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        raise NotImplementedError()


class BaseButton:
    pass
