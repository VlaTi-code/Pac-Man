from pathlib import Path

import attr
import pygame

from core import *   # noqa
from logic import *  # noqa
from utils import draw_text, init_from_config


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

    def handle_event(self, event: Event | None = None) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            if self.is_paused:
                self.is_paused = False
            elif event.key == pygame.K_p:
                self.is_paused = True
            else:
                pass

    def render(self, screen: pygame.Surface) -> None:
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
        super().step(delta_time)
        if not self.is_paused and not self.board.is_game_over():
            self.board.step(delta_time)
