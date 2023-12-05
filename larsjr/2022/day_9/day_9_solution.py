from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Move:
    direction: str
    steps: int


def read_moves(lines: list[str]) -> list[Move]:
    return [
        Move(direction=line.split()[0], steps=int(line.split()[1].strip()))
        for line in lines
    ]


def get_axis_from_move(move: Move) -> int:
    match move.direction:
        case "R":
            return 0
        case "L":
            return 0
        case "U":
            return 1
        case "D":
            return 1
        case _:
            raise ValueError("Unknown direction")


def get_step_direction_from_move(move: Move) -> int:
    match move.direction:
        case "R":
            return 1
        case "L":
            return -1
        case "U":
            return 1
        case "D":
            return -1
        case _:
            raise ValueError("Unknown direction")


# Corner of shame below, didn't want to invest time in visualizing
# the grid in a proper way
grid = [["." for _ in range(15)] for _ in range(16)]


def print_grid():
    rows = []
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[i])):
            row += str(grid[i][j])
        rows.append(row)
    for row in reversed(rows):
        print(row)
    print("\n")


def update_grid(head_position, tail_positions):
    for i in range(len(tail_positions) - 1, 0, -1):
        grid[tail_positions[i][1]][tail_positions[i][0]] = str(i)

    grid[head_position[1]][head_position[0]] = "H"


def update_tail(head: tuple[int, ...], tail: list[int]) -> list[int]:
    x_diff = head[0] - tail[0]
    y_diff = head[1] - tail[1]

    move_x = 0
    move_y = 0
    if abs(x_diff) <= 1 and abs(y_diff) <= 1:
        return tail
    elif abs(x_diff) == 2 and abs(y_diff) == 0:
        move_x = int(x_diff / 2)
    elif abs(y_diff) == 2 and abs(x_diff) == 0:
        move_y = int(y_diff / 2)
    else:  # Move diagonally
        move_x = int(x_diff / abs(x_diff))
        move_y = int(y_diff / abs(y_diff))

    tail[0] += move_x
    tail[1] += move_y
    return tail


def handle_move(
    move: Move, head_position: list[int], tail_positions: list[list[int]]
) -> tuple[list[int], list[list[int]], set[tuple[int, ...]]]:
    visited_positions: set[tuple[int, ...]] = set()
    axis = get_axis_from_move(move)
    step_direction = get_step_direction_from_move(move)

    start_position = head_position[axis]
    stop_position = head_position[axis] + (step_direction * (move.steps + 1))
    for pos in range(start_position, stop_position, step_direction):
        head_position[axis] = pos

        relative_head_position = tuple(head_position)
        for i in range(len(tail_positions)):
            current_tail_position = tail_positions[i]
            current_tail_position = update_tail(
                relative_head_position, current_tail_position
            )
            relative_head_position = tuple(current_tail_position)

            if i == len(tail_positions) - 1:
                visited_positions.add(tuple(current_tail_position))

    return head_position, tail_positions, visited_positions


def count_positions_visited_by_last_tail(moves: list[Move], num_tails: int) -> int:
    # List of coordinates visited by the last tail
    visited_positions: set[tuple[int, ...]] = set()
    visited_positions.add(tuple([0, 0]))
    head_position = [0, 0]
    tail_positions = [[0, 0] for _ in range(num_tails)]

    for move in moves:
        head_position, tail_positions, new_visited_positions = handle_move(
            move, head_position, tail_positions
        )
        visited_positions = visited_positions.union(new_visited_positions)

    return len(visited_positions)


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines_part_1 = fp.readlines()

    moves_part_1 = read_moves(lines_part_1)
    number_of_visited_positions_part_1 = count_positions_visited_by_last_tail(
        moves_part_1, num_tails=1
    )
    print(
        f"Part 1, positions visited at least once: {number_of_visited_positions_part_1}"
    )

    with open("input.txt", "r") as fp:
        lines_part_2 = fp.readlines()

    moves_part_2 = read_moves(lines_part_2)
    number_of_visited_positions_part_2 = count_positions_visited_by_last_tail(
        moves_part_2, num_tails=9
    )
    print(
        f"Part 2, positions visited at least once: {number_of_visited_positions_part_2}"
    )
