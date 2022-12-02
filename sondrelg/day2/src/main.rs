use std::{env, fs};
use std::ops::Index;
use std::path::Path;

#[derive(Eq, PartialEq)]
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
            "X" => Self::Rock,
            "Y" => Self::Paper,
            "Z" => Self::Scissor,
            _ => panic!("Unhandled strategy: {c}")
        }
    }

    fn from_opponent_strategy(strategy: &Strategy) -> Self {
        match strategy {
            Self::Rock => Self::Paper,
            Self::Paper => Self::Scissor,
            Self::Scissor => Self::Rock,
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

enum Outcome {
    Loss,
    Draw,
    Win,
}

impl Outcome {
    fn from_strategies(opponent_strategy: &Strategy, my_strategy: &Strategy) -> Self {
        if my_strategy == &Strategy::from_opponent_strategy(opponent_strategy) {
            Self::Win
        } else if opponent_strategy == &Strategy::from_opponent_strategy(my_strategy) {
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


fn main() {
    let input_path = format!("{}/src/input", &env::var("CARGO_MANIFEST_DIR").unwrap());
    println!("{}", input_path);
    let path = Path::new(&input_path);
    let contents = fs::read_to_string(path).unwrap();
    let points: u16 = contents.lines().into_iter().map(|line| {
        // Load choices
        let split = line.split(" ").collect::<Vec<&str>>();
        let (opponent_choice, my_choice) = (split.index(0), split.index(1));
        // Convert choice to strategy
        let opponent_strategy = Strategy::from_char(opponent_choice);
        let my_strategy = Strategy::from_char(my_choice);
        // Calculate score
        Outcome::from_strategies(&opponent_strategy, &my_strategy).points() + my_strategy.points()
    }).sum();

    println!("The game produced {} points", points)
}
