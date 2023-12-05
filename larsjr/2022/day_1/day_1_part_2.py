from day_1_part_1 import get_calories_by_elf


def get_sum_top_three_elfs(calories_by_elf: dict[int, int]):
    sorted_clories = sorted(calories_by_elf.values(), reverse=True)
    return sum(sorted_clories[0:3])


if __name__ == "__main__":
    calories_by_elf = get_calories_by_elf("elfs_and_calories.txt")
    print(get_sum_top_three_elfs(calories_by_elf))
