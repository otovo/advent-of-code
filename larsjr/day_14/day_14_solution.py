from dataclasses import dataclass, field
import numpy as np
import sys
import itertools


@dataclass
class Path:
    points: list[tuple[int, int]] = field(default_factory=list)
    min_x: int = sys.maxsize
    max_x: int = 0
    min_y: int = sys.maxsize
    max_y: int = 0

    def add_point(self, point: tuple[int, int]) -> None:
        if point[0] < self.min_x:
            self.min_x = point[0]
        if point[0] > self.max_x:
            self.max_x = point[0]
        if point[1] < self.min_y:
            self.min_y = point[1]
        if point[1] > self.max_y:
            self.max_y = point[1]

        self.points.append(point)


def read_input(filename: str) -> list[Path]:
    paths = []
    with open(filename, "r") as fp:
        lines = fp.readlines()

    for line in lines:
        points = line.strip().split("->")
        path = Path()
        for point in points:
            elements = point.split(",")
            path.add_point((int(elements[0]), int(elements[1])))
        paths.append(path)

    return paths


def draw_path_on_grid(path: Path, grid: list[list[str]]) -> None:
    for start, end in itertools.pairwise(path.points):
        if start[0] == end[0]:
            # Change is on y-axis
            x = start[0]
            direction = int((end[1] - start[1]) / abs(end[1] - start[1]))
            y = start[1]
            while y != end[1] + 1 * direction:
                grid[y][x] = "#"
                y += direction * 1
        else:
            # Change is on x-axis
            y = start[1]
            direction = int((end[0] - start[0]) / abs(end[0] - start[0]))
            x = start[0]
            while x != end[0] + 1 * direction:
                grid[y][x] = "#"
                x += direction * 1


def set_up_grid(paths: list[Path]) -> tuple[list[list[str]], int, int, int, int]:
    min_x = paths[0].min_x
    max_x = paths[0].max_x
    min_y = paths[0].min_y
    max_y = paths[0].max_y

    for path in paths:
        if path.min_x < min_x:
            min_x = path.min_x
        if path.max_x > max_x:
            max_x = path.max_x
        if path.min_y < min_y:
            min_y = path.min_y
        if path.max_y > max_y:
            max_y = path.max_y

    grid = [
        ["." for _ in range(max_x + 1)] for _ in range(max_y + 1)
    ]  # index as grid[y][x]
    grid[0][500] = "+"

    for path in paths:
        draw_path_on_grid(path, grid)

    # visualize(grid, min_x, max_x, 0, max_y)

    return grid, min_x, max_x, min_y, max_y


def visualize(
    grid: list[list[str]], min_x: int, max_x: int, min_y: int, max_y: int
) -> None:
    array = np.array(grid)

    print(f"max x: {max_x}")
    part = array[min_y : max_y + 1, min_x : max_x + 1]

    for j in range(part.shape[0]):
        row = ""
        for i in range(part.shape[1]):
            row += part[j, i]
        print(row)


def is_outside_rocks(
    pos: tuple[int, int], min_x: int, max_x: int, min_y: int, max_y: int
) -> bool:
    return pos[0] < min_x or pos[0] >= max_x or pos[1] >= max_y


def go_down(pos: tuple[int, int]) -> tuple[int, int]:
    return (pos[0], pos[1] + 1)


def go_diagonal_left(pos: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] - 1, pos[1] + 1)


def go_diagonal_right(pos: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + 1, pos[1] + 1)


def position_inside_grid(pos: tuple[int, int], grid: list[list[str]]) -> bool:
    return (
        pos[0] >= 0
        and pos[0] <= len(grid[0]) - 1
        and pos[1] >= 0
        and pos[1] <= len(grid) - 1
    )


def can_move_down(pos: tuple[int, int], grid: list[list[str]]) -> bool:
    down = go_down(pos)
    return position_inside_grid(down, grid) and grid[down[1]][down[0]] == "."


def can_move_diagonal_left(pos: tuple[int, int], grid: list[list[str]]) -> bool:
    diagonal_left = go_diagonal_left(pos)
    return (
        position_inside_grid(diagonal_left, grid)
        and grid[diagonal_left[1]][diagonal_left[0]] == "."
    )


def can_move_diagonal_right(pos: tuple[int, int], grid: list[list[str]]) -> bool:
    diagonal_right = go_diagonal_right(pos)
    return (
        position_inside_grid(diagonal_right, grid)
        and grid[diagonal_right[1]][diagonal_right[0]] == "."
    )


def simulate(
    grid: list[list[str]], min_x: int, max_x: int, min_y: int, max_y: int
) -> int:
    units_of_sand_at_rest = 0

    while True:
        sand_at_rest = False

        sand_pos = (500, 0)
        while not sand_at_rest:
            if sand_pos == (494, 9):
                breakpoint()
            if can_move_down(sand_pos, grid):
                sand_pos = go_down(sand_pos)
            elif can_move_diagonal_left(sand_pos, grid):
                sand_pos = go_diagonal_left(sand_pos)
            elif can_move_diagonal_right(sand_pos, grid):
                sand_pos = go_diagonal_right(sand_pos)
            else:
                if is_outside_rocks(sand_pos, min_x, max_x, min_y, max_y):
                    visualize(grid, min_x, max_x, 0, max_y)
                    return units_of_sand_at_rest

                sand_at_rest = True
                grid[sand_pos[1]][sand_pos[0]] = "o"
                units_of_sand_at_rest += 1


if __name__ == "__main__":
    paths = read_input("input.txt")
    grid, min_x, max_x, min_y, max_y = set_up_grid(paths)
    units_of_sand_at_rest = simulate(grid, min_x, max_x, min_y, max_y)
    print(f"Solution part 1: {units_of_sand_at_rest}")
