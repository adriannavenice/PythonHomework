class WeightedEdge:
    def __init__(self, initNode1, initNode2, initWeight):
        self.node1 = initNode1
        self.node2 = initNode2
        self.weight = initWeight

    def getNode1(self):
        return self.node1

    def getNode2(self):
        return self.node2

    def getWeight(self):
        return self.weight


class WeightedGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def get_keys(self):
        return list(self.nodes.keys())

    def node_exists(self, test_node):
        return test_node in self.nodes

    def get_edge_id(self, node1, node2):
        return f"{node1}-{node2}"

    def add_node(self, node_id, node_data):
        self.nodes[node_id] = node_data

    def get_node_data(self, node_id):
        return self.nodes.get(node_id)

    def add_edge(self, node1, node2, weight):
        edge_id = self.get_edge_id(node1, node2)
        self.edges[edge_id] = WeightedEdge(node1, node2, weight)

    def remove_edge(self, node1, node2):
        edge_id = self.get_edge_id(node1, node2)
        if edge_id in self.edges:
            del self.edges[edge_id]

    def get_neighbors(self, node):
        neighbors = []
        for edge_id, edge in self.edges.items():
            start_node, end_node = edge_id.split("-")
            if start_node == node:
                neighbors.append(end_node)
        return neighbors

    def are_neighbors(self, node1, node2):
        neighbors = self.get_neighbors(node1)
        return node2 in neighbors

    def get_neighbor_weight(self, node1, node2):
        if self.are_neighbors(node1, node2):
            edge_id = self.get_edge_id(node1, node2)
            return self.edges[edge_id].getWeight()
        return 0.0

    def find_path(self, node1, node2):
        path = []
        if not self.node_exists(node1) or not self.node_exists(node2):
            return path

        path.append(node1)
        visited = {node1: node1}

        while len(path) > 0:
            last = path[-1]
            neighbors = self.get_neighbors(last)
            closest_index = -1
            closest_distance = 100000.0

            for i, neighbor in enumerate(neighbors):
                if neighbor == node2:
                    path.append(neighbor)
                    return path

                if neighbor not in visited:
                    edge_id = self.get_edge_id(last, neighbor)
                    edge = self.edges[edge_id]
                    if edge.getWeight() < closest_distance:
                        closest_index = i
                        closest_distance = edge.getWeight()

            if closest_index >= 0:
                closest_node = neighbors[closest_index]
                visited[closest_node] = closest_node
                path.append(closest_node)
            elif len(path) > 0:
                path.pop()

        return path