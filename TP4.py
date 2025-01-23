import heapq
from collections import defaultdict

# Define the vertices and edges of the graph
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
graph_edges = {
    (1, 2): 4, (1, 5): 1, (1, 7): 2,
    (2, 3): 7, (2, 6): 5,
    (3, 4): 1, (3, 6): 8,
    (4, 6): 6, (4, 7): 4, (4, 8): 3,
    (5, 6): 9, (5, 7): 10,
    (6, 9): 2,
    (7, 7): 2, (7, 9): 8,
    (8, 9): 1
}

# Create an adjacency list from the edges
adj_list = defaultdict(list)
for (start, end), weight in graph_edges.items():
    adj_list[start].append((end, weight))
    adj_list[end].append((start, weight))

# Function to perform Prim's algorithm
def prim(start_node):
    mst = []
    visited_nodes = set()
    min_heap = [(0, start_node, None)]  # (weight, current_node, previous_node)
    total_cost = 0

    while min_heap:
        weight, current_node, prev_node = heapq.heappop(min_heap)
        if current_node not in visited_nodes:
            visited_nodes.add(current_node)
            if prev_node is not None:
                mst.append((prev_node, current_node, weight))
                total_cost += weight
            for neighbor, edge_weight in adj_list[current_node]:
                if neighbor not in visited_nodes:
                    heapq.heappush(min_heap, (edge_weight, neighbor, current_node))

    return mst, total_cost

# Function to perform Kruskal's algorithm
def kruskal():
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]:
                    rank[root2] += 1

    for node in nodes:
        parent[node] = node
        rank[node] = 0

    mst = []
    total_cost = 0
    sorted_edges = sorted(graph_edges.items(), key=lambda item: item[1])

    for (u, v), weight in sorted_edges:
        if find(u) != find(v):
            union(u, v)
            mst.append((u, v, weight))
            total_cost += weight

    return mst, total_cost

def main():
    try:
        root_node = int(input(f"Please enter the root node for Prim's algorithm (options: {nodes}): "))
        if root_node not in nodes:
            raise ValueError("The root node must be one of the vertices.")
    except ValueError as error:
        print(f"Error: {error}")
    else:
        print("\nExecuting Prim's Algorithm:")
        prim_mst_edges, prim_total_weight = prim(root_node)
        print("MST Edges:", prim_mst_edges)
        print("MST Total Weight:", prim_total_weight)

    print("\nExecuting Kruskal's Algorithm:")
    kruskal_mst_edges, kruskal_total_weight = kruskal()
    print("MST Edges:", kruskal_mst_edges)
    print("MST Total Weight:", kruskal_total_weight)

if __name__ == "__main__":
    main()