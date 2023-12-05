from __future__ import annotations
from dataclasses import dataclass
from sre_constants import JUMP


@dataclass
class Side:
    points_in_side: tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ]

    def __hash__(self) -> int:
        return (
            self.points_in_side[0].__hash__()
            + self.points_in_side[1].__hash__()
            + self.points_in_side[2].__hash__()
            + self.points_in_side[3].__hash__()
        )

    def __lt__(self, other):
        return self.points_in_side < other.points_in_side

    def __eq__(self, other: Side) -> bool:
        return self.points_in_side == other.points_in_side

    @staticmethod
    def create_sides_from_point(point: tuple[int, int, int]) -> list[Side]:
        sides = []
        for z in range(point[2], point[2] + 2):
            positions = []
            for y in range(point[1], point[1] + 2):
                for x in range(point[0], point[0] + 2):
                    positions.append((x, y, z))
            sides.append(Side(points_in_side=tuple(sorted(positions))))

        for y in range(point[1], point[1] + 2):
            positions = []
            for z in range(point[2], point[2] + 2):
                for x in range(point[0], point[0] + 2):
                    positions.append((x, y, z))
            sides.append(Side(points_in_side=tuple(sorted(positions))))

        for x in range(point[0], point[0] + 2):

            positions = []
            for y in range(point[1], point[1] + 2):

                for z in range(point[2], point[2] + 2):
                    positions.append((x, y, z))
            sides.append(Side(points_in_side=tuple(sorted(positions))))

        return sides


def read_input(filename: str) -> list[tuple[int, int, int]]:
    points = []
    with open(filename, "r") as fp:
        for line in fp:
            elements = line.strip().split(",")
            points.append((int(elements[0]), int(elements[1]), int(elements[2])))
    return points


if __name__ == "__main__":
    points = read_input("input.txt")
    sides = []
    for point in points:
        sides.extend(Side.create_sides_from_point(point))

    unique_sides = set()
    for side in sides:
        if isinstance(side, list):
            breakpoint()
        if side in unique_sides:
            unique_sides.remove(side)
        else:
            unique_sides.add(side)

    print(len(unique_sides))
