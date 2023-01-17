from collections import defaultdict, deque

import attr
import pygame


@attr.s(slots=True, hash=True, eq=True)
class Vertex:
    x: int = attr.ib(converter=round)
    y: int = attr.ib(converter=round)

    @staticmethod
    def from_vector(self, vector: pygame.Vector2) -> 'Vertex':
        return Vertex(vector.x, vector.y)

    def to_vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)

    def __add__(self, other: pygame.Vector2) -> 'Vertex':
        assert isinstance(other, pygame.Vector2), 'You are a donkey!'
        return Vertex(self.x + other.x, self.y + other.y)


@attr.s(slots=True, kw_only=True)
class UndirectedGraph:
    edges: dict[Vertex, list[Vertex]] = attr.ib(factory=lambda: defaultdict(list), init=False)

    @property
    def size(self) -> int:
        return len(self.edges)

    def add_edge(self, from_: Vertex, to: Vertex) -> None:
        self.edges[from_].append(to)
        if from_ != to:
            self.edges[to].append(from_)

    def __getitem__(self, vertex: Vertex) -> list[Vertex]:
        return self.edges.get(vertex, [])


@attr.s(slots=True, kw_only=True)
class BFSData:
    dist: dict[Vertex, float] = attr.ib(factory=dict)
    parent: dict[Vertex, Vertex] = attr.ib(factory=dict)

    def is_visited(self, vertex: Vertex) -> bool:
        return to in self.dist

    def process_edge(self, from_: Vertex, to: Vertex, weight: float = 1) -> None:
        if not self.is_visited(to):
            self.dist[to] = self.dist[from_] + weight
            self.parent[to] = from_


def bfs(graph: UndirectedGraph,
        sources: list[Vertex],
        target: Vertex,
        src_dists: list[float] = None) -> BFSData:
    if src_dists is None:
        src_dists = [0] * len(sources)

    data = BFSData()
    queue = deque(sources)
    for src, dist in zip(sources, src_dists):
        data.dist[src] = dist

    while queue and not data.is_visited(target):
        vertex = queue.popleft()
        for to in graph[vertex]:
            if not data.is_visited(to):
                data.process_edge(vertex, to)
                queue.append(to)
                if to == target:
                    break
    return data
