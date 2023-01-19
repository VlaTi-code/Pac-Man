'''Buttons classes'''

import os

import attr
import pygame

from core import *  # noqa
import rooms
from sprites import ButtonSprite
from utils import draw_text, draw_sprite, init_from_config


Event = pygame.event.EventType  # type: ignore
Image = pygame.surface.Surface
Rect = pygame.rect.Rect
Sprite = pygame.sprite.Sprite


__all__ = (
    'PlayButton',
    'SettingsButton',
    'SkinsButton',
    'AboutButton',
    'QuitButton',
    'BackButton',

    'LevelButton',
)


@attr.s(slots=True, kw_only=True)
class TransitionButton(BaseButton):
    '''Base class for buttons switching current room'''

    room: BaseRoom = attr.ib()
    source_name: str = attr.ib()
    xy: tuple[int, int] = attr.ib()
    handle_escape: bool = attr.ib(default=False)

    next_room_type: type = None  # type: ignore

    def _on_click(self) -> None:
        '''
        Callback for click event
        '''

        manager = ResourceManager()
        config = manager.get_config()
        next_room = init_from_config(config, self.next_room_type)
        self.room.set_next_room(next_room)

    def __attrs_post_init__(self) -> None:
        '''
        Post-initialization
        '''

        manager = ResourceManager()
        sheet = manager.get_image(os.path.join('buttons', self.source_name))
        self.sprite = ButtonSprite(
            sheet=sheet,
            xy=self.xy,
            on_click=self._on_click,
            handle_escape=self.handle_escape,
        )


@attr.s(slots=True, kw_only=True)
class PlayButton(TransitionButton):
    '''Button for opening level menu'''

    next_room_type: type = rooms.LevelMenu


@attr.s(slots=True, kw_only=True)
class SettingsButton(TransitionButton):
    '''Button for opening Settings room'''

    next_room_type: type = rooms.SettingsMenu


@attr.s(slots=True, kw_only=True)
class SkinsButton(TransitionButton):
    '''Button for opening skins choosing menu'''

    next_room_type: type = rooms.SkinsMenu


@attr.s(slots=True, kw_only=True)
class AboutButton(TransitionButton):
    '''Button for opening About section'''

    next_room_type: type = rooms.AboutMenu


@attr.s(slots=True, kw_only=True)
class QuitButton(TransitionButton):
    '''Button for running away (ahh)'''

    next_room_type: type = type(None)


@attr.s(slots=True, kw_only=True)
class BackButton(TransitionButton):
    '''Button for getting back to main menu'''

    next_room_type: type = rooms.MainMenu


@attr.s(slots=True, kw_only=True)
class LevelButton(TransitionButton):
    '''Base class for all level choosing buttons'''

    level_idx: int = None  # type: ignore

    def draw(self, screen: Image) -> None:
        '''
        Drawing method

        :param screen: a surface to draw the button on
        '''

        super().draw(screen)

        manager = ResourceManager()
        font = manager.get_font('Chessmaster X', 36)

        pos = pygame.mouse.get_pos()
        rect: Rect = self.sprite.rect  # type: ignore
        color = 'white' if rect.collidepoint(pos) else 'gray'
        draw_text(screen, font, str(self.level_idx), color, rect.center)
