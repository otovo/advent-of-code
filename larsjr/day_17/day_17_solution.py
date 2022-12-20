from abc import ABC
from enum import Enum, auto
import itertools
import copy


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    DOWN = auto()


class Shape(ABC):
    def __init__(self, xmin: int, ymin: int):
        self.positions: list[list[int]] = []
        self.height: int = 0
        self.at_rest = False
        self.create_start_coordinates(xmin, ymin)

    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        raise NotImplementedError()

    def move_if_possible(self, direction: Direction, chamber: list[list[str]]) -> bool:
        # Can do an optimization of only checking bottom positions for DOWN, left for LEFT, etc
        # if postions are ordered by bottom, right, down in the subclasses
        new_positions = self.get_new_positions(direction)
        can_move: bool = True
        for pos in new_positions:
            if pos[0] < 0 or pos[0] >= len(chamber[0]):
                can_move = False
            elif pos[1] < 0:
                can_move = False
            elif chamber[pos[1]][pos[0]] != ".":
                can_move = False

        if can_move:
            self.positions = new_positions
        if direction == Direction.DOWN and can_move == False:
            self.at_rest = True

        return can_move

    @property
    def ymax(self) -> int:
        return self.positions[0][1]

    def get_new_positions(self, direction: Direction) -> list[list[int]]:
        new_positions = copy.deepcopy(self.positions)
        for pos in new_positions:
            match direction:
                case Direction.LEFT:
                    pos[0] -= 1
                case Direction.RIGHT:
                    pos[0] += 1
                case Direction.DOWN:
                    pos[1] -= 1

        return new_positions

    def draw_shape_in_chamber(self, chamber: list[list[str]], is_at_rest=False) -> None:
        for pos in self.positions:
            if is_at_rest:
                chamber[pos[1]][pos[0]] = "#"
            else:
                try:
                    chamber[pos[1]][pos[0]] = "@"
                except IndexError:
                    breakpoint()
                    a = 1

    def undo_draw(self, chamber: list[list[str]]) -> None:
        for pos in self.positions:
            chamber[pos[1]][pos[0]] = "."


class HorizontalLine(Shape):
    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        self.height = 1
        for i in range(xmin, xmin + 4):
            self.positions.append([i, ymin])


class Plus(Shape):
    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        self.height = 3
        self.positions.append([xmin + 1, ymin + 2])
        self.positions.append([xmin, ymin + 1])
        self.positions.append([xmin + 1, ymin + 1])
        self.positions.append([xmin + 2, ymin + 1])
        self.positions.append([xmin + 1, ymin])


class InvertedL(Shape):
    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        self.height = 3
        self.positions.append([xmin + 2, ymin + 2])
        self.positions.append([xmin + 2, ymin + 1])
        self.positions.append([xmin, ymin])
        self.positions.append([xmin + 1, ymin])
        self.positions.append([xmin + 2, ymin])


class VerticalLine(Shape):
    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        self.height = 4
        for j in range(ymin, ymin + 4):
            self.positions.insert(0, [xmin, j])


class Square(Shape):
    def create_start_coordinates(self, xmin: int, ymin: int) -> None:
        self.height = 2
        self.positions.append([xmin, ymin + 1])
        self.positions.append([xmin + 1, ymin + 1])
        self.positions.append([xmin, ymin])
        self.positions.append([xmin + 1, ymin])


class ShapeFactory:
    def __init__(self) -> None:
        self.shape_iterator = itertools.cycle(
            [HorizontalLine, Plus, InvertedL, VerticalLine, Square]
        )

    def get_shape(self, xmin: int, ymin: int) -> Shape:
        return next(self.shape_iterator)(xmin, ymin)


class DirectionProvider:
    def __init__(self, directions: str) -> None:
        self.directions_iterator = itertools.cycle(directions)

    def get_direction(self):
        direction = next(self.directions_iterator)
        match direction:
            case ">":
                return Direction.RIGHT
            case "<":
                return Direction.LEFT


def visualize_chamber(chamber: list[list[str]]) -> None:
    for row in reversed(chamber):
        output = ""
        for element in row:
            output += element
        print(output)


def simulate(chamber: list[list[str]], directions: str) -> int:
    index_of_highest_rock = -1
    direction_provider = DirectionProvider(directions)
    shape_factory = ShapeFactory()
    highest_seen_y = -1

    for _ in range(2022):
        rock = shape_factory.get_shape(2, highest_seen_y + 4)
        while len(chamber) <= rock.ymax + 2:
            chamber.append(["." for _ in range(7)])

        while not rock.at_rest:
            # print(f"Rock pos: {rock.positions}")
            # rock.draw_shape_in_chamber(chamber)
            # visualize_chamber(chamber)
            # rock.undo_draw(chamber)

            hot_gas_direction = direction_provider.get_direction()
            # print(f"Moving {hot_gas_direction}")
            moved = rock.move_if_possible(hot_gas_direction, chamber)
            # print(f"Rock moved: {moved}, pos: {rock.positions}")
            # rock.draw_shape_in_chamber(chamber)
            # visualize_chamber(chamber)
            # rock.undo_draw(chamber)

            # print("Moving DOWN")
            moved = rock.move_if_possible(Direction.DOWN, chamber)
            # print(f"Rock moved: {moved}, pos: {rock.positions}")
            # rock.draw_shape_in_chamber(chamber)
            # visualize_chamber(chamber)
            # rock.undo_draw(chamber)

        rock.draw_shape_in_chamber(chamber, is_at_rest=True)
        index_of_highest_rock = rock.ymax
        if index_of_highest_rock > highest_seen_y:
            highest_seen_y = index_of_highest_rock

    # visualize_chamber(chamber)
    return highest_seen_y + 1


def read_input(filename: str) -> str:
    with open(filename) as fp:
        return fp.read().strip()


if __name__ == "__main__":
    chamber = [["." for _ in range(7)] for _ in range(5)]
    directions = read_input("input.txt")

    print(f"Solution part 1: {simulate(chamber, directions)}")
