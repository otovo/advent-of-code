// Start of a package: 4 characters in a row that are different
use std::{env, fs};

fn packet_start(input: &str) -> Option<(Vec<char>, usize)> {
    let mut sequence = vec![];
    for (index, character) in input.chars().enumerate() {
        if sequence.len() == 14 {
            return Some((sequence, index));
        } else if sequence.contains(&character) {
            let position = sequence.iter().position(|&ch| ch == character).unwrap() + 1;
            sequence = sequence[position..].to_vec();
            sequence.push(character);
        } else {
            sequence.push(character);
        }
    }
    None
}

fn main() {
    let input = fs::read_to_string(format!(
        "{}/src/input",
        &env::var("CARGO_MANIFEST_DIR").unwrap()
    ))
    .unwrap();

    if let Some((sequence, index)) = packet_start(&input) {
        println!("Found sequence {:?} at index {}", sequence, index)
    }
}
