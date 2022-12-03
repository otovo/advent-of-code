use std::{env, fs, collections::HashSet};
// utils

pub fn get_file() -> String {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    fs::read_to_string(filename).expect("Could not read file")
}

//day 01
pub fn day_01(input: String) {
    let mut cals: Vec<i32> = Vec::new();
    let mut elf: Vec<i32> = Vec::new();
    
    for line in input.lines() {
        if line.is_empty() {
            cals.push(elf.iter().sum());
            elf.clear();
        }
        else {
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
        if line.is_empty(){
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
        return val - 96
    }
    val - 38
}

fn common_el(elements: &[&str]) -> char {
    let mut sets: Vec<HashSet<_>> = elements
        .iter()
        .map(|e|  e.chars().collect::<HashSet<_>>())
        .collect();
    let mut result = sets.pop().unwrap();
    result.retain(|item| {
        sets.iter().all(|set| set.contains(item))
    });
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
