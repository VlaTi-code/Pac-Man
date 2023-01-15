import attr
import pygame

from core import *  # noqa


@attr.s(slots=True, kw_only=True)
class BaseButton:
    pass


@attr.s(slots=True, kw_only=True)
class TransitionButton(BaseButton):
    pass


@attr.s(slots=True, kw_only=True)
class PlayButton(TransitionButton):
    pass


@attr.s(slots=True, kw_only=True)
class SettingsButton(TransitionButton):
    pass


@attr.s(slots=True, kw_only=True)
class SkinsButton(TransitionButton):
    pass


@attr.s(slots=True, kw_only=True)
class AboutButton(TransitionButton):
    pass


@attr.s(slots=True, kw_only=True)
class QuitButton(TransitionButton):
    pass


@attr.s(slots=True, kw_only=True)
class BackButton(TransitionButton):
    pass
