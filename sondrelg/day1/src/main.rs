use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::str::FromStr;

fn main() {
    let input_path = format!("{}/src/input", &env::var("CARGO_MANIFEST_DIR").unwrap());
    let path = Path::new(&input_path);
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);

    let mut elf = 0;
    let mut calories: Vec<u32> = vec![0];

    for line in reader.lines() {
        let line = line.unwrap();

        if line.is_empty() {
            elf += 1;
            continue;
        }

        let line_calories = u32::from_str(&line).unwrap();
        let entry = calories.get(elf).unwrap_or(&0_u32);
        if calories.len() == elf {
            calories.insert(elf, entry + line_calories);
        } else {
            calories[elf] = entry + line_calories;
        }
    }

    let mut most = 0;
    let mut second_most = 0;
    let mut third_most = 0;

    for i in &calories {
        if i > &most {
            third_most = second_most;
            second_most = most;
            most = *i;
        } else if i > &second_most {
            third_most = second_most;
            second_most = *i;
        } else if i > &third_most {
            third_most = *i;
        }
    }

    let max_index = calories.iter().position(|&r| r == most).unwrap();
    let second_max_index = calories.iter().position(|&r| r == second_most).unwrap();
    let third_max_index = calories.iter().position(|&r| r == third_most).unwrap();
    println!(
        "The most calories was {} and was held by elf {}",
        most,
        max_index + 1
    );
    println!(
        "The second most calories was {} and was held by elf {}",
        second_most,
        second_max_index + 1
    );
    println!(
        "The third most calories was {} and was held by elf {}",
        most,
        third_max_index + 1
    );
    println!("Total {}", most + second_most + third_most);
}
