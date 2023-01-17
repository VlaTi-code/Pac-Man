from pathlib import Path

import attr
import pygame

from core import *   # noqa
from rooms import *  # noqa


@attr.s(slots=True, kw_only=True)
class LevelOne(LevelRoom):
    level_name = 'level_1.txt'


@attr.s(slots=True, kw_only=True)
class LevelTwo(LevelRoom):
    level_name = 'level_2.txt'


@attr.s(slots=True, kw_only=True)
class LevelThree(LevelRoom):
    level_name = 'level_3.txt'


@attr.s(slots=True, kw_only=True)
class LevelFour(LevelRoom):
    level_name = 'level_4.txt'
