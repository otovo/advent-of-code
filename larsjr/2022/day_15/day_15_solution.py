from dataclasses import dataclass, field
import re


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
    xmin = 0
    xmax = 0

    def __post_init__(self):
        self.manhatten_distance = self.compute_manhatten_distance(
            self.position, self.closest_beacon
        )

        self.xmin = min(self.closest_beacon[0], self.position[0])
        self.xmax = max(self.closest_beacon[0], self.position[0])

    def occupied_range_for_row(self, row: int, exclude_becon_pos=True) -> Range | None:
        x, y = self.position
        diff = abs(y - row)
        if diff > self.manhatten_distance:
            return None
        start_occupied = x - (self.manhatten_distance - diff)
        end_occupied = x + (self.manhatten_distance - diff)

        if exclude_becon_pos:
            if (
                start_occupied == self.closest_beacon[0]
                and row == self.closest_beacon[1]
            ):
                start_occupied += 1
            if end_occupied == self.closest_beacon[0] and row == self.closest_beacon[1]:
                end_occupied -= 1

            if start_occupied > end_occupied:
                return None

        return Range(row=row, xmin=start_occupied, xmax=end_occupied)

    @staticmethod
    def compute_manhatten_distance(
        point1: tuple[int, int], point2: tuple[int, int]
    ) -> int:
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def merge_ranges(ranges: list[Range]) -> list[Range]:
    if not len(ranges):
        return []
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


def find_occupied_positions_at_row(row: int, sensors: list[Sensor]) -> int:
    ranges = [sensor.occupied_range_for_row(row=row) for sensor in sensors]
    ranges = [r for r in ranges if r is not None]
    merged_ranges = merge_ranges(ranges)

    occupied_positions = 0
    for r in merged_ranges:
        occupied_positions += (r.xmax - r.xmin) + 1

    return occupied_positions


def find_distress_beacon_position(max_value: int, sensors: list[Sensor]) -> int:
    available_positions = set()

    for row in range(0, max_value):
        if row % 100000 == 0:
            print(f"At row: {row}")

        ranges = [
            sensor.occupied_range_for_row(row=row, exclude_becon_pos=False)
            for sensor in sensors
        ]
        ranges = [r for r in ranges if r is not None]
        merged_ranges = merge_ranges(ranges)

        for i in range(len(merged_ranges) - 1):
            start = merged_ranges[i].xmax + 1
            for x in range(start, merged_ranges[i + 1].xmin):
                available_positions.add((x, row))

    if len(available_positions) > 1:
        raise ValueError("More than one possible position found!")
    x, y = available_positions.pop()
    return x * 4000000 + y


if __name__ == "__main__":
    sensors = parse_input("input.txt")
    print(
        f"Solution part 1: {find_occupied_positions_at_row(row=2000000, sensors=sensors)}"
    )

    print(
        f"Solution part 2: {find_distress_beacon_position(max_value=4000000, sensors=sensors)}"
    )
