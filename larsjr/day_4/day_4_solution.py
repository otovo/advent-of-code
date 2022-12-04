def is_subrange(range: range, test_range: range) -> bool:
    return test_range.start in range and test_range[-1] in range


def ranges_overlap(range1: range, range2: range) -> bool:
    if range1.start in range2 or range1[-1] in range2:
        return True
    if range2.start in range1 or range2[-1] in range1:
        return True
    return False


def create_range(range_representation: str) -> range:
    elements = range_representation.split("-")

    return range(int(elements[0]), int(elements[1]) + 1)


def count_sub_ranges(ranges: list[tuple[range, range]]) -> int:
    contained_ranges = 0
    for range1, range2 in ranges:
        if is_subrange(range1, range2):
            contained_ranges += 1
        elif is_subrange(range2, range1):
            contained_ranges += 1

    return contained_ranges


def count_overlaps(ranges: list[tuple[range, range]]) -> int:
    overlaps = 0
    for range1, range2 in ranges:
        if ranges_overlap(range1, range2):
            overlaps += 1

    return overlaps


if __name__ == "__main__":
    with open("input.txt", "r") as fp:
        lines = fp.readlines()

    ranges = []
    for line in lines:
        elements = line.split(",")
        first_range = create_range(elements[0])
        second_range = create_range(elements[1].strip())
        ranges.append((first_range, second_range))

    print(
        f"Number of ranges fully contained in other range: {count_sub_ranges(ranges)}"
    )

    print(f"Number of overlaps: {count_overlaps(ranges)}")
