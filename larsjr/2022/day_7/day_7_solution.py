from __future__ import annotations
from enum import Enum, auto
from typing import Callable


class NodeType(Enum):
    DIR = auto()
    FILE = auto()


class Node:
    def __init__(
        self, name: str, size: int | None, node_type: NodeType, parent: Node | None
    ) -> None:
        self.name = name
        self.size = size
        self.node_type = node_type
        self.parent = parent
        self.children: list[Node] = []

    def __str__(self) -> str:
        return self.build_str_rep()

    def build_str_rep(self, indent="") -> str:
        info = (
            "(dir)" if self.node_type == NodeType.DIR else f"(file, size={self.size})"
        )
        rep = f"{indent}- {self.name} {info}\n"
        for child in self.children:
            rep += child.build_str_rep(indent=indent + "  ")

        return rep

    def add_child(self, child: Node):
        self.children.append(child)

    def get_node_with_name(self, name: str) -> Node:
        for child in self.children:
            if child.name == name:
                return child
        raise NameError(f"No node with name {name} exists")

    def filter_nodes(self, filter_criteria: Callable, selection: list[Node]) -> None:
        if filter_criteria(self):
            selection.append(self)
        for child in self.children:
            child.filter_nodes(filter_criteria, selection)

    def calculate_size(self):
        # If the the node is a file, of size has been calculated, return it
        if self.size:
            return self.size

        # If no size, this is a directory, and we must calculate the size of all children
        size = sum(child.calculate_size() for child in self.children)
        self.size = size
        return size


def get_dir_name(dir_line: str) -> str:
    return dir_line.split()[-1].strip()


def get_file_name_and_size(file_line: str) -> tuple[int, str]:
    elements = file_line.split()
    return (int(elements[0]), elements[1].strip())


def build_tree(lines: list[str]) -> Node:
    # Assume that first line is the name of the root directory
    root_name = get_dir_name(lines[0])
    root = Node(name=root_name, size=None, node_type=NodeType.DIR, parent=None)
    current_node = root

    for line in lines[1:]:
        if line.startswith("$ ls"):
            continue
        elif line.startswith("$ cd .."):
            if current_node.parent is None:
                raise ValueError("Invalid directory structure")
            current_node = current_node.parent
        elif line.startswith("$ cd"):
            dir_name = get_dir_name(line)
            current_node = current_node.get_node_with_name(dir_name)
        elif line.startswith("dir"):
            current_node.add_child(
                Node(
                    name=get_dir_name(line),
                    size=None,
                    node_type=NodeType.DIR,
                    parent=current_node,
                )
            )
        else:
            file_size, file_name = get_file_name_and_size(line)
            current_node.add_child(
                Node(
                    name=file_name,
                    size=file_size,
                    node_type=NodeType.FILE,
                    parent=current_node,
                )
            )

    return root


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    root = build_tree(lines)

    # Part 1: Find directories with size of at most 100000
    filter_criteria = (
        lambda x: x.node_type == NodeType.DIR and x.calculate_size() <= 100000
    )
    filtered_nodes: list[Node] = []
    root.filter_nodes(filter_criteria, filtered_nodes)
    size_of_filtered_nodes = sum(node.calculate_size() for node in filtered_nodes)
    print(f"Part 1, total size of directories: {size_of_filtered_nodes}")

    # Part 2: Find the smallest directory that can be deleted to get 30000000 free space
    file_system_size = 70000000
    unused_space_needed = 30000000
    currently_used_space = root.calculate_size()
    currently_unused_space = file_system_size - currently_used_space
    space_needed_to_be_freed_up = unused_space_needed - currently_unused_space
    filter_criteria = (
        lambda x: x.node_type == NodeType.DIR
        and x.calculate_size() >= space_needed_to_be_freed_up
    )
    nodes_with_enough_space = []
    root.filter_nodes(filter_criteria, nodes_with_enough_space)
    size_of_smallest_dir_that_can_be_deleted = min(
        node.calculate_size() for node in nodes_with_enough_space
    )
    print(
        f"Part 2, size of smallest directory that can be deleted: {size_of_smallest_dir_that_can_be_deleted}"
    )
