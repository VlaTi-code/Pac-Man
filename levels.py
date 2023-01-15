from pathlib import Path

import attr
import pygame

from core import *   # noqa
from rooms import *  # noqa


@attr.s(slots=True, kw_only=True)
class LevelOne(LevelRoom):
    pass


def load_level(path: str | Path) -> LevelRoom:
    raise NotImplementedError()
