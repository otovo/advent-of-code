from pathlib import Path


def main(input_string: str):
    # part 1
    sums: list[int] = []

    for elf in input_string.split("\n\n"):
        sums.append(sum(map(int, elf.split("\n"))))

    print(max(sums))

    # part 2
    print(sum(sorted(sums, reverse=True)[:3]))


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "input_1.txt"
    with open(input_path) as f:
        input_string = f.read().strip()
    main(input_string)
