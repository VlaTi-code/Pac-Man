'''Room classes'''

from pathlib import Path

import attr
import pygame

from core import *   # noqa
from logic import *  # noqa
from utils import draw_text, init_from_config


__all__ = (
    'BaseMenu',
    'LevelRoom',

    'MainMenu',
    'LevelMenu',
    'SettingsMenu',
    'SkinsMenu',
    'AboutMenu',
)


Event = pygame.event.EventType  # type: ignore
Image = pygame.surface.Surface


@attr.s(slots=True, kw_only=True)
class BaseMenu(BaseRoom):
    '''Base class for all rooms with buttons'''

    buttons: list['BaseButton'] = attr.ib(factory=list)

    def handle_event(self, event: Event | None = None) -> None:
        '''
        Event handler method

        :param event: an event to handle (optional)
        '''

        super().handle_event(event)
        for button in self.buttons:
            button.handle_event(event)

    def render(self, screen: Image) -> None:
        '''
        Drawing method

        :param screen: a surface to draw the room on
        '''

        super().render(screen)
        for button in self.buttons:
            button.draw(screen)


@attr.s(slots=True, kw_only=True)
class MainMenu(BaseMenu):
    '''Main menu'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.PlayButton, room=self),
            init_from_config(config, buttons.SettingsButton, room=self),
            init_from_config(config, buttons.SkinsButton, room=self),
            init_from_config(config, buttons.AboutButton, room=self),
            init_from_config(config, buttons.QuitButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class LevelMenu(BaseMenu):
    '''Menu for choosing a level'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons
        import levels

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
            init_from_config(config, levels.LevelOneButton, room=self),
            init_from_config(config, levels.LevelTwoButton, room=self),
            init_from_config(config, levels.LevelThreeButton, room=self),
            init_from_config(config, levels.LevelFourButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class SettingsMenu(BaseMenu):
    '''Settings menu'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class SkinsMenu(BaseMenu):
    '''Menu for choosing skins'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class AboutMenu(BaseMenu):
    '''About section'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class LevelRoom(BaseMenu):
    '''Base class for all level rooms'''

    level_name: str | Path = None  # type: ignore

    board: Board = attr.ib(default=None, init=False)
    is_paused: bool = attr.ib(default=False, init=False)

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]

        self.board = init_from_config(config, Board, level_name=self.level_name)

    def handle_event(self, event: Event | None = None) -> None:
        '''
        Event handler method

        :param event: an event to handle (optional)
        '''

        super().handle_event(event)

        if event is None:
            return

        if event.type == pygame.KEYDOWN:
            if self.is_paused:
                self.is_paused = False
            elif event.key == pygame.K_p:
                self.is_paused = True
            else:
                pass

    def render(self, screen: Image) -> None:
        '''
        Drawing method

        :param screen: a surface to draw the room on
        '''

        super().render(screen)

        self.board.render(screen)

        manager = ResourceManager()
        font = manager.get_font('Chessmaster X', 48)
        center = screen.get_rect().center
        if self.is_paused:
            draw_text(screen, font, 'PAUSE (press any key to continue)', 'white', center)
        elif self.board.has_won():
            draw_text(screen, font, 'VICTORY!', 'green', center)
        elif self.board.has_lost():
            draw_text(screen, font, 'YOU LOST!', 'red', center)

    def step(self, delta_time: float) -> None:
        '''
        Update internal room's state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        super().step(delta_time)
        if not self.is_paused and not self.board.is_game_over():
            self.board.step(delta_time)
