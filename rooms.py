from pathlib import Path
from typing import Any

import attr
import pygame

from core import *   # noqa
from logic import *  # noqa
from utils import init_from_config


Event = pygame.event.EventType


@attr.s(slots=True, kw_only=True)
class BaseMenu(BaseRoom):
    buttons = attr.ib(factory=list)

    def handle_event(self, event: Event | None = None) -> None:
        super().handle_event(event)
        for button in self.buttons:
            button.update(event)

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        for button in self.buttons:
            button.draw(screen)


@attr.s(slots=True, kw_only=True)
class MainMenu(BaseMenu):
    def __attrs_post_init__(self):
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
    def __attrs_post_init__(self):
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
    def __attrs_post_init__(self):
        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class SkinsMenu(BaseMenu):
    def __attrs_post_init__(self):
        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class AboutMenu(BaseMenu):
    def __attrs_post_init__(self):
        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]


@attr.s(slots=True, kw_only=True)
class LevelRoom(BaseMenu):
    level_name: str | Path = None

    board: Board = attr.ib(default=None, init=False)
    is_paused: bool = attr.ib(default=False, init=False)

    def __attrs_post_init__(self):
        import buttons

        manager = ResourceManager()
        config = manager.get_config()

        self.buttons = [
            init_from_config(config, buttons.BackButton, room=self),
        ]

        self.board = init_from_config(config, Board, level_name=self.level_name)

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)

        self.board.render(screen)

        manager = ResourceManager()
        font = manager.get_font('Chessmaster X', 80)
        if self.is_paused:
            render_text(screen, font, 'PAUSE', 'white', screen.get_rect().center)
        elif self.board.has_won():
            render_text(screen, font, 'VICTORY!', 'green', screen.get_rect().center)
        elif self.board.has_lost():
            render_text(screen, font, 'YOU LOST', 'red', screen.get_rect().center)

    def step(self, delta_time: float) -> None:
        super().step(delta_time)
        # TODO: add win / lose state
        if not self.is_paused and not self.board.is_game_over():
            self.board.step(delta_time)
