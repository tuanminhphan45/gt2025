import numpy as np
import pandas as pd

class Graph:
    def __init__(self):
        self._vertices = []
        self._vertex_map = {}
        self._weight_map = {}
        self._wmatrix = None

    def add_vertices_by_string(self, vertex_name_string: str):
        for vertex_name in vertex_name_string:
            if vertex_name not in self._vertex_map:
                self._vertices.append(vertex_name)
                self._vertex_map[vertex_name] = len(self._vertices) - 1

    def add_undirected_edges(self, edge_list: list[tuple[str, str, int]]):
        size = len(self._vertices)
        self._wmatrix = np.zeros((size, size), dtype=int)
        
        for u, v, weight in edge_list:
            if u in self._vertex_map and v in self._vertex_map:
                u_idx = self._vertex_map[u]
                v_idx = self._vertex_map[v]
                self._wmatrix[u_idx][v_idx] = weight
                self._wmatrix[v_idx][u_idx] = weight
                self._weight_map[(u, v)] = weight
                self._weight_map[(v, u)] = weight
    
    def show_wmatrix(self):
        return pd.DataFrame(self._wmatrix, index=self._vertices, columns=self._vertices)

    def dijkstra(self, source: str, target: str):
        import heapq
        
        if source not in self._vertex_map or target not in self._vertex_map:
            raise ValueError("Source or target vertex not found in the graph.")
        
        dist = {v: float('inf') for v in self._vertices}
        prev = {v: None for v in self._vertices}
        dist[source] = 0
        
        heap = [(0, source)]
        visited = set()
        
        while heap:
            current_dist, u = heapq.heappop(heap)
            
            if u in visited:
                continue
            visited.add(u)
            
            if u == target:
                break
            
            for v in self._vertices:
                if (u, v) in self._weight_map:
                    weight = self._weight_map[(u, v)]
                    if dist[v] > current_dist + weight:
                        dist[v] = current_dist + weight
                        prev[v] = u
                        heapq.heappush(heap, (dist[v], v))
        
        path, current = [], target
        if prev[current] is None and current != source:
            return [], float('inf')
        while current is not None:
            path.insert(0, current)
            current = prev[current]
        return path, dist[target]

if __name__ == "__main__":
    g = Graph()
    vertices = "ABCDEFGHLM"
    g.add_vertices_by_string(vertices)
    
    edges = [
        ('A', 'C', 1), ('A', 'B', 4), ('B', 'F', 3), ('C', 'D', 8), ('C', 'F', 7),
        ('D', 'H', 5), ('F', 'E', 1), ('F', 'H', 1), ('E', 'H', 2), ('E', 'L', 2),
        ('H', 'G', 3), ('H', 'M', 7), ('H', 'L', 6), ('G', 'L', 4), ('G', 'M', 4),
        ('L', 'M', 1)
    ]
    g.add_undirected_edges(edges)
    
    print("Adjacency Matrix:")
    print(g.show_wmatrix())
    
    source = input("Enter the source vertex (S): ")
    target = input("Enter the target vertex (T): ")
    
    try:
        path, total_weight = g.dijkstra(source, target)
        if path:
            print(f"Shortest path from {source} to {target}: {' -> '.join(path)}")
            print(f"Total weight: {total_weight}")
        else:
            print(f"No path exists from {source} to {target}.")
    except ValueError as e:
        print(e)
