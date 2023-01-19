'''Board class implementation'''

from math import pi

import attr
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *   # noqa
from .player import *  # noqa
from utils import draw_sprite, draw_text, init_from_config


@attr.s(slots=True, kw_only=True)
class Board:
    '''Level board class'''

    topleft: Vector2 = attr.ib(converter=Vector2)
    cell_size: int = attr.ib()
    level_name: str = attr.ib()

    graph: UndirectedGraph = attr.ib(factory=UndirectedGraph, init=False)
    pellets: list[list[bool]] = attr.ib(factory=list, init=False)
    total_pellets: int = attr.ib(default=0, init=False)
    players: list[Player] = attr.ib(factory=list, init=False)
    pacman: Pacman = attr.ib(default=None, init=False)
    level_background: pygame.Surface = attr.ib(default=None, init=False)

    def _parse_level_map(self, lines: list[str]) -> None:
        '''
        Helper function for level map parsing and graph construction

        :param lines: list of strings read from a level map file
        '''

        manager = ResourceManager()
        config = manager.get_config()

        shifts = tuple(map(Vector2, ((-1, 0), (1, 0), (0, -1), (0, 1))))
        size_x, size_y = len(lines[0]), len(lines)
        self.pellets = [[False] * size_x for _ in range(size_y)]

        # '#' - wall
        # '.' - pellet
        # ' ' - empty cell
        # BPIC - Blinky / Pinky / Inky / Clyde
        # S - Pacman spawn
        # W - warp
        # F - power pellet

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                vertex = Vertex(x, y)
                if char != '#':
                    for shift in shifts:
                        neighbour = vertex + shift
                        if (0 <= neighbour.x < size_x
                                and 0 <= neighbour.y < size_y
                                and lines[neighbour.y][neighbour.x] in ('.', ' ')):
                            self.graph.add_edge(vertex, neighbour)

                vector = vertex.to_vector()
                match char:
                    case '.':
                        self.pellets[y][x] = True
                        self.total_pellets += 1
                    case 'S':
                        self.pacman = init_from_config(config, Pacman, spawn_pos=vector)
                        self.players.append(self.pacman)
                    case 'B':
                        self.players.append(
                            init_from_config(config, Blinky, spawn_pos=vector),
                        )
                    case 'P':
                        self.players.append(
                            init_from_config(config, Pinky, spawn_pos=vector),
                        )
                    case 'I':
                        self.players.append(
                            init_from_config(config, Inky, spawn_pos=vector),
                        )
                    case 'C':
                        self.players.append(
                            init_from_config(config, Clyde, spawn_pos=vector),
                        )
                    case '#' | ' ':
                        pass
                    case 'W':  # warps
                        ...
                    case 'F':  # power pellets
                        ...
                    case _:
                        raise ValueError(f'Unknown cell type char: {char}')

    @staticmethod
    def _has_wall(lines: list[str], x: int, y: int) -> bool:
        '''
        Helper function for checking if a wall exists on the given position

        :param lines: list of strings read from a level map file
        :param x: cell x-coordinate
        :param y: cell y-coordinate
        '''

        size_x, size_y = len(lines[0]), len(lines)
        return 0 <= x < size_x and 0 <= y < size_y and lines[y][x] == '#'

    def _draw_horizontal_line(self, topleft: Vector2) -> None:
        '''
        Helper method for drawing a horizontal line over a wall cell

        :param topleft: cell top-left coordinate, relative to the board
        '''

        pygame.draw.line(
            self.level_background,
            'blue',
            start_pos=topleft + Vector2(0, self.cell_size / 2),
            end_pos=topleft + Vector2(self.cell_size, self.cell_size / 2),
            width=2,
        )

    def _draw_vertical_line(self, topleft: Vector2) -> None:
        '''
        Helper method for drawing a vertical line over a wall cell

        :param topleft: cell top-left coordinate, relative to the board
        '''

        pygame.draw.line(
            self.level_background,
            'blue',
            start_pos=topleft + Vector2(self.cell_size / 2, 0),
            end_pos=topleft + Vector2(self.cell_size / 2, self.cell_size),
            width=2,
        )

    def _draw_arc(self, center: Vector2, start_angle: float) -> None:
        '''
        Helper method for drawing a 90 degrees anti-clockwise arc line over a wall cell

        :param center: center position for a base ellipse to pick an arc from, relative to the board
        :param start_angle: arc starting direction, in radians
        '''

        pygame.draw.arc(
            self.level_background,
            'blue',
            (center - Vector2(self.cell_size / 2), Vector2(self.cell_size)),
            start_angle,
            start_angle + pi / 2,
            width=2,
        )

    def _init_level_background(self, lines: list[str]) -> None:
        '''
        Helper function for board background initialization

        :param lines: list of strings read from a level map file
        '''

        size_x, size_y = len(lines[0]), len(lines)
        self.level_background = pygame.Surface(self.cell_size * Vector2(size_x, size_y))
        cell_vector = Vector2(self.cell_size)

        # Chessboard-like coloring
        for x in range(size_x):
            for y in range(size_y):
                pygame.draw.rect(
                    self.level_background,
                    (128, 128, 128) if (x + y) % 2 else (224, 224, 224),
                    (self.cell_size * Vector2(x, y), cell_vector),
                )

        shifts = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != '#':
                    continue

                topleft = self.cell_size * Vector2(x, y)

                if (self._has_wall(lines, x - 1, y) and self._has_wall(lines, x + 1, y)
                        and not (self._has_wall(lines, x, y - 1) and self._has_wall(lines, x, y + 1))):
                    self._draw_horizontal_line(topleft)
                elif (self._has_wall(lines, x, y - 1) and self._has_wall(lines, x, y + 1)
                        and not (self._has_wall(lines, x - 1, y) and self._has_wall(lines, x + 1, y))):
                    self._draw_vertical_line(topleft)
                elif (self._has_wall(lines, x + 1, y) and self._has_wall(lines, x, y + 1)
                        and not self._has_wall(lines, x - 1, y) and not self._has_wall(lines, x, y - 1)):
                    # top left corner
                    self._draw_arc(center=topleft + cell_vector, start_angle=pi / 2)
                elif (self._has_wall(lines, x - 1, y) and self._has_wall(lines, x, y + 1)
                        and not self._has_wall(lines, x + 1, y) and not self._has_wall(lines, x, y - 1)):
                    # top right corner
                    self._draw_arc(center=topleft + Vector2(0, self.cell_size), start_angle=0)
                elif (self._has_wall(lines, x + 1, y) and self._has_wall(lines, x, y - 1)
                        and not self._has_wall(lines, x - 1, y) and not self._has_wall(lines, x, y + 1)):
                    # bottom left corner
                    self._draw_arc(center=topleft + Vector2(self.cell_size, 0), start_angle=pi)
                elif (self._has_wall(lines, x - 1, y) and self._has_wall(lines, x, y - 1)
                        and not self._has_wall(lines, x + 1, y) and not self._has_wall(lines, x, y + 1)):
                    # bottom right corner
                    self._draw_arc(center=topleft, start_angle=3 * pi / 2)
                elif all(self._has_wall(lines, x + dx, y + dy) for (dx, dy) in shifts):
                    if not self._has_wall(lines, x + 1, y + 1):
                        # top left corner
                        self._draw_arc(center=topleft + cell_vector, start_angle=pi / 2)
                    elif not self._has_wall(lines, x - 1, y + 1):
                        # top right corner
                        self._draw_arc(center=topleft + Vector2(0, self.cell_size), start_angle=0)
                    elif not self._has_wall(lines, x + 1, y - 1):
                        # bottom left corner
                        self._draw_arc(center=topleft + Vector2(self.cell_size, 0), start_angle=pi)
                    elif not self._has_wall(lines, x - 1, y - 1):
                        # bottom right corner
                        self._draw_arc(center=topleft, start_angle=3 * pi / 2)
                    else:
                        pass
                else:
                    pass

    def __attrs_post_init__(self):
        '''Post-initialization'''

        manager = ResourceManager()
        lines = manager.get_level_map(self.level_name)

        self._parse_level_map(lines)
        self._init_level_background(lines)

        for player in self.players:
            player.scale_sprite((self.cell_size, self.cell_size))
            player.store_init_frames()
            player.compute_masks()

    def has_won(self) -> bool:
        '''Check whether pacman has already won or not'''

        return not self.total_pellets

    def has_lost(self) -> bool:
        '''Check whether pacman has already lost or not'''

        return not self.pacman.lives

    def is_game_over(self) -> bool:
        '''Check whether the game is over or not'''

        return self.has_won() or self.has_lost()

    def step(self, delta_time: float) -> None:
        '''
        Update internal board and players' state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        for player in self.players:
            player.update_target(self.graph, self.pacman.real_pos)
            player.step(delta_time)

        if self.pacman.is_aligned():
            x, y = map(round, self.pacman.real_pos)
            if self.pellets[y][x]:
                self.pellets[y][x] = False
                self.total_pellets -= 1
                self.pacman.score += 1

        if not self.pacman.is_invincible():
            for player in self.players:
                if player != self.pacman and pygame.sprite.collide_mask(self.pacman, player):
                    self.pacman.get_caught()
                    self.pacman.scale_sprite((self.cell_size, self.cell_size))

    def render(self, screen: pygame.Surface) -> None:
        '''
        Drawing method

        :param screen: surface to draw the board on
        '''

        screen.blit(self.level_background, self.topleft)

        for y, row in enumerate(self.pellets):
            for x, has_pellet in enumerate(row):
                if has_pellet:
                    pos = self.topleft + self.cell_size * Vector2(x + 0.5, y + 0.5)
                    pygame.draw.circle(screen, 'yellow', pos, radius=4)

        for player in self.players:
            player.rect.topleft = self.topleft + self.cell_size * player.real_pos
            draw_sprite(screen, player)

        if self.pacman.is_invincible():
            color = pygame.Color('blue')
            topleft = self.topleft + self.cell_size * self.pacman.real_pos
            radius = self.cell_size / 2
            pygame.draw.circle(screen, color, topleft + Vector2(radius), radius, width=2)

        manager = ResourceManager()
        _, height = screen.get_size()
        font = manager.get_font('Chessmaster X', 28)
        draw_text(
            screen,
            font,
            f'Score: {self.pacman.score}',
            'white',
            (225, height - 50),
            centered=False,
        )

        life_sprite = manager.get_sprite('life.png')
        for idx in range(self.pacman.lives):
            life_sprite.rect.topleft = (350 + 60 * idx, height - 65)
            draw_sprite(screen, life_sprite)
