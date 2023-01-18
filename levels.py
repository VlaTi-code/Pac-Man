from pathlib import Path

import attr
import pygame

from buttons import *
from core import *   # noqa
from rooms import *  # noqa


# Level rooms
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


# Level buttons
@attr.s(slots=True, kw_only=True)
class LevelOneButton(LevelButton):
    next_room_type: type = LevelOne
    level_idx: int = 1


@attr.s(slots=True, kw_only=True)
class LevelTwoButton(LevelButton):
    next_room_type: type = LevelTwo
    level_idx: int = 2


@attr.s(slots=True, kw_only=True)
class LevelThreeButton(LevelButton):
    next_room_type: type = LevelThree
    level_idx: int = 3


@attr.s(slots=True, kw_only=True)
class LevelFourButton(LevelButton):
    next_room_type: type = LevelFour
    level_idx: int = 4
