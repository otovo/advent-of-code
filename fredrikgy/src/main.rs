use std::{env, fs};

pub fn get_file() -> String {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    fs::read_to_string(filename).expect("Could not read file")
}

fn main() {
    let input = get_file();
    advent_of_rust::SOLUTIONS[0](input);
}
