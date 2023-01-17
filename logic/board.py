import attr
import pygame
from pygame import Vector2

from core import ResourceManager
from .graph import *   # noqa
from .player import *  # noqa
from utils import draw_sprite


@attr.s(slots=True, kw_only=True)
class Board:
    graph: UndirectedGraph = attr.ib(factory=UndirectedGraph, init=False)
    pellets: list[list[bool]] = attr.ib(init=False)
    total_pellets: int = attr.ib(default=0, init=False)
    players: list[Player] = attr.ib(factory=list, init=False)
    pacman: Pacman = attr.ib(init=False)
    level_background: pygame.Surface = attr.ib(init=False)

    topleft: Vector2 = attr.ib(converter=Vector2)
    cell_size: int = attr.ib(default=25)  # config.yml for Board?
    level_name: str = attr.ib()

    def _parse_level_map(self, lines: list[str]) -> None:
        shifts = tuple(map(Vector2, ((-1, 0), (1, 0), (0, -1), (0, 1))))
        size_x, size_y = len(lines[0]), len(lines)
        self.pellets = [[False] * size_x for _ in range(size_y)]

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                vertex = Vertex(x, y)
                match char:
                    case '.' | ' ':
                        for shift in shifts:
                            neighbour = vertex + shift
                            if (0 <= neighbour.x < size_x and
                                    0 <= neighbour.y < size_y and
                                    lines[neighbour.y][neighbour.x] in ('.', ' ')):
                                self.graph.add_edge(vertex, neighbour)
                        if char == '.':
                            self.pellets[y][x] = True
                            self.total_pellets += 1
                    case 'P':
                        self.pacman = Pacman(spawn_pos=vertex.to_vector())
                        self.players.append(self.pacman)
                    case 'S':
                        self.players.extend([
                            Blinky(spawn_pos=vertex.to_vector()),
                            Pinky(spawn_pos=vertex.to_vector()),
                            Inky(spawn_pos=vertex.to_vector()),
                            Clide(spawn_pos=vertex.to_vector()),
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
                        # draw walls
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

    def has_won(self) -> bool:
        return not self.total_pellets

    def has_lost(self) -> bool:
        return not self.pacman.lives

    def is_game_over(self) -> bool:
        return self.has_won() or self.has_lost()

    def step(self, delta_time: float) -> None:
        for player in self.players:
            player.step(delta_time)
        # check pacman position: eat pellets

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
