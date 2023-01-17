import os
from pathlib import Path

import attrs
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *  # noqa
from sprites import AnimatedSprite


@attr.s(slots=True, kw_only=True)
class Player(AnimatedSprite):
    spawn_pos: Vector2 = attr.ib()
    real_pos: Vector2 = attr.ib(init=False)
    target_pos: Vector2 = attr.ib(init=False)
    speed: float = attr.ib(default=2)  # blocks per second
    sheet_name: str | Path = None

    @real_pos.default
    def _(self) -> Vector2:
        return self.spawn_pos

    @target_pos.default
    def _(self) -> Vector2:
        return self.real_pos

    def __attrs_pre_init__(self):
        manager = ResourceManager()
        sheet = manager.get_image(os.path.join('players', self.sheet_name))
        super().__init__(sheet=sheet, num_cols=4, num_rows=1, delay=1/4)

    def get_target_pos(self) -> Vector2:
        '''Return (possibly new) target cell'''
        ...
        return self.target_pos

    def step(self, delta_time: float) -> None:
        super().step(delta_time)  # sprite animation
        direction = self.target_pos - self.real_pos
        # if ||direction|| < eps: real_pos = target_pos
        self.real_pos += self.speed * delta_time * direction


@attr.s(slots=True, kw_only=True)
class AI(Player):
    ...

    def __attrs_post_init__(self):
        # spawn Vector2
        ...

    def _get_bfs_data(self, graph: UndirectedGraph) -> BFSData:
        # data = bfs(graph)
        # return data
        ...


@attr.s(slots=True, kw_only=True)
class Blinky(AI):
    sheet_name: str = 'blinky.png'

    def get_target_pos(self) -> Vector2:
        ...


@attr.s(slots=True, kw_only=True)
class Pinky(AI):
    sheet_name: str = 'pinky.png'

    def get_target_pos(self) -> Vector2:
        ...


@attr.s(slots=True, kw_only=True)
class Inky(AI):
    sheet_name: str = 'inky.png'

    def get_target_pos(self) -> Vector2:
        ...


@attr.s(slots=True, kw_only=True)
class Clide(AI):
    sheet_name: str = 'clide.png'

    def get_target_pos(self) -> Vector2:
        ...


@attr.s(slots=True, kw_only=True)
class Pacman(Player):
    sheet_name: str = 'pacman.png'
    lives: int = attr.ib(default=3, init=False)  # default <- from config
    score: int = attr.ib(default=0, init=False)

    def __attrs_post_init__(self):
        ...

    def get_target_pos(self) -> Vector2:
        ...
