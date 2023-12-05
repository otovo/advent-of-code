import numpy as np


def count_view_distance(current_height, trees: np.array, reverse=False):
    view_distance = 0
    trees = reversed(trees) if reverse else trees
    for tree in trees:
        if tree < current_height:
            view_distance += 1
        else:
            return view_distance + 1
    return view_distance


def count_visible_trees_and_highest_scenic_socre(grid: np.array) -> tuple[int, int]:
    visible_from_edge = len(grid[1:-1]) * 2 + len(grid) * 2
    visible = visible_from_edge
    rows, columns = grid.shape
    highest_scenic_socre = 1

    for row in range(1, rows - 1):
        for column in range(1, columns - 1):
            current_height = grid[row, column]
            if max(grid[row, 0:column]) < current_height:  # Visible left
                visible += 1

            elif max(grid[row, column + 1 :]) < current_height:  # Visible right
                visible += 1

            elif max(grid[0:row, column]) < current_height:  # Visible top
                visible += 1

            elif max(grid[row + 1 :, column]) < current_height:  # Visible bottom
                visible += 1

            left_view_distance = count_view_distance(
                current_height, grid[row, 0:column], reverse=True
            )
            right_view_distance = count_view_distance(
                current_height, grid[row, column + 1 :]
            )
            bottom_view_distance = count_view_distance(
                current_height, grid[row + 1 :, column]
            )
            top_view_distance = count_view_distance(
                current_height, grid[0:row, column], reverse=True
            )
            current_scenic_score = (
                left_view_distance
                * right_view_distance
                * top_view_distance
                * bottom_view_distance
            )
            if current_scenic_score > highest_scenic_socre:
                highest_scenic_socre = current_scenic_score
    return visible, highest_scenic_socre


def read_grid(file_name: str) -> np.array:
    grid = []
    with open(file_name, "r") as fp:
        for line in fp:
            heights = []
            for char in line:
                if char.isdigit():
                    heights.append(int(char))
            grid.append(heights)
    return np.array(grid)


if __name__ == "__main__":
    grid = read_grid("input.txt")
    visible_trees, highest_scenic_socre = count_visible_trees_and_highest_scenic_socre(
        grid
    )
    print(f"Part 1, visible from edge: {visible_trees}")
    print(f"Part 2, hightest scenic score: {highest_scenic_socre}")
