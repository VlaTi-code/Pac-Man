import os
from pathlib import Path

import attrs
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *  # noqa
from sprites import AnimatedSprite
from utils import EPS


@attr.s(slots=True, kw_only=True)
class Player(AnimatedSprite):
    spawn_pos: Vector2 = attr.ib()
    speed: float = attr.ib()  # blocks per second
    sheet_name: str | Path = attr.ib()

    real_pos: Vector2 = attr.ib(init=False)
    target_pos: Vector2 = attr.ib(init=False)

    @real_pos.default
    def _(self) -> Vector2:
        return self.spawn_pos

    @target_pos.default
    def _(self) -> Vector2:
        return self.real_pos

    def __attrs_post_init__(self):
        manager = ResourceManager()
        config = manager.get_config()
        sheet = manager.get_image(os.path.join('players', self.sheet_name))
        super().__init__(sheet=sheet, **config['Player-AnimatedSprite'])

    def get_target_pos(self) -> Vector2:
        '''Return (possibly new) target cell'''
        ...
        return self.target_pos

    def step(self, delta_time: float) -> None:
        super().step(delta_time)  # sprite animation
        direction = self.target_pos - self.real_pos
        if direction.magnitude() < EPS:
            self.real_pos = self.target_pos
        else:
            self.real_pos += self.speed * delta_time * direction


@attr.s(slots=True, kw_only=True)
class AI(Player):  # TODO
    ...

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        # spawn Vector2
        ...

    def _get_bfs_data(self, graph: UndirectedGraph) -> BFSData:
        # data = bfs(graph)
        # return data
        ...


@attr.s(slots=True, kw_only=True)
class Blinky(AI):
    def get_target_pos(self) -> Vector2:
        ...

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        ...


@attr.s(slots=True, kw_only=True)
class Pinky(AI):
    def get_target_pos(self) -> Vector2:
        ...

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        ...


@attr.s(slots=True, kw_only=True)
class Inky(AI):
    def get_target_pos(self) -> Vector2:
        ...

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        ...


@attr.s(slots=True, kw_only=True)
class Clide(AI):
    def get_target_pos(self) -> Vector2:
        ...

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        ...


@attr.s(slots=True, kw_only=True)
class Pacman(Player):
    lives: int = attr.ib()

    score: int = attr.ib(default=0, init=False)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        ...

    def get_target_pos(self) -> Vector2:
        ...
