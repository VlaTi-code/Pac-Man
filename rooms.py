import attr
import pygame

from core import *  # noqa


Event = pygame.event.EventType


@attr.s(slots=True, kw_only=True)
class BaseMenu(BaseRoom):
    buttons = attr.ib(factory=pygame.sprite.Group)  # TODO: list[BaseButton] + for loops?

    def handle_event(self, event: Event | None = None) -> None:
        super().handle_event(event)
        self.buttons.update(event)

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)
        self.buttons.draw(screen)


@attr.s(slots=True, kw_only=True)
class MainMenu(BaseMenu):
    background_name = 'main_menu_back.png'

    def __attrs_post_init__(self):
        import buttons

        self.buttons.add(buttons.PlayButton(room=self))
        self.buttons.add(buttons.SetttingsButton(room=self))
        self.buttons.add(buttons.SkinsButton(room=self))
        self.buttons.add(buttons.AboutButton(room=self))
        self.buttons.add(buttons.QuitButton(room=self))

        # TODO: position buttons on the screen


@attr.s(slots=True, kw_only=True)
class LevelMenu(BaseMenu):
    background_name = 'level_menu_back.png'

    def __attrs_post_init__(self):
        import buttons

        self.buttons.add(buttons.BackButton(room=self))
        # TODO: + level buttons


@attr.s(slots=True, kw_only=True)
class SettingsMenu(BaseMenu):
    background_name = 'settings_back.png'

    def __attrs_post_init__(self):
        import buttons

        self.buttons.add(buttons.BackButton(room=self))


@attr.s(slots=True, kw_only=True)
class SkinsMenu(BaseMenu):
    background_name = 'skins_back.png'

    def __attrs_post_init__(self):
        import buttons

        self.buttons.add(buttons.BackButton(room=self))


@attr.s(slots=True, kw_only=True)
class AboutMenu(BaseMenu):
    background_name = 'about_back.png'

    def __attrs_post_init__(self):
        import buttons

        self.buttons.add(buttons.BackButton(room=self))


@attr.s(slots=True, kw_only=True)
class LevelRoom(BaseRoom):
    # TODO
    # back button
    # level map - Graph?
    # player
    # AI npcs

    def __attrs_post_init__(self):
        import buttons

        # ...
