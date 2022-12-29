from pathlib import Path


def main(input_string: str):
    lines = input_string.split("\n")

    num_fully_overlapping_pairs = 0
    num_overlapping_pairs = 0

    for line in lines:
        elf1, elf2 = line.split(",")
        elf1_lower, elf1_upper = list(map(int, elf1.split("-")))
        elf2_lower, elf2_upper = list(map(int, elf2.split("-")))

        # part 1
        if (elf1_lower <= elf2_lower and elf1_upper >= elf2_upper) or (
            elf2_lower <= elf1_lower and elf2_upper >= elf1_upper
        ):
            num_fully_overlapping_pairs += 1

        # part 2
        if elf1_lower <= elf2_upper and elf2_lower <= elf1_upper:
            num_overlapping_pairs += 1

    print(num_fully_overlapping_pairs)
    print(num_overlapping_pairs)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "input_4.txt"
    with open(input_path) as f:
        input_string = f.read().strip()
    main(input_string)
