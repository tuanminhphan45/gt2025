#init ex2
class Vertex():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Vertex({self.name})'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Edge():
    def __init__(self, tuple):
        self.start, self.end = tuple

    def __str__(self):
        return f'Edge({self.start} -> {self.end})'

    def __repr__(self):
        return self.__str__()

class Graph():
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def __str__(self):
        return f'Graph(V, E): V = {self.vertices}, E = {self.edges}'