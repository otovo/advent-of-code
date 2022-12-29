from pathlib import Path


def char_to_priority(char: str):
    if char.islower():
        return ord(char) - ord("a") + 1
    return ord(char) - ord("A") + 27


def main(input_string: str):
    lines = input_string.split("\n")

    # part 1
    sum_priotities = 0

    for line in lines:
        assert len(line) % 2 == 0
        middle_index = len(line) // 2
        first_half, second_half = line[:middle_index], line[middle_index:]
        shared_char = list(set(first_half).intersection(second_half))[0]
        sum_priotities += char_to_priority(shared_char)

    print(sum_priotities)

    # part 2
    sum_priotities = 0

    for i in range(0, len(lines), 3):
        first, second, third = lines[i : i + 3]
        shared_char = list(set(first).intersection(second, third))[0]
        sum_priotities += char_to_priority(shared_char)

    print(sum_priotities)


if __name__ == "__main__":
    input_path = Path(__file__).parents[1] / "inputs" / "input_3.txt"
    with open(input_path) as f:
        input_string = f.read().strip()
    main(input_string)
