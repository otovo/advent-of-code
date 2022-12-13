use std::fs;
use std::str::FromStr;

#[derive(Debug)]
enum Instruction {
    Add { val: i32 },
    Noop,
}

impl Instruction {
    fn from_str(s: &str) -> Self {
        match s.chars().next().unwrap() {
            'a' => {
                let (_, value) = s.split_at(5);
                Self::Add {
                    val: i32::from_str(value).unwrap(),
                }
            }
            'n' => Self::Noop,
            _ => panic!("Unexpected first character"),
        }
    }

    fn cycles(&self) -> i32 {
        match self {
            Self::Noop => 1,
            Self::Add { .. } => 2,
        }
    }

    fn value_to_add(&self) -> i32 {
        if let Instruction::Add { val: value } = self {
            *value
        } else {
            0
        }
    }
}

fn sum_signal_strengths(input: &str) {
    let mut sum = 0;

    let mut cycle = 0;
    let mut register_x = 1;
    let mut interval_count = 0;

    input.lines().into_iter().for_each(|line| {
        let instruction = Instruction::from_str(line);

        for _ in 0..instruction.cycles() {
            cycle += 1;

            // Register signal strengths
            if cycle == 20 + 40 * interval_count {
                interval_count += 1;
                sum += register_x * cycle;
            }
        }
        register_x += instruction.value_to_add();
    });
    println!("{}", sum);
}

fn main() {
    let input = fs::read_to_string("day10/src/input").unwrap();
    sum_signal_strengths(&input)
}
