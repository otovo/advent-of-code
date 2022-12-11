#![allow(dead_code)]
use std::ops::Index;
use std::path::Path;
use std::{env, fs};

#[derive(Eq, PartialEq, Clone)]
enum Strategy {
    Rock,
    Paper,
    Scissor,
}

impl Strategy {
    fn from_char(c: &str) -> Self {
        match c {
            "A" => Self::Rock,
            "B" => Self::Paper,
            "C" => Self::Scissor,
            _ => panic!("Unhandled strategy: {c}"),
        }
    }

    fn from_desired_outcome(outcome: &Outcome, opponent_strategy: &Strategy) -> Self {
        match outcome {
            Outcome::Draw => opponent_strategy.clone(),
            Outcome::Loss => match opponent_strategy {
                Self::Rock => Self::Scissor,
                Self::Paper => Self::Rock,
                Self::Scissor => Self::Paper,
            },
            Outcome::Win => match opponent_strategy {
                Self::Rock => Self::Paper,
                Self::Paper => Self::Scissor,
                Self::Scissor => Self::Rock,
            },
        }
    }

    fn points(self) -> u16 {
        match self {
            Self::Rock => 1,
            Self::Paper => 2,
            Self::Scissor => 3,
        }
    }
}

#[derive(Debug)]
enum Outcome {
    Loss,
    Draw,
    Win,
}

impl Outcome {
    fn from_char(c: &str) -> Self {
        match c {
            "X" => Self::Loss,
            "Y" => Self::Draw,
            "Z" => Self::Win,
            _ => panic!("Unhandled outcome: {c}"),
        }
    }

    fn from_strategies(opponent_strategy: &Strategy, my_strategy: &Strategy) -> Self {
        if my_strategy == &Strategy::from_desired_outcome(&Outcome::Win, opponent_strategy) {
            Self::Win
        } else if opponent_strategy == &Strategy::from_desired_outcome(&Outcome::Loss, my_strategy)
        {
            Self::Loss
        } else {
            Self::Draw
        }
    }

    fn points(&self) -> u16 {
        match self {
            Self::Loss => 0,
            Self::Draw => 3,
            Self::Win => 6,
        }
    }
}

fn calc(content: String) -> u16 {
    // Iterate over each set of items
    content
        .lines()
        .into_iter()
        .map(|line| {
            // Parse choices
            let split = line.split(' ').collect::<Vec<&str>>();
            let (opponent_choice, outcome) = (split.index(0), split.index(1));

            // Convert choice to strategy
            let opponent_strategy = Strategy::from_char(opponent_choice);
            let desired_outcome = Outcome::from_char(outcome);
            let strategy = Strategy::from_desired_outcome(&desired_outcome, &opponent_strategy);

            // Calculate score
            strategy.points() + desired_outcome.points()
        })
        .sum()
}

fn main() {
    let input_path = format!("{}/src/input", &env::var("CARGO_MANIFEST_DIR").unwrap());
    let path = Path::new(&input_path);
    let content = fs::read_to_string(path).unwrap();
    let points = calc(content);
    println!("The game produced {} points", points)
}
