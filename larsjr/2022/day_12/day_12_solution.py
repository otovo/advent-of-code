from dataclasses import dataclass, field
from dijkstar import Graph, find_path, NoPathError


@dataclass
class Edge:
    node_number: int
    weight: int


@dataclass
class Node:
    value: str
    number: int
    i: int
    j: int


@dataclass
class Heightmap:
    map: list[list[Node]] = field(default_factory=list)
    start_pos: tuple[int, int] = (0, 0)
    start_pos_num: int = 0
    end_pos: tuple[int, int] = (0, 0)
    end_pos_num: int = 0

    def __iter__(self):
        for j in range(len(self.map)):
            for i in range(len(self.map[0])):
                yield self.map[j][i]

    def get_edges(self, node: Node):
        edges = []
        if (above := self.node_above(node)) and (
            ord(above.value) - ord(node.value)
        ) <= 1:
            weight = 1
            edges.append(Edge(node_number=above.number, weight=weight))

        if (below := self.node_below(node)) and (
            ord(below.value) - ord(node.value)
        ) <= 1:
            weight = 1
            edges.append(Edge(node_number=below.number, weight=weight))

        if (left := self.node_left(node)) and (ord(left.value) - ord(node.value)) <= 1:
            weight = 1
            edges.append(Edge(node_number=left.number, weight=weight))

        if (right := self.node_right(node)) and (
            ord(right.value) - ord(node.value)
        ) <= 1:
            weight = 1
            edges.append(Edge(node_number=right.number, weight=weight))

        return edges

    def node_above(self, node: Node) -> Node | None:
        if node.j == 0:
            return None
        return self.map[node.j - 1][node.i]

    def node_below(self, node: Node) -> Node | None:
        if node.j == len(self.map) - 1:
            return None
        return self.map[node.j + 1][node.i]

    def node_left(self, node: Node) -> Node | None:
        if node.i == 0:
            return None
        return self.map[node.j][node.i - 1]

    def node_right(self, node: Node) -> Node | None:
        if node.i == len(self.map[0]) - 1:
            return None
        return self.map[node.j][node.i + 1]


def read_input(lines: list[str]) -> Heightmap:
    heightmap = Heightmap()

    node_counter = 0
    for j, line in enumerate(lines):
        row = []
        for i, char in enumerate(line.strip()):
            if char == "S":
                heightmap.start_pos = (i, j)
                heightmap.start_pos_num = node_counter
                row.append(Node(value="a", number=node_counter, i=i, j=j))
            elif char == "E":
                heightmap.end_pos = (i, j)
                heightmap.end_pos_num = node_counter
                row.append(Node(value="z", number=node_counter, i=i, j=j))
            else:
                row.append(Node(value=char, number=node_counter, i=i, j=j))
            node_counter += 1
        heightmap.map.append(row)

    return heightmap


def create_graph(heightmap: Heightmap) -> Graph:
    graph = Graph()
    for node in heightmap:
        edges = heightmap.get_edges(node)
        for edge in edges:
            graph.add_edge(node.number, edge.node_number, edge.weight)
    return graph


def find_length_of_shortest_path(heightmap: Heightmap, graph: Graph) -> int:
    path_info = find_path(graph, heightmap.start_pos_num, heightmap.end_pos_num)

    return len(path_info.nodes) - 1


def find_shortest_path_when_starting_at_one_of_lowest_positions(
    heightmap: Heightmap, graph: Graph
) -> int:
    graph_numbers_with_lowest_position = [
        node.number for node in heightmap if node.value == "a"
    ]

    end_node = heightmap.end_pos_num
    path_lengths = []
    for start_number in graph_numbers_with_lowest_position:
        try:
            path = find_path(graph, start_number, end_node)
            path_lengths.append(len(path.nodes) - 1)
        except NoPathError:
            continue

    return min(path_lengths)


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    heightmap = read_input(lines)
    graph = create_graph(heightmap)
    shortest_path = find_length_of_shortest_path(heightmap, graph)
    print(f"Solution part 1: {shortest_path}")

    shortest_path_from_any_lowest_position = (
        find_shortest_path_when_starting_at_one_of_lowest_positions(heightmap, graph)
    )
    print(f"Solution part 2: {shortest_path_from_any_lowest_position}")
