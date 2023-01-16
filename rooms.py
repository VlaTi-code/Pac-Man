import attr
import pygame

from core import *  # noqa


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
    # TODO: base level configuration
    # level map - Graph?
    # player
    # AI npcs

    def __attrs_post_init__(self):
        import buttons

        screen = pygame.display.get_surface()
        width, height = screen.get_size()

        self.buttons = [
            buttons.BackButton(room=self, xy=(15, height - 65)),
        ]

        # ...
