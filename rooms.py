import attr
import pygame

from core import *  # noqa


@attr.s(slots=True, kw_only=True)
class BaseMenu(BaseRoom):
    pass


@attr.s(slots=True, kw_only=True)
class MainMenu(BaseMenu):
    pass


@attr.s(slots=True, kw_only=True)
class LevelMenu(BaseMenu):
    pass


@attr.s(slots=True, kw_only=True)
class SettingsMenu(BaseMenu):
    pass


@attr.s(slots=True, kw_only=True)
class SkinsMenu(BaseMenu):
    pass


@attr.s(slots=True, kw_only=True)
class AboutMenu(BaseMenu):
    pass


@attr.s(slots=True, kw_only=True)
class LevelRoom(BaseRoom):
    pass
