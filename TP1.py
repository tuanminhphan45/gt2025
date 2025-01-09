def Path_Existence(G, s, t):
    
    start_vertex = next((v for v in G.vertices if v.name == s), None)
    target_vertex = next((v for v in G.vertices if v.name == t), None)
    
    if not start_vertex or not target_vertex:
        return False  
    
    visited = set()
    visited.add(start_vertex)
    queue = [start_vertex]
    
    while queue:
        current = queue.pop(0)
        if current == target_vertex:
            return True
        
        for edge in G.edges:
            if edge.start == current and edge.end not in visited:
                visited.add(edge.end)
                queue.append(edge.end)
    
    return False

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

# Define the graph
A = Vertex('A')
B = Vertex('B')
C = Vertex('C')
D = Vertex('D')

AB = Edge((A, B))
BC = Edge((B, C))
CD = Edge((C, D))

graph = Graph([A, B, C, D], [AB, BC, CD])


print(Path_Existence(graph, 'B', 'A'))  # return false because  no connection between B and A
print(Path_Existence(graph, 'A', 'C'))  # return true because there is a connection between A and C
