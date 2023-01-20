'''Ghosts and Pacman implementation'''

from enum import Enum, IntEnum
import os
from pathlib import Path
from typing import Sequence

import attr
import pygame
from pygame.math import Vector2

from core import ResourceManager
from .graph import *  # noqa
from sprites import AnimatedSprite
from utils import EPS


__all__ = (
    'Player',
    'GhostGangAI',

    'Blinky',
    'Pinky',
    'Inky',
    'Clyde',

    'Pacman',
)


Image = pygame.surface.Surface
KeysType = Sequence[bool]


def round_vector(vector: Vector2) -> Vector2:
    '''
    Round vector components

    :param vector: 2D-vector to round
    '''

    return Vertex.from_vector(vector).to_vector()


def is_zero(vector: Vector2) -> bool:
    '''
    Check whether a vector is zero

    :param vector: 2D-vector to check
    '''

    return vector.x == vector.y == 0


def is_almost_zero(vector: Vector2) -> bool:
    '''
    Check whether a vector is close to zero

    :param vector: 2D-vector to check
    '''

    return vector.length_squared() < EPS


class LookAtDirection(IntEnum):
    '''Enumerated Player facing directions, represented as angles converted into degrees'''

    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270


@attr.s(slots=True, kw_only=True)
class Player(AnimatedSprite):
    '''Base class for players (i.e. ghosts and pacman)'''

    spawn_pos: Vector2 = attr.ib()
    speed: float = attr.ib()  # blocks per second
    sheet_name: str | Path = attr.ib()

    real_pos: Vector2 = attr.ib(default=None, init=False)
    target_pos: Vector2 = attr.ib(default=None, init=False)
    # direction always stays either zero or normalized, for numerical stability
    direction: Vector2 = attr.ib(factory=Vector2, init=False)  # type: ignore
    sheet: Image = attr.ib(default=None, init=False)
    init_frames: list[Image] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        manager = ResourceManager()
        self.sheet = manager.get_image(os.path.join('players', self.sheet_name))
        self.respawn()

    def store_init_frames(self) -> None:
        '''Helper method for storing initial frames internally'''

        self.init_frames = [frame.copy() for frame in self.frames]

    def respawn(self) -> None:
        '''Respawn method'''

        manager = ResourceManager()
        config = manager.get_config()
        super().__init__(sheet=self.sheet, compute_masks=True, **config['Player-AnimatedSprite'])

        self.real_pos = Vector2(self.spawn_pos)
        self.target_pos = Vector2(self.real_pos)

    def _rotate_frames(self, angle: LookAtDirection) -> None:
        '''
        Rotate all frames by angle w.r.t. initial frame directions

        :param angle: angle to rotate by, in degrees
        '''

        self.frames = [
            pygame.transform.rotate(frame, angle)
            for frame in self.init_frames
        ]
        self.compute_masks()

    def is_aligned(self) -> bool:
        '''Check whether a player is at the center of a target cell'''

        return is_zero(self.direction)

    def precise_align(self) -> None:
        '''Round player position'''

        self.real_pos = round_vector(self.real_pos)

    def _update_direction(self) -> None:
        '''Update direction vector according to current target position'''

        offset = self.target_pos - self.real_pos
        if is_almost_zero(offset):  # arrival
            self.direction = Vector2()
            return

        if offset.x < 0:
            self.direction = Vector2(-1, 0)
        elif offset.x > 0:
            self.direction = Vector2(1, 0)
        elif offset.y < 0:
            self.direction = Vector2(0, -1)
        elif offset.y > 0:
            self.direction = Vector2(0, 1)
        else:
            assert False, 'Smth went numerically unstable, sorry'

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        raise NotImplementedError()

    def step(self, delta_time: float) -> None:
        '''
        Update internal player state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        super().step(delta_time)  # sprite animation

        if self.is_aligned():
            self.precise_align()
        else:
            self.real_pos += self.speed * delta_time * self.direction


class GhostState(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    EATEN = 3


@attr.s(slots=True, kw_only=True)
class GhostGangAI(Player):
    '''Base class for all ghosts'''

    state: GhostState = attr.ib(default=GhostState.SCATTER, init=False)
    state_timer: float = attr.ib(default=0, init=False)
    last_direction: Vector2 = attr.ib(default=None, init=False)

    # TODO: implement AI strategies

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def _update_direction(self) -> None:
        '''Update direction vector according to current target position'''

        super()._update_direction()

        if not is_zero(self.direction):
            self.last_direction = self.direction

    def _get_possible_directions(self, graph: UndirectedGraph) -> list[Vertex]:
        if not self.is_aligned():
            return []

        vertex = Vertex.from_vector(self.real_pos)
        directions = list(filter(
            lambda vec: -vec != self.last_direction,
            [
                neighbour.to_vector() - self.real_pos
                for neighbour in graph[vertex]
            ],
        ))
        return directions

    def _get_bfs_data(self, graph: UndirectedGraph, pacman_pos: Vector2) -> BFSData:
        '''
        Run BFS on the board graph and return BFS output data

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        target = Vertex.from_vector(pacman_pos)
        if self.is_aligned():
            return bfs(graph, sources=[Vertex.from_vector(self.real_pos)], target=target)

        offset = self.target_pos - self.real_pos
        norm = offset.length()

        sources = [
            Vertex.from_vector(self.target_pos - self.direction),
            Vertex.from_vector(self.target_pos),
        ]
        src_dists = [1 - norm, norm]
        return bfs(graph, sources=sources, target=target, src_dists=src_dists)

    def step(self, delta_time: float) -> None:
        '''
        Update internal player state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        super().step(delta_time)

        self.state_timer -= delta_time
        if self.state_timer < 0:
            manager = ResourceManager()
            config = manager.get_config()

            if self.state == GhostState.CHASE:
                self.state = GhostState.SCATTER
                self.state_timer = config['GhostGangAI']['scatter-timer']
            elif self.state == GhostState.SCATTER:
                self.state = GhostState.CHASE
                self.state_timer = config['GhostGangAI']['chase-timer']
            else:
                pass


@attr.s(slots=True, kw_only=True)
class Blinky(GhostGangAI):
    '''Blinky strategy implementation'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        directions = self._get_possible_directions(graph)
        if not directions:
            self._update_direction()
            return

        self.direction = min(
            directions,
            key=lambda vec: (self.real_pos + vec - pacman_pos).length_squared(),
        )
        self.target_pos = self.real_pos + self.direction


@attr.s(slots=True, kw_only=True)
class Pinky(GhostGangAI):
    '''Pinky strategy implementation'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        data = self._get_bfs_data(graph, pacman_pos)
        ...
        self._update_direction()


@attr.s(slots=True, kw_only=True)
class Inky(GhostGangAI):
    '''Inky strategy implementation'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        data = self._get_bfs_data(graph, pacman_pos)
        ...
        self._update_direction()


@attr.s(slots=True, kw_only=True)
class Clyde(GhostGangAI):
    '''Clyde strategy implementation'''

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        data = self._get_bfs_data(graph, pacman_pos)
        ...
        self._update_direction()


@attr.s(slots=True, kw_only=True)
class Pacman(Player):
    '''Pacman implementation'''

    lives: int = attr.ib()
    invincible_time: float = attr.ib(default=0)

    score: int = attr.ib(default=0, init=False)

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        super().__attrs_post_init__()

    def is_invincible(self) -> bool:
        '''Check whether Pacman is currently invincible for ghosts or not'''

        return self.invincible_time > 0

    def get_caught(self) -> None:
        '''Catch Pacman!'''

        self.lives -= 1
        if not self.lives:
            self.image.set_alpha(0)  # type: ignore
        self.respawn()
        self.score = 0

        manager = ResourceManager()
        config = manager.get_config()
        self.invincible_time = config['Pacman']['invincible_time']

    def step(self, delta_time: float) -> None:
        '''
        Update internal player state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        super().step(delta_time)

        if self.is_invincible():
            self.invincible_time = max(0, self.invincible_time - delta_time)

    def _init_new_move(self, keys: KeysType, graph: UndirectedGraph) -> None:
        '''
        Check if pacman tries to initiate a new move while being aligned and accept it if possible

        :param keys: pygame.key.get_pressed() structure
        :param graph: board graph
        '''

        vertex = Vertex.from_vector(self.real_pos)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self._rotate_frames(LookAtDirection.LEFT)
            neighbour = Vertex(vertex.x - 1, vertex.y)
            if neighbour in graph[vertex]:
                self.target_pos.x -= 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self._rotate_frames(LookAtDirection.RIGHT)
            neighbour = Vertex(vertex.x + 1, vertex.y)
            if neighbour in graph[vertex]:
                self.target_pos.x += 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self._rotate_frames(LookAtDirection.UP)
            neighbour = Vertex(vertex.x, vertex.y - 1)
            if neighbour in graph[vertex]:
                self.target_pos.y -= 1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self._rotate_frames(LookAtDirection.DOWN)
            neighbour = Vertex(vertex.x, vertex.y + 1)
            if neighbour in graph[vertex]:
                self.target_pos.y += 1
        else:
            pass

    def _reverse_last_move(self, keys: KeysType) -> None:
        '''
        Check if pacman tries to move in the opposite direction and accept it if possible

        :param keys: pygame.key.get_pressed() structure
        '''

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.direction.x == 1:   # right
                self.target_pos -= self.direction
                self._rotate_frames(LookAtDirection.LEFT)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.direction.x == -1:  # left
                self.target_pos -= self.direction
                self._rotate_frames(LookAtDirection.RIGHT)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.direction.y == 1:   # down
                self.target_pos -= self.direction
                self._rotate_frames(LookAtDirection.UP)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.direction.y == -1:  # up
                self.target_pos -= self.direction
                self._rotate_frames(LookAtDirection.DOWN)
        else:
            pass

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. board, in cells
        '''

        keys = pygame.key.get_pressed()
        if self.is_aligned():
            self._init_new_move(keys, graph)
        else:
            self._reverse_last_move(keys)

        self._update_direction()
