def Path_Existence(G, s, t):
    
    visited = set() 
    visited.add(s)
    u = s 

    marked = True
    while marked:
        marked = False
        for edge in G.edges:
            if edge.start in visited and edge.end not in visited:
                visited.add(edge.end)
                marked = True
                    
    return t in visited
class Vertex():
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'Vertex({self.name})'
class Edge():