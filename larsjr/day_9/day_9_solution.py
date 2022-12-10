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


def handle_move(
    move: Move, head_position: list[int], tail_position: list[int]
) -> tuple[list[int], list[int], set[tuple[int, int]]]:
    visited_positions: set[tuple[int, int]] = set()
    axis = get_axis_from_move(move)
    step_direction = get_step_direction_from_move(move)

    start_position = head_position[axis] + (step_direction * 1)
    stop_position = head_position[axis] + (step_direction * (move.steps + 1))

    for pos in range(start_position, stop_position, step_direction):
        head_position[axis] = pos
        x_diff = abs(head_position[0] - tail_position[0])
        y_diff = abs(head_position[1] - tail_position[1])

        if x_diff > 1 and y_diff == 1:  # move diagonally
            tail_position[0] += step_direction * 1
            tail_position[1] = head_position[1]
        elif x_diff == 1 and y_diff > 1:  # move diagonally
            tail_position[0] = head_position[0]
            tail_position[1] += step_direction * 1
        elif x_diff > 1 and y_diff == 0:
            tail_position[0] += step_direction * 1
        elif y_diff > 1 and x_diff == 0:
            tail_position[1] += step_direction * 1

        visited_positions.add(tuple(tail_position))

    return head_position, tail_position, visited_positions


def count_positions_visited_by_tail(moves: list[Move]) -> int:
    # List of coordinates visited by tail
    visited_positions: set[tuple[int, int]] = set()
    head_position = [0, 0]
    tail_position = [0, 0]

    for move in moves:
        head_position, tail_position, new_visited_positions = handle_move(
            move, head_position, tail_position
        )
        visited_positions = visited_positions.union(new_visited_positions)

    return len(visited_positions)


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    moves = read_moves(lines)
    number_of_visited_positions = count_positions_visited_by_tail(moves)
    print(f"Part 1, positions visited at least once: {number_of_visited_positions}")
