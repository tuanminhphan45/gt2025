from typing import List, Dict, Tuple
import numpy as np
import pandas as pd


class Node:
    def __init__(self, identifier):
        self.identifier = str(identifier)

    def __str__(self):
        return f"Node({self.identifier})"

    def __repr__(self):
        return f"Node({self.identifier})"


class Link:
    """
    Represents a directed connection between two nodes.
    """

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return f"Link({self.source.identifier} -> {self.target.identifier})"

    def __repr__(self):
        return f"Link({self.source}, {self.target})"


class Network:
    def __init__(self):
        self.nodes: List[Node] = []
        self.links: List[Link] = []
        self.node_map: Dict[str, Node] = {}
        self.link_map: Dict[Tuple[str, str], Link] = {}
        self.adj_matrix: np.ndarray = None
        self.subnetworks: List['Network' | 'DirectedNetwork'] = []

    def add_node(self, node_id: str):
        node_id = str(node_id)
        if node_id not in self.node_map:
            node = Node(node_id)
            self.nodes.append(node)
            self.node_map[node_id] = node

        self.update_adj_matrix()

    def add_multiple_nodes(self, node_ids: list):
        for node_id in node_ids:
            self.add_node(node_id)

    def add_link(self, link_tuple: tuple):
        if len(link_tuple) != 2:
            print(f"{link_tuple} is an invalid link. Skipping.")
            return

        source_id, target_id = map(str, link_tuple)

        if source_id not in self.node_map or target_id not in self.node_map:
            print(f"Invalid link endpoints: ({source_id}, {target_id}). Skipping.")
            return

        forward_link = (source_id, target_id)
        backward_link = (target_id, source_id)

        if forward_link not in self.link_map:
            link = Link(self.node_map[source_id], self.node_map[target_id])
            self.links.append(link)
            self.link_map[forward_link] = link

        if backward_link not in self.link_map:
            reverse_link = Link(self.node_map[target_id], self.node_map[source_id])
            self.links.append(reverse_link)
            self.link_map[backward_link] = reverse_link

        self.update_adj_matrix()

    def add_multiple_links(self, link_tuples: list):
        for link_tuple in link_tuples:
            self.add_link(link_tuple)

    def update_adj_matrix(self):
        size = len(self.nodes)
        self.adj_matrix = np.zeros((size, size), dtype=int)
        node_indices = {node.identifier: idx for idx, node in enumerate(self.nodes)}

        for link in self.links:
            src_idx = node_indices[link.source.identifier]
            tgt_idx = node_indices[link.target.identifier]
            self.adj_matrix[src_idx, tgt_idx] = 1
            self.adj_matrix[tgt_idx, src_idx] = 1

    def display_adj_matrix(self):
        labels = [node.identifier for node in self.nodes]
        return pd.DataFrame(self.adj_matrix, index=labels, columns=labels)

    def dfs_traversal(self, start_id, visited=None, result=None):
        if visited is None:
            visited = [False] * len(self.nodes)
        if result is None:
            result = []

        if start_id not in self.node_map:
            print(f"Node {start_id} does not exist. Skipping traversal.")
            return []

        node_indices = {node.identifier: idx for idx, node in enumerate(self.nodes)}
        start_idx = node_indices[start_id]
        result.append(start_id)
        visited[start_idx] = True

        for i in range(len(self.nodes)):
            if self.adj_matrix[start_idx][i] == 1 and not visited[i]:
                self.dfs_traversal(self.nodes[i].identifier, visited, result)

        return result

    def find_subnetworks(self):
        visited = [False] * len(self.nodes)
        subnetworks = []

        for node in self.nodes:
            node_idx = {n.identifier: idx for idx, n in enumerate(self.nodes)}[node.identifier]
            if not visited[node_idx]:
                subnetwork_nodes = self.dfs_traversal(node.identifier, visited)
                subnetworks.append(subnetwork_nodes)

        self.subnetworks = subnetworks
        return subnetworks


class DirectedNetwork(Network):
    def __init__(self):
        super().__init__()
        self.directed_matrix: np.ndarray = None

    def add_directed_link(self, link_tuple):
        if len(link_tuple) != 2:
            print(f"{link_tuple} is an invalid link. Skipping.")
            return

        source_id, target_id = map(str, link_tuple)

        if source_id not in self.node_map or target_id not in self.node_map:
            print(f"Invalid link endpoints: ({source_id}, {target_id}). Skipping.")
            return

        link = (source_id, target_id)

        if link not in self.link_map:
            directed_link = Link(self.node_map[source_id], self.node_map[target_id])
            self.links.append(directed_link)
            self.link_map[link] = directed_link

        self.update_directed_matrix()

    def add_multiple_directed_links(self, link_tuples: list):
        for link_tuple in link_tuples:
            self.add_directed_link(link_tuple)

    def update_directed_matrix(self):
        size = len(self.nodes)
        self.directed_matrix = np.zeros((size, size), dtype=int)
        node_indices = {node.identifier: idx for idx, node in enumerate(self.nodes)}

        for link in self.links:
            src_idx = node_indices[link.source.identifier]
            tgt_idx = node_indices[link.target.identifier]
            self.directed_matrix[src_idx, tgt_idx] = 1

    def display_directed_matrix(self):
        labels = [node.identifier for node in self.nodes]
        return pd.DataFrame(self.directed_matrix, index=labels, columns=labels)


class Utility:
    counter = 0

    @staticmethod
    def next_number():
        Utility.counter += 1
        return Utility.counter - 1

    @staticmethod
    def reset_counter():
        Utility.counter = 0


if __name__ == "__main__":
    node_ids = "123456789"

    directed_net = DirectedNetwork()
    directed_net.add_multiple_nodes(node_ids)

    connections = [
        (1, 2),
        (1, 4),
        (2, 3),
        (5, 4),
        (5, 9),
        (6, 3),
        (6, 4),
        (7, 6),
        (8, 9),
    ]

    directed_net.add_multiple_directed_links(connections)

    print("Directed Adjacency Matrix:")
    print(directed_net.display_directed_matrix())

    print("Subnetworks:")
    print(directed_net.find_subnetworks())

