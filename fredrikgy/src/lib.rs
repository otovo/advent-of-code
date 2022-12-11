use itertools::Itertools;
use std::collections::{HashMap, HashSet};
// I'm keeping it all in one file so that i can easily reference previous days, and keep track of
// how many lines I've written total

pub static SOLUTIONS: [fn(String); 11] = [
    day_11, day_10, day_09, day_08, day_07, day_06, day_05, day_04, day_03, day_02, day_01,
];

//day 01
pub fn day_01(input: String) {
    let mut group_sums = input
        .split("\n\n")
        .map(|el| {
            el.lines()
                .filter_map(|n| n.parse::<u32>().ok())
                .sum::<u32>()
        })
        .collect_vec();
    let part1 = group_sums.iter().max().unwrap();
    println!("part 1: {}", part1);

    group_sums.sort_unstable();
    let part2 = group_sums.iter().rev().take(3).sum::<u32>();
    println!("part 2: {}", part2);
}

//day 02
pub fn day_02(input: String) {
    let mut total1: u32 = 0;
    let mut total2: u32 = 0;
    for line in input.lines() {
        if line.is_empty() {
            break;
        }
        match line {
            "A X" | "B Y" | "C Z" => total1 += 3,
            "A Y" | "B Z" | "C X" => total1 += 6,
            _ => (),
        }
        let op = line.chars().next().unwrap() as u32;
        let me = line.chars().nth(2).unwrap() as u32;
        total1 += me - 87;

        match me {
            89 => total2 += 3,
            90 => total2 += 6,
            _ => (),
        }

        let z: i32 = (op as i32 - 65) + (me as i32 - 89);
        let m = ((z % 3) + 3) % 3; // modulus 3
        total2 += (m + 1) as u32;
    }
    println!("part 1: {}", total1);
    println!("part 2: {}", total2);
}

//day 03
fn letter_to_priority(l: &char) -> u32 {
    let val = *l as u32;
    if val > 96 {
        return val - 96;
    }
    val - 38
}

fn common_el(elements: &[&str]) -> char {
    let mut sets: Vec<HashSet<_>> = elements
        .iter()
        .map(|e| e.chars().collect::<HashSet<_>>())
        .collect();
    let mut result = sets.pop().unwrap();
    result.retain(|item| sets.iter().all(|set| set.contains(item)));
    return *result.iter().next().unwrap();
}

pub fn day_03(input: String) {
    let mut part1: u32 = 0;
    for line in input.lines() {
        let mid = line.len() / 2;
        let a: HashSet<char> = line[..mid].chars().collect();
        let b: HashSet<char> = line[mid..].chars().collect();
        let el = a.intersection(&b).into_iter().next().unwrap();
        part1 += letter_to_priority(el);
    }
    println!("part 1: {}", part1);

    let mut part2: u32 = 0;
    let mut lines = input.lines().peekable();
    while lines.peek().is_some() {
        let chunk: Vec<_> = lines.by_ref().take(3).collect();
        let badge = common_el(&chunk);
        part2 += letter_to_priority(&badge);
    }
    println!("part 2: {}", part2);
}

//day 04

struct Shift {
    start: u32,
    end: u32,
}

impl Shift {
    fn new(data: &str) -> Shift {
        let parts: (u32, u32) = data
            .splitn(2, '-')
            .filter_map(|el| el.parse::<u32>().ok())
            .collect_tuple()
            .unwrap();

        Shift {
            start: parts.0,
            end: parts.1,
        }
    }

    fn contains(&self, other: &Shift) -> bool {
        self.start <= other.start && self.end >= other.end
    }

    fn contains_or_contained_by(&self, other: &Shift) -> bool {
        self.contains(other) || other.contains(self)
    }

    fn overlaps(&self, other: &Shift) -> bool {
        self.contains_or_contained_by(other)
            || (self.start <= other.end && other.end <= self.end)
            || (self.start <= other.start && other.start <= self.end)
    }
}

pub fn day_04(input: String) {
    let pairs: Vec<(Shift, Shift)> = input
        .lines()
        .filter_map(|pair| pair.split(',').map(Shift::new).collect_tuple())
        .collect();

    let part1 = pairs
        .iter()
        .filter(|(p1, p2)| p1.contains_or_contained_by(p2))
        .count();
    println!("part 1: {}", part1);

    let part2 = pairs.iter().filter(|(p1, p2)| p1.overlaps(p2)).count();
    println!("part 2: {}", part2);
}

//day 05
struct CrateStacks {
    stacks: Vec<Vec<char>>,
    moves: Vec<(usize, usize, usize)>,
}

impl CrateStacks {
    fn new(input: String) -> CrateStacks {
        let parts = input.split_once("\n\n").unwrap();
        let num_stacks = (1 + parts.0.lines().next().unwrap().len()) / 4;
        let stacks = (0..num_stacks)
            .map(|i| {
                parts
                    .0
                    .lines()
                    .filter_map(|line| line.chars().skip(1).nth(4 * i))
                    .filter(|&el| el != ' ')
                    .collect_vec()
            })
            .collect_vec();
        let moves = parts
            .1
            .lines()
            .map(|line| {
                line.split(' ')
                    .skip(1)
                    .step_by(2)
                    .filter_map(|el| el.parse::<usize>().ok())
                    .collect_tuple()
                    .unwrap()
            })
            .collect_vec();
        CrateStacks { stacks, moves }
    }

    fn rearange(&self, li_fo: bool) -> CrateStacks {
        let mut stacks = self.stacks.clone();
        for (crates, from, to) in &self.moves {
            let (to_move, to_remain) = stacks[from - 1].split_at(*crates);
            let mut new_to = to_move.to_vec();

            if li_fo {
                new_to.reverse();
            }
            new_to.extend(&stacks[to - 1]);
            stacks[from - 1] = to_remain.to_vec();
            stacks[to - 1] = new_to.clone();
        }
        CrateStacks {
            stacks,
            moves: self.moves.clone(),
        }
    }

    fn top_crates(&self) -> String {
        self.stacks.iter().filter_map(|el| el.first()).collect()
    }
}
pub fn day_05(input: String) {
    let crate_stack = CrateStacks::new(input);

    println!("part1: {}", crate_stack.rearange(true).top_crates());
    println!("part2: {}", crate_stack.rearange(false).top_crates());
}

//day 06
fn signal_search(input: &[char], win: usize) -> usize {
    for (i, window) in input.windows(win).enumerate() {
        let signal_length = window.iter().collect::<HashSet<_>>().len();
        if signal_length == win {
            return i + win;
        }
    }
    panic!("Could not find signal")
}

pub fn day_06(input: String) {
    let iv = input.chars().collect_vec();
    println!("part1: {}", signal_search(&iv, 4));
    println!("part2: {}", signal_search(&iv, 14));
}

//day 07
pub fn day_07(input: String) {
    let mut directories = HashMap::new();
    let mut stack = Vec::new();

    for line in input.lines() {
        if line.starts_with("$ ls") || line.starts_with("dir") {
            continue;
        }
        let parts = line.split_whitespace().collect_vec();
        match parts[..] {
            ["$", "cd", ".."] => {
                stack.pop();
            }
            ["$", "cd", name] => {
                stack.push(name);
            }
            [s, _] => {
                let size = s.parse::<u32>().unwrap();
                for idx in 1..=stack.len() {
                    let path = stack[..idx].join("/");
                    *directories.entry(path).or_insert(0) += size;
                }
            }
            _ => (),
        }
    }

    let part1: u32 = directories.values().filter(|&el| *el < 100000).sum();
    println!("part1: {}", part1);

    let target = directories.get("/").unwrap() - 40000000;
    let part2 = directories
        .values()
        .filter(|&el| el > &target)
        .min()
        .unwrap();
    println!("part2: {}", part2);
}

//day 08

type TreeMap = Vec<Vec<u32>>;
fn visibility(trees: &TreeMap, coord: &(usize, usize)) -> usize {
    let &(row, col) = coord;
    let tree = &trees[row][col];
    let left = trees[row][..col].iter().max().unwrap() < tree;
    let right = trees[row][col + 1..].iter().max().unwrap() < tree;
    let over = trees.iter().take(row).map(|r| &r[col]).max().unwrap() < tree;
    let under = trees.iter().skip(row + 1).map(|r| &r[col]).max().unwrap() < tree;
    (left || right || over || under) as usize
}

fn scenic_score(trees: &TreeMap, coord: &(usize, usize)) -> usize {
    // All the wierd unwraps is to handle hitting the boundary
    // ideally a take_until().count() whould probably make this alot better

    let &(row, col) = coord;
    let tree = &trees[row][col];
    let dim = trees.len();
    let left = 1 + trees[row][..col]
        .iter()
        .rev()
        .position(|el| el >= tree)
        .unwrap_or(col - 1);
    let right = 1 + trees[row][col + 1..]
        .iter()
        .position(|el| el >= tree)
        .unwrap_or(dim - col - 2);
    let over = 1 + trees
        .iter()
        .take(row)
        .map(|r| r[col])
        .rev()
        .position(|el| &el >= tree)
        .unwrap_or(row - 1);
    let under = 1 + trees
        .iter()
        .skip(row + 1)
        .map(|r| r[col])
        .position(|el| &el >= tree)
        .unwrap_or(dim - row - 2);
    left * right * over * under
}

pub fn day_08(input: String) {
    let trees = input
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect_vec())
        .collect_vec();
    let dim = trees.len();
    let part1: usize = (1..dim - 1)
        .cartesian_product(1..dim - 1)
        .map(|coord| visibility(&trees, &coord))
        .sum();
    println!("part1: {}", part1 + dim * 4 - 4);

    let part2: usize = (1..dim - 1)
        .cartesian_product(1..dim - 1)
        .map(|coord| scenic_score(&trees, &coord))
        .max()
        .unwrap();
    println!("part2: {}", part2);
}

// day 09
type Pos = (i32, i32);
fn move_head(from: Pos, direction: char) -> Pos {
    match direction {
        'R' => (from.0 + 1, from.1),
        'L' => (from.0 - 1, from.1),
        'U' => (from.0, from.1 + 1),
        'D' => (from.0, from.1 - 1),
        _ => panic!("Could not parse direction"),
    }
}

fn move_tail(from: Pos, head: Pos) -> Pos {
    if from.0.abs_diff(head.0) < 2 && from.1.abs_diff(head.1) < 2 {
        return from;
    }
    let (dx, dy) = (
        (head.0 - from.0).clamp(-1, 1),
        (head.1 - from.1).clamp(-1, 1),
    );
    (from.0 + dx, from.1 + dy)
}

pub fn day_09(input: String) {
    //parse
    let moves = input
        .lines()
        .filter_map(|el| el.split_once(' '))
        .map(|(dir, n)| (dir.chars().next().unwrap(), n.parse::<i32>().unwrap()))
        .collect_vec();

    //part 1
    let mut head = (0, 0);
    let mut tail = (0, 0);
    let mut visited: HashSet<Pos> = HashSet::new();
    visited.insert(tail);
    for &(dir, n) in &moves {
        for _ in 0..n {
            head = move_head(head, dir);
            tail = move_tail(tail, head);
            visited.insert(tail);
        }
    }
    println!("part1: {}", visited.len());

    //part 2
    visited.clear();
    head = (0, 0);
    visited.insert(head);
    let mut tails: Vec<Pos> = (0..9).map(|_| (0, 0)).collect_vec();
    for &(dir, n) in &moves {
        for _ in 0..n {
            head = move_head(head, dir);
            tails = tails
                .iter()
                .scan(head, |to, from| {
                    *to = move_tail(*from, *to);
                    Some(*to)
                })
                .collect_vec();
            visited.insert(*tails.last().unwrap());
        }
    }
    println!("part2: {}", visited.len());
}

//day 10
pub fn day_10(input: String) {
    let commands = input
        .lines()
        .map(|el| {
            let tup = el.split_once(' ');
            match tup {
                Some(a) => (2, a.1.parse::<i32>().unwrap()),
                _ => (1, 0),
            }
        })
        .scan((0, 1), |(cyc, reg), (inc_cyc, inc_reg)| {
            for x in 0..inc_cyc {
                let i: i32 = (*cyc + x) % 40;
                if i.abs_diff(*reg) < 2 {
                    print!("▒");
                } else {
                    print!(" ");
                }
                if i == 39 {
                    println!();
                }
            }

            *cyc += inc_cyc;
            *reg += inc_reg;
            Some((*cyc, *reg))
        })
        .fold((20, 0), |(target, signal), (cyc, reg)| {
            if target - cyc <= 2 {
                (target + 40, signal + (reg * target))
            } else {
                (target, signal)
            }
        });
    println!("part1: {}", commands.1);
}

//day 11
struct Monkey {
    operation: char,
    operand: Option<usize>,
    test: usize,
    true_dest: usize,
    false_dest: usize,
}
impl Monkey {
    fn new(input: &str) -> (Monkey, Vec<usize>) {
        let mut lines = input.lines().skip(1);
        let items = lines
            .next()
            .unwrap()
            .split_once(": ")
            .unwrap()
            .1
            .split(", ")
            .map(|x| x.parse::<usize>().unwrap())
            .collect_vec();
        let (operand, operation) = lines
            .next()
            .unwrap()
            .rsplitn(3, ' ')
            .take(2)
            .collect_tuple()
            .unwrap();
        let (test, true_dest, false_dest) = lines
            .map(|l| l.rsplit_once(' ').unwrap().1.parse::<usize>().unwrap())
            .collect_tuple()
            .unwrap();
        (
            Monkey {
                test,
                true_dest,
                false_dest,
                operation: operation.chars().next().unwrap(),
                operand: operand.parse::<usize>().ok(),
            },
            items,
        )
    }

    fn get_move<F: Fn(usize) -> usize>(&self, items: &[usize], reducer: F) -> Vec<(usize, usize)> {
        items
            .iter()
            .map(|&el| {
                let other = self.operand.unwrap_or(el);
                let new_value = match self.operation {
                    '+' => reducer(el + other),
                    '*' => reducer(el * other),
                    _ => panic!("Unrecognised operation"),
                };

                match new_value % self.test {
                    0 => (new_value, self.true_dest),
                    _ => (new_value, self.false_dest),
                }
            })
            .collect_vec()
    }
}

fn do_monkey_rounds<F: Fn(usize) -> usize>(
    items: &mut [Vec<usize>],
    monkeys: &Vec<Monkey>,
    rounds: usize,
    reducer: &F,
) -> usize {
    let mut monkey_business = vec![0; monkeys.len()];
    for _ in 0..rounds {
        for (i, monkey) in monkeys.iter().enumerate() {
            for (new_val, dest) in monkey.get_move(&items[i], reducer) {
                items[dest].push(new_val);
                monkey_business[i] += items[i].len();
                items[i].clear();
            }
        }
    }
    monkey_business
        .iter()
        .sorted()
        .rev()
        .take(2)
        .product::<usize>()
}

pub fn day_11(input: String) {
    let sections = input.split("\n\n");
    let (monkeys, mut items): (Vec<_>, Vec<_>) = sections.map(Monkey::new).unzip();
    let part = |x: usize| x % monkeys.iter().map(|x| x.test).product::<usize>();

    let part1 = do_monkey_rounds(&mut items.clone(), &monkeys, 20, &|x: usize| x / 3);
    let part2 = do_monkey_rounds(&mut items, &monkeys, 10000, &part);

    println!("part1: {}", part1);
    println!("part2: {}", part2);
}
