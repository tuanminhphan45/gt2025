edges = [
    (1, 2),
    (1, 3),
    (2, 5),
    (2, 6),
    (5, 7),
    (3, 4),
    (4, 8)
]

def create_adjacency_matrix(edges, num_nodes):
    
    matrix = [[0] * num_nodes for _ in range(num_nodes)]
    
 
    for src, dest in edges:
        matrix[src - 1][dest - 1] = 1  
    
    return matrix

def print_adjacency_matrix(matrix):
    print("Adjacency Matrix:")
    for row in matrix:
        print(" ".join(map(str, row)))

# Function to perform inorder traversal of the graph
def inorder_traversal(graph, node, visited):
    visited.add(node)
    for child in graph.get(node, []):
        if child not in visited:
            inorder_traversal(graph, child, visited)
    print(node, end=" ")

# Function to create an adjacency list from the adjacency matrix
def create_adjacency_list(adj_matrix, num_nodes):
    adj_list = {i + 1: [] for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i][j] == 1:
                adj_list[i + 1].append(j + 1)
    return adj_list

# Function to handle user input for the starting node
def get_start_node(num_nodes):
    while True:
        try:
            start_node = int(input("\nEnter the starting node label (1-8): "))
            if start_node < 1 or start_node > num_nodes:
                raise ValueError("Node label out of range.")
            return start_node
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid node label.")

# Main code
num_nodes = 8  
adj_matrix = create_adjacency_matrix(edges, num_nodes)

print_adjacency_matrix(adj_matrix)

adj_list = create_adjacency_list(adj_matrix, num_nodes)

start_node = get_start_node(num_nodes)

print(f"\nInorder traversal of subtree rooted at {start_node}:")
visited = set()
inorder_traversal(adj_list, start_node, visited)