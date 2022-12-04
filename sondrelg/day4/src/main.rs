use std::str::FromStr;
use std::{env, fs};

#[derive(Debug)]
struct Range {
    start: u32,
    end: u32,
}

impl Range {
    fn from_str(section: &str) -> Range {
        let s = section.split('-').collect::<Vec<&str>>();
        Range {
            start: u32::from_str(s[0]).unwrap(),
            end: u32::from_str(s[1]).unwrap(),
        }
    }

    fn contains(&self, other: &Range) -> bool {
        self.start <= other.start && self.end >= other.end
    }

    fn overlaps_with(&self, other: &Range) -> bool {
        self.start <= other.start && other.start <= self.end
            || self.start <= other.end && other.end <= self.end
    }

    fn contains_contained_or_overlaps_with(&self, other: &Range) -> bool {
        self.contains(other) || other.contains(self) || self.overlaps_with(other)
    }
}

fn main() {
    let input = fs::read_to_string(format!(
        "{}/src/input",
        &env::var("CARGO_MANIFEST_DIR").unwrap()
    ))
    .unwrap();

    let count: u32 = input
        .lines()
        .map(|line| {
            let split = line.split(',').collect::<Vec<&str>>();
            let first_range = Range::from_str(split[0]);
            let second_range = Range::from_str(split[1]);
            u32::from(first_range.contains_contained_or_overlaps_with(&second_range))
        })
        .sum();
    println!("{}", count);
}
