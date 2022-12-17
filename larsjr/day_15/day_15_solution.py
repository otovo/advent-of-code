from dataclasses import dataclass, field
import re
import sys


@dataclass
class Range:
    row: int
    xmin: int
    xmax: int


@dataclass
class Sensor:
    position: tuple[int, int]
    closest_beacon: tuple[int, int]
    occupied_positions: list[tuple[int, int]] = field(default_factory=list)
    manhatten_distance: int = -1
    xmin = sys.maxsize
    xmax = sys.maxsize * -1

    def __post_init__(self):
        self.manhatten_distance = self.compute_manhatten_distance(
            self.position, self.closest_beacon
        )

        self.xmin = self.position[0] - self.manhatten_distance - 1
        self.xmax = self.position[0] + self.manhatten_distance + 1

    def point_occupied_by_sensor(self, point: tuple[int, int]) -> bool:
        return (
            self.compute_manhatten_distance(self.position, point)
            <= self.manhatten_distance
            and point != self.closest_beacon
        )

    def compute_occupied_positions(self):
        xmin = self.position[0] - self.manhatten_distance
        xmax = self.position[0] + self.manhatten_distance
        ymin = self.position[1] - self.manhatten_distance
        ymax = self.position[1] + self.manhatten_distance

        for j in range(ymin, ymax):
            for i in range(xmin, xmax):
                if (
                    self.compute_manhatten_distance(self.position, (i, j))
                    <= self.manhatten_distance
                ) and (i, j) != self.closest_beacon:
                    self.occupied_positions.append((i, j))

    @staticmethod
    def compute_manhatten_distance(
        point1: tuple[int, int], point2: tuple[int, int]
    ) -> int:
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def occupied_range_for_row(self, row: int) -> Range | None:
        x, y = self.position
        diff = abs(y - row)
        if diff > self.manhatten_distance:
            return None
        occupied_for_row = (self.manhatten_distance - diff) * 2 + 1
        start_occupied = x - (self.manhatten_distance - diff)
        end_occupied = x + (self.manhatten_distance - diff)

        if start_occupied == self.closest_beacon[0]:
            start_occupied += 1
        if end_occupied == self.closest_beacon[0]:
            end_occupied -= 1

        return Range(row=row, xmin=start_occupied, xmax=end_occupied)


def merge_ranges(ranges: list[Range]) -> list[Range]:
    sorted_ranges = sorted(ranges, key=lambda r: r.xmin)

    merged_ranges = []
    merged_ranges.append(sorted_ranges[0])
    for r in sorted_ranges[1:]:
        if merged_ranges[-1].xmin <= r.xmin <= merged_ranges[-1].xmax:
            merged_ranges[-1].xmax = max(merged_ranges[-1].xmax, r.xmax)
        else:
            merged_ranges.append(r)

    return merged_ranges


def parse_input(filename: str):
    with open(filename) as fp:
        lines = fp.readlines()

    pattern = r"x=(-?\d+),\sy=(-?\d+)"
    sensors = []
    for line in lines:
        sensor_info, beacon_info = line.split(":")
        sensor_match = re.search(pattern=pattern, string=sensor_info)
        beacon_match = re.search(pattern=pattern, string=beacon_info)
        if sensor_match and beacon_match:
            sensors.append(
                Sensor(
                    position=(int(sensor_match.group(1)), int(sensor_match.group(2))),
                    closest_beacon=(
                        int(beacon_match.group(1)),
                        int(beacon_match.group(2)),
                    ),
                )
            )

    return sensors


def find_occupied_positions_at_row_faster(row: int, sensors: list[Sensor]) -> int:
    xmin = min(sensors, key=lambda p: p.xmin).xmin
    xmax = max(sensors, key=lambda p: p.xmax).xmax
    ranges = [sensor.occupied_range_for_row(row=row) for sensor in sensors]
    ranges = [r for r in ranges if r is not None]
    merged_ranges = merge_ranges(ranges)

    breakpoint()
    occupied_positions = set()
    for i in range(xmin, xmax):
        for sensor in sensors:
            if sensor.point_occupied_by_sensor((i, row)):
                occupied_positions.add((i, row))
                break

    for sensor in sensors:
        if sensor.position in occupied_positions:
            occupied_positions.remove(sensor.position)

    return len(occupied_positions)


def find_occupied_positions_at_row(row: int, sensors: list[Sensor]) -> int:
    xmin = min(sensors, key=lambda p: p.xmin).xmin
    xmax = max(sensors, key=lambda p: p.xmax).xmax

    occupied_positions = set()
    for i in range(xmin, xmax):
        for sensor in sensors:
            if sensor.point_occupied_by_sensor((i, row)):
                occupied_positions.add((i, row))
                break

    for sensor in sensors:
        if sensor.position in occupied_positions:
            occupied_positions.remove(sensor.position)

    return len(occupied_positions)


if __name__ == "__main__":
    sensors = parse_input("test_input.txt")
    print(
        f"Solution part 1: {find_occupied_positions_at_row_faster(row=10, sensors=sensors)}"
    )
