'''Ghosts and Pacman implementation'''

from enum import IntEnum
import os
from pathlib import Path

import attr
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *  # noqa
from sprites import AnimatedSprite
from utils import EPS


Image = pygame.Surface


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
    sheet: Image = attr.ib(default=None, init=False)
    init_frames: list[Image] = attr.ib(factory=list, init=False)

    def __attrs_post_init__(self):
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

    def _get_direction(self, *, normalize: bool = False) -> Vector2:
        '''
        Get current facing direction vector and normalize it optionally

        :param normalize: whether to normalize non-zero direction vector or not
        '''

        direction = self.target_pos - self.real_pos
        if normalize and direction.length_squared() > EPS:
            direction.normalize_ip()
        return direction

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        pass

    def is_aligned(self) -> bool:
        '''Check whether a player is at the center of any cell'''

        direction = self._get_direction()
        return direction.length_squared() < EPS

    def step(self, delta_time: float) -> None:
        '''
        Update internal player state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        super().step(delta_time)  # sprite animation
        if not self.is_aligned():
            direction = self._get_direction(normalize=True)
            self.real_pos += self.speed * delta_time * direction
        else:
            self.real_pos = Vertex.from_vector(self.target_pos).to_vector()
            # TODO: sprite shakes and inverses incorrectly :(


@attr.s(slots=True, kw_only=True)
class GhostGangAI(Player):  # TODO: implement AI strategies
    '''Base class for all ghosts'''

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def _get_bfs_data(self, graph: UndirectedGraph, pacman_pos: Vector2) -> BFSData:
        '''
        Run BFS on the board graph and return BFS output data

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        target = Vector(pacman_pos)
        if self.is_aligned():
            return bfs(graph, [Vertex.from_vector(self.real_pos)], target)

        direction = self._get_direction()
        norm = direction.length()
        sources = [
            Vertex.from_vector(self.target_pos - direction.normalize()),
            Vertex.from_vector(self.target_pos),
        ]
        src_dists = [1 - norm, norm]
        return bfs(graph, sources=sources, target=target, src_dists=src_dists)


@attr.s(slots=True, kw_only=True)
class Blinky(GhostGangAI):
    '''Blinky strategy implementation'''

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        ...


@attr.s(slots=True, kw_only=True)
class Pinky(GhostGangAI):
    '''Pinky strategy implementation'''

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        ...


@attr.s(slots=True, kw_only=True)
class Inky(GhostGangAI):
    '''Inky strategy implementation'''

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        ...


@attr.s(slots=True, kw_only=True)
class Clyde(GhostGangAI):
    '''Clyde strategy implementation'''

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        ...


@attr.s(slots=True, kw_only=True)
class Pacman(Player):
    '''Pacman implementation'''

    lives: int = attr.ib()

    score: int = attr.ib(default=0, init=False)
    invincible_time: float = attr.ib(default=0)

    def __attrs_post_init__(self):
        '''Post-initialization'''

        super().__attrs_post_init__()

    def is_invincible(self) -> bool:
        '''Check whether Pacman is currently invincible for ghosts or not'''

        return self.invincible_time > 0

    def get_caught(self) -> None:
        '''Catch Pacman!'''

        self.lives -= 1
        if not self.lives:
            self.image.set_alpha(0)
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

    def _init_new_move(self, keys, graph: UndirectedGraph) -> None:
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

    def _reverse_last_move(self, keys) -> None:
        '''
        Check if pacman tries to move in the opposite direction and accept it if possible

        :param keys: pygame.key.get_pressed() structure
        '''

        direction = self._get_direction(normalize=True)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if direction.x == 1:   # right
                self.target_pos -= direction
                self._rotate_frames(LookAtDirection.LEFT)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if direction.x == -1:  # left
                self.target_pos -= direction
                self._rotate_frames(LookAtDirection.RIGHT)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if direction.y == 1:   # down
                self.target_pos -= direction
                self._rotate_frames(LookAtDirection.UP)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if direction.y == -1:  # up
                self.target_pos -= direction
                self._rotate_frames(LookAtDirection.DOWN)
        else:
            pass

    def update_target(self, graph: UndirectedGraph, pacman_pos: Vector2) -> None:
        '''
        Update player target position given the board graph and current Pacman position

        :param graph: board graph
        :param pacman_pos: Pacman intermediate position w.r.t. to board, in cells
        '''

        keys = pygame.key.get_pressed()
        if self.is_aligned():
            self._init_new_move(keys, graph)
            return
        self._reverse_last_move(keys)
