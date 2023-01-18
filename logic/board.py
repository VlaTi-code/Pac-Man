import attr
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *   # noqa
from .player import *  # noqa
from utils import draw_sprite, init_from_config


@attr.s(slots=True, kw_only=True)
class Board:
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
        manager = ResourceManager()
        config = manager.get_config()

        shifts = tuple(map(Vector2, ((-1, 0), (1, 0), (0, -1), (0, 1))))
        size_x, size_y = len(lines[0]), len(lines)
        self.pellets = [[False] * size_x for _ in range(size_y)]

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

                match char:
                    case '.':
                        self.pellets[y][x] = True
                        self.total_pellets += 1
                    case 'P':
                        vector = vertex.to_vector()
                        self.pacman = init_from_config(config, Pacman, spawn_pos=vector)
                        self.players.append(self.pacman)
                    case 'S':
                        vector = vertex.to_vector()
                        self.players.extend([
                            init_from_config(config, Blinky, spawn_pos=vector),
                            init_from_config(config, Pinky, spawn_pos=vector),
                            init_from_config(config, Inky, spawn_pos=vector),
                            init_from_config(config, Clyde, spawn_pos=vector),
                        ])
                    case '#':
                        pass

    def _init_level_background(self, lines: list[str]) -> None:
        size_x, size_y = len(lines[0]), len(lines)

        self.level_background = pygame.Surface(self.cell_size * Vector2(size_x, size_y))
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                match char:
                    case '#':
                        # TODO: draw walls
                        pygame.draw.rect(
                            self.level_background,
                            'brown',
                            (self.cell_size * Vector2(x, y), Vector2(self.cell_size)),
                        )
                    case _:
                        pass

    def __attrs_post_init__(self):
        manager = ResourceManager()
        lines = manager.get_level_map(self.level_name)

        self._parse_level_map(lines)
        self._init_level_background(lines)

        for player in self.players:
            player.scale_sprite((self.cell_size, self.cell_size))
            player.store_init_frames()

    def has_won(self) -> bool:
        return not self.total_pellets

    def has_lost(self) -> bool:
        return not self.pacman.lives

    def is_game_over(self) -> bool:
        return self.has_won() or self.has_lost()

    def step(self, delta_time: float) -> None:
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
            # color.a = 64
            topleft = self.topleft + self.cell_size * self.pacman.real_pos
            radius = self.cell_size / 2
            pygame.draw.circle(screen, color, topleft + Vector2(radius), radius, width=2)
