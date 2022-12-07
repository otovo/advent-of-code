use itertools::Itertools;
use std::collections::{HashMap, HashSet};
// I'm keeping it all in one file so that i can easily reference previous days, and keep track of
// how many lines I've written total

pub static SOLUTIONS: [fn(String); 7] = [day_07, day_06, day_05, day_04, day_03, day_02, day_01];

//day 01
pub fn day_01(input: String) {
    let mut cals: Vec<i32> = Vec::new();
    let mut elf: Vec<i32> = Vec::new();

    for line in input.lines() {
        if line.is_empty() {
            cals.push(elf.iter().sum());
            elf.clear();
        } else {
            elf.push(line.parse::<i32>().unwrap());
        }
    }
    let part1 = cals.iter().max().unwrap();
    println!("part 1: {}", part1);

    cals.sort_unstable();
    let part2: i32 = cals.iter().rev().take(3).sum();
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
        let start: &str;
        let end: &str;
        (start, end) = data.split_once('-').unwrap();

        Shift {
            start: start.parse().unwrap(),
            end: end.parse().unwrap(),
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
        .map(|line| {
            line.split_once(',')
                .map(|(p1, p2)| (Shift::new(p1), Shift::new(p2)))
                .unwrap()
        })
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
    stacks: [Vec<char>; 9],
    moves: Vec<(usize, usize, usize)>,
}

impl CrateStacks {
    fn new(input: String) -> CrateStacks {
        let mut stacks: [Vec<char>; 9] = Default::default();
        let mut moves: Vec<(usize, usize, usize)> = Default::default();

        for line in input.lines() {
            // blank row is empty or 1
            let second_column_char = line.chars().nth(1).unwrap_or('1');
            //m[o]ve
            if second_column_char == 'o' {
                moves.push(
                    line.split(' ')
                        .skip(1)
                        .step_by(2)
                        .map(|el| el.parse::<usize>().unwrap())
                        .into_iter()
                        .next_tuple()
                        .unwrap(),
                );
            } else if second_column_char != '1' {
                line.chars()
                    .skip(1)
                    .step_by(4)
                    .enumerate()
                    .filter(|(_i, el)| *el != ' ')
                    .for_each(|(i, el)| stacks[i].push(el));
            }
        }
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
        self.stacks
            .iter()
            .map(|el| *el.first().unwrap_or(&'.'))
            .collect()
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
