'''Level rooms and buttons'''

from pathlib import Path

import attr

from buttons import LevelButton
from rooms import LevelRoom


# Level rooms
@attr.s(slots=True, kw_only=True)
class LevelOne(LevelRoom):
    '''Level 1 room'''

    level_name: str | Path = 'level_1.txt'


@attr.s(slots=True, kw_only=True)
class LevelTwo(LevelRoom):
    '''Level 2 room'''

    level_name: str | Path = 'level_2.txt'


@attr.s(slots=True, kw_only=True)
class LevelThree(LevelRoom):
    '''Level 3 room'''

    level_name: str | Path = 'level_3.txt'


@attr.s(slots=True, kw_only=True)
class LevelFour(LevelRoom):
    '''Level 4 room'''

    level_name: str | Path = 'level_4.txt'


# Level buttons
@attr.s(slots=True, kw_only=True)
class LevelOneButton(LevelButton):
    '''Button for opening level 1'''

    next_room_type: type = LevelOne
    level_idx: int = 1


@attr.s(slots=True, kw_only=True)
class LevelTwoButton(LevelButton):
    '''Button for opening level 2'''

    next_room_type: type = LevelTwo
    level_idx: int = 2


@attr.s(slots=True, kw_only=True)
class LevelThreeButton(LevelButton):
    '''Button for opening level 3'''

    next_room_type: type = LevelThree
    level_idx: int = 3


@attr.s(slots=True, kw_only=True)
class LevelFourButton(LevelButton):
    '''Button for opening level 4'''

    next_room_type: type = LevelFour
    level_idx: int = 4
