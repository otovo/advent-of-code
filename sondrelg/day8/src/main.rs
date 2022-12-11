use std::fs;

/// Check if a tree is visible wrt. the row of trees in front of it
fn tree_is_visible_in_single_direction(height: usize, trees: &Vec<usize>) -> bool {
    for tree in trees {
        if tree >= &height {
            return false;
        }
    }
    true
}

/// Retrieve the number from line x and index y, as usize
fn line_index_as_usize(input: &str, line_index: &usize, char_index: &usize) -> usize {
    input
        .lines()
        .nth(*line_index)
        .unwrap()
        .chars()
        .nth(*char_index)
        .unwrap()
        .to_string()
        .parse::<usize>()
        .unwrap()
}

/// Check whether tree is visible from any direction
fn tree_is_visible(
    tree: usize,
    input: &str,
    tree_index: &usize,
    line_index: &usize,
    grid_x: &usize,
    grid_y: &usize,
) -> u32 {
    // top down
    if {
        let mut trees = vec![];
        for index in 0..*line_index {
            trees.push(line_index_as_usize(
                &input,
                &index,
                &tree_index
            ));
        }
        tree_is_visible_in_single_direction(tree, &trees)
    } {
        return 1;
    };

    // bottom up
    if {
        let mut trees = vec![];
        for index in 0..grid_y - line_index - 1 {
            trees.push(line_index_as_usize(
                &input,
                &(grid_y - index - 1),
                tree_index,
            ));
        }
        tree_is_visible_in_single_direction(tree, &trees)
    } {
        return 1;
    };

    // left right
    if {
        let mut trees = vec![];
        for index in 0..*tree_index {
            trees.push(line_index_as_usize(&input, line_index, &(index as usize)));
        }
        tree_is_visible_in_single_direction(tree, &trees)
    } {
        return 1;
    };

    // right left
    if {
        let mut trees = vec![];
        for index in *tree_index..grid_x - 1 {
            trees.push(line_index_as_usize(
                &input,
                line_index,
                &(index + 1 as usize),
            ));
        }
        tree_is_visible_in_single_direction(tree, &trees)
    } {
        return 1;
    };

    // Not visible
    0
}

fn main() {
    let input = fs::read_to_string("day8/src/input").unwrap();
    let grid_x = input.lines().next().unwrap().len();
    let grid_y = input.lines().map(|_| 1).sum::<usize>();
    let visible_trees = input
        .lines()
        .enumerate()
        .map(|(line_index, line)| {
            line.chars().enumerate()
                .map(|(tree_index, tree_char)| {
                    // Edge nodes are always visible
                    if tree_index == 0
                        || tree_index == grid_x - 1
                        || line_index == 0
                        || line_index == grid_y - 1
                    {
                        1
                    }
                    else {
                        let tree = tree_char.to_string().parse::<usize>().unwrap();
                        tree_is_visible(
                            tree,
                            &input,
                            &tree_index,
                            &line_index,
                            &grid_x,
                            &grid_y
                        )
                    }
                })
                .sum::<u32>()
        })
        .sum::<u32>();
    println!("{}", visible_trees);
}
