use std::{collections::HashSet};
use std::fs;

trait Runstack {
    fn priority(&self) -> i32;
}

impl Runstack for str {
    fn priority(&self) -> i32 {
        let mut first_compartment: HashSet<String> = HashSet::new();
        let (first, second) = self.split_at(self.len() / 2);
        for char in first.chars() {
            first_compartment.insert(char.to_string());
        }
        for char in second.chars() {
            if first_compartment.contains(&char.to_string()) {
                return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".find(char).unwrap() as i32 + 1
            }
        }
        panic!("Unable to find a conflict")
    }
}

fn main() {
    let input = fs::read_to_string("day3/input.txt").unwrap();
    let total: i32 = input.split("\n").map(|string| string.priority()).sum();
    println!("{}", total)
}
