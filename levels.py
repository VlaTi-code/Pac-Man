from pathlib import Path

import attr
import pygame

from core import *   # noqa
from rooms import *  # noqa


@attr.s(slots=True, kw_only=True)
class LevelOne(LevelRoom):
    pass


@attr.s(slots=True, kw_only=True)
class LevelTwo(LevelRoom):
    pass


@attr.s(slots=True, kw_only=True)
class LevelThree(LevelRoom):
    pass


@attr.s(slots=True, kw_only=True)
class LevelFour(LevelRoom):
    pass


def load_level(path: str | Path) -> LevelRoom:
    # TODO: add levels/ to resources and manager | beware circular imports!
    raise NotImplementedError()
