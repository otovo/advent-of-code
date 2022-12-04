use std::fs;
use std::ops::Range;

trait ToRange {
    fn to_range(&self) -> Range<i32>;
}

impl ToRange for str {
    fn to_range(&self) -> Range<i32> {
        let (first, second) = self.split_once("-").unwrap();
        let first = first.parse::<i32>().unwrap();
        let second = second.parse::<i32>().unwrap();
        first..second
    }
}

fn main() {
    let input = fs::read_to_string("input.txt").unwrap();
    let assignments = input.split("\n")
        .map(|line| line.split_once(",").unwrap()).collect::<Vec<(&str, &str)>>();
    let ranges: Vec<(Range<i32>, Range<i32>)> = assignments.iter()
        .map(|(first, second)| (first.to_range(), second.to_range())).collect();
    let number_of_overlaps = ranges.iter().map(|(first, second)| {
        if first.start <= second.start && second.end <= first.end {
            1
        } else if second.start <= first.start && first.end <= second.end {
            1
        } else {
            0
        }
    }).sum::<i32>();
    println!("Part 1: {}", number_of_overlaps);

    let number_of_partially_overlap = ranges.iter().map(|(first, second)| {
        let end_difference = second.start - first.end;
        let start_difference = second.end - first.start;
        // Checking if the numerator is differnet in the differences, or a 0 value
        if end_difference >= 0 && start_difference <= 0 {
            1
        } else if end_difference <= 0 && start_difference >= 0 {
            1
        } else {
            0
        }
    }).sum::<i32>();
    println!("Part 2: {}", number_of_partially_overlap)
}
