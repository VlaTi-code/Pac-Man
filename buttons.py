import os
from typing import Any

import attr
import pygame

from core import *  # noqa
import rooms
from sprites import ButtonSprite
from utils import draw_text, draw_sprite, init_from_config


Event = pygame.event.EventType
Sprite = pygame.sprite.Sprite


@attr.s(slots=True, kw_only=True)
class BaseButton(Sprite):
    sprite: ButtonSprite = attr.ib(default=None, init=False)

    def update(self, event: Event | None = None) -> None:
        self.sprite.update(event)

    def draw(self, screen: pygame.Surface) -> None:
        draw_sprite(screen, self.sprite)


@attr.s(slots=True, kw_only=True)
class TransitionButton(BaseButton):
    room: BaseRoom = attr.ib()
    source_name: str = attr.ib()
    xy: tuple[int, int] = attr.ib()
    handle_escape: bool = attr.ib(default=False)

    next_room_type: type = None

    def _set_next_room(self, **kwargs: Any) -> None:
        manager = ResourceManager()
        config = manager.get_config()
        next_room = init_from_config(config, self.next_room_type, **kwargs)
        self.room.set_next_room(next_room)

    def on_click(self) -> None:
        self._set_next_room()

    def __attrs_post_init__(self):
        manager = ResourceManager()
        sheet = manager.get_image(os.path.join('buttons', self.source_name))
        self.sprite = ButtonSprite(
            sheet=sheet,
            xy=self.xy,
            on_click=self.on_click,
            handle_escape=self.handle_escape,
        )


@attr.s(slots=True, kw_only=True)
class PlayButton(TransitionButton):
    next_room_type: type = rooms.LevelMenu


@attr.s(slots=True, kw_only=True)
class SettingsButton(TransitionButton):
    next_room_type: type = rooms.SettingsMenu


@attr.s(slots=True, kw_only=True)
class SkinsButton(TransitionButton):
    next_room_type: type = rooms.SkinsMenu


@attr.s(slots=True, kw_only=True)
class AboutButton(TransitionButton):
    next_room_type: type = rooms.AboutMenu


@attr.s(slots=True, kw_only=True)
class QuitButton(TransitionButton):
    next_room_type: type = type(None)


@attr.s(slots=True, kw_only=True)
class BackButton(TransitionButton):
    next_room_type: type = rooms.MainMenu


@attr.s(slots=True, kw_only=True)
class LevelButton(TransitionButton):
    level_idx: int = None

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)

        manager = ResourceManager()
        font = manager.get_font('Chessmaster X', 36)

        pos = pygame.mouse.get_pos()
        rect = self.sprite.rect
        color = 'white' if rect.collidepoint(pos) else 'gray'
        draw_text(screen, font, str(self.level_idx), color, rect.center)
