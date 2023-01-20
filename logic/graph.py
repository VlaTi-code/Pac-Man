'''Implementation of graph algorithms'''

from collections import defaultdict, deque

import attr
from pygame.math import Vector2


__all__ = (
    'Vertex',
    'UndirectedGraph',
    'BFSData',

    'bfs',
)


@attr.s(slots=True, hash=True, eq=True)
class Vertex:
    '''Struct for graph vertex representation'''

    x: int = attr.ib(converter=round)
    y: int = attr.ib(converter=round)

    @staticmethod
    def from_vector(vector: Vector2) -> 'Vertex':
        '''
        Construct a vertex from a 2D-vector. Rounds coordinates to integers

        :param vector: vector to initialize a vertex
        :return: new Vertex instance
        '''

        return Vertex(vector.x, vector.y)

    def to_vector(self) -> Vector2:
        '''
        Convert into a 2D-vector

        :return: new Vector2 instance
        '''

        return Vector2(self.x, self.y)

    def __add__(self, other: Vector2) -> 'Vertex':
        '''
        Addition operator for vertices and 2D-vectors

        :param other: right-hand side addend
        :return: new Vertex instance, sum of addends
        '''

        assert isinstance(other, Vector2), 'You are a donkey!'
        return Vertex(self.x + other.x, self.y + other.y)


@attr.s(slots=True, kw_only=True)
class UndirectedGraph:
    '''Undirected pseudograph representation via adjacency lists (sets)'''

    edges: dict[Vertex, set[Vertex]] = attr.ib(factory=lambda: defaultdict(set), init=False)

    @property
    def size(self) -> int:
        '''
        Get number of vertices, not taking into account isolated ones

        :return: # of vertices
        '''

        return len(self.edges)

    def add_edge(self, from_: Vertex, to: Vertex) -> None:
        '''
        Add an edge between two vertices if absent. Loops are allowed though, but multiple edges are not

        :param from_: one of the vertices to connect
        :param to: one of the vertices to connect
        '''

        self.edges[from_].add(to)
        if from_ != to:
            self.edges[to].add(from_)

    def __getitem__(self, vertex: Vertex) -> set[Vertex]:
        '''
        Adjacent vertices lookup method

        :param vertex: vertex to lookup neighbours for
        :return: set of neighbours
        '''

        return self.edges.get(vertex, set())


@attr.s(slots=True, kw_only=True)
class BFSData:
    '''Simple structure for BFS output data'''

    dist: dict[Vertex, float] = attr.ib(factory=dict)
    parent: dict[Vertex, Vertex] = attr.ib(factory=dict)

    def is_visited(self, vertex: Vertex) -> bool:
        '''
        Helper function to check whether a vertex has been visited before by BFS

        :param vertex: vertex to check
        :return: True if vertex has been bisited
        '''

        return vertex in self.dist

    def process_edge(self, from_: Vertex, to: Vertex, weight: float = 1) -> None:
        '''
        Move along the edge and update search data

        :param from_: edge source vertex
        :param to: edge target vertex
        :param weight: edge weight, defaults to 1 for unweighted graphs
        '''

        if not self.is_visited(to):
            self.dist[to] = self.dist[from_] + weight
            self.parent[to] = from_


def bfs(graph: UndirectedGraph,
        *,
        sources: list[Vertex],
        target: Vertex,
        src_dists: list[float] | None = None) -> BFSData:
    '''
    Multi-source BFS runner

    :param graph: graph to search
    :param sources: list of BFS sources
    :param target: vertex to search for, stop on reaching it
    :param src_dists: list of initial distance values for sources, defaults to zeroes
    :return: BFSData instance
    '''

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
