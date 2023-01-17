from pathlib import Path

import attr
import pygame

from core import *   # noqa
from logic import *  # noqa


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
    background_name = 'main_menu_back.png'

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        _, height = screen.get_size()

        self.buttons = [
            buttons.PlayButton(room=self, xy=(15, height - 265)),
            buttons.SettingsButton(room=self, xy=(15, height - 215)),
            buttons.SkinsButton(room=self, xy=(15, height - 165)),
            buttons.AboutButton(room=self, xy=(15, height - 115)),
            buttons.QuitButton(room=self, xy=(15, height - 65)),
        ]


@attr.s(slots=True, kw_only=True)
class LevelMenu(BaseMenu):
    background_name = 'level_menu_back.png'

    def __attrs_post_init__(self):
        import buttons
        import levels

        screen = pygame.display.get_surface()
        width, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),

            buttons.LevelButton(
                room=self,
                next_room_type=levels.LevelOne,
                level_idx=1,
                xy=(width // 2 - 75, height // 2 - 75),
            ),
            buttons.LevelButton(
                room=self,
                next_room_type=levels.LevelTwo,
                level_idx=2,
                xy=(width // 2 + 25, height // 2 - 75),
            ),
            buttons.LevelButton(
                room=self,
                next_room_type=levels.LevelThree,
                level_idx=3,
                xy=(width // 2 - 75, height // 2 + 25),
            ),
            buttons.LevelButton(
                room=self,
                next_room_type=levels.LevelFour,
                level_idx=4,
                xy=(width // 2 + 25, height // 2 + 25),
            ),
        ]


@attr.s(slots=True, kw_only=True)
class SettingsMenu(BaseMenu):
    background_name = 'settings_back.png'

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        _, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),
        ]


@attr.s(slots=True, kw_only=True)
class SkinsMenu(BaseMenu):
    background_name = 'skins_back.png'

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        _, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),
        ]


@attr.s(slots=True, kw_only=True)
class AboutMenu(BaseMenu):
    background_name = 'about_back.png'

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        _, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),
        ]


@attr.s(slots=True, kw_only=True)
class LevelRoom(BaseMenu):
    board: Board = attr.ib(default=None, init=False)
    level_name: str | Path = None
    is_paused: bool = attr.ib(default=False, init=False)

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        width, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),
        ]

        self.board = Board(level_name=self.level_name, topleft=(20, 20))

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
        # add win / lose state
        if not self.is_paused and not self.board.is_game_over():
            self.board.step(delta_time)
