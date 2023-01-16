import attr
import pygame

from core import *  # noqa
import rooms
from sprites import ButtonSprite


Event = pygame.event.EventType
Sprite = pygame.sprite.Sprite


@attr.s(slots=True, kw_only=True)
class BaseButton(Sprite):
    sprite: ButtonSprite = attr.ib(default=None, init=False)

    def update(self, event: Event | None = None) -> None:
        self.sprite.update(event)

    def draw(self, screen: pygame.Surface) -> None:
        self.sprite.draw(screen)


@attr.s(slots=True, kw_only=True)
class TransitionButton(BaseButton):
    room: BaseRoom = attr.ib()

    next_room_type: type = None
    source_name: str = None
    handle_escape: bool = False

    def on_click(self):
        next_room = self.next_room_type()
        self.room.set_next_room(next_room)

    def __attrs_post_init__(self):
        manager = ResourceManager()
        sheet = manager.get_image(self.source_name)
        self.sprite = ButtonSprite(
            sheet=sheet,
            on_click=self.on_click,
            handle_escape=self.handle_escape,
        )


@attr.s(slots=True, kw_only=True)
class PlayButton(TransitionButton):
    next_room_type: type = rooms.LevelMenu
    source_name: str = 'play_btn.png'


@attr.s(slots=True, kw_only=True)
class SettingsButton(TransitionButton):
    next_room_type: type = rooms.SettingsMenu
    source_name: str = 'settings_btn.png'


@attr.s(slots=True, kw_only=True)
class SkinsButton(TransitionButton):
    next_room_type: type = rooms.SkinsMenu
    source_name: str = 'skins_btn.png'


@attr.s(slots=True, kw_only=True)
class AboutButton(TransitionButton):
    next_room_type: type = rooms.AboutMenu
    source_name: str = 'about_btn.png'


@attr.s(slots=True, kw_only=True)
class QuitButton(TransitionButton):
    next_room_type: type = type(None)
    source_name: str = 'quit_btn.png'
    handle_escape = True


@attr.s(slots=True, kw_only=True)
class BackButton(TransitionButton):
    next_room_type: type = rooms.MainMenu
    source_name: str = 'back_btn.png'
