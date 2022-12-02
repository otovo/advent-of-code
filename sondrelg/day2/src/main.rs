#[derive(Eq, PartialEq)]
enum Strategy {
    Rock,
    Paper,
    Scissor,
}

impl Strategy {
    fn from_char(c: &char) -> Self {
        match c {
            'A' => Self::Rock,
            'B' => Self::Paper,
            'C' => Self::Scissor,
            _ => panic!("Unhandled strategy")
        }
    }

    fn from_opponent_strategy(strategy: &Strategy) -> Self {
        match strategy {
            Self::Rock => Self::Paper,
            Self::Paper => Self::Scissor,
            Self::Scissor => Self::Rock,
        }
    }

    fn points(self) -> u8 {
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

    fn points(&self) -> u8 {
        match self {
            Self::Loss => 0,
            Self::Draw => 3,
            Self::Win => 6,
        }
    }
}


fn main() {
    let opponent_choices = ['A', 'B', 'C'];

    let points: u8 = opponent_choices.iter().map(|opponent_choice| {
        // Convert choice to strategy
        let opponent_strategy = Strategy::from_char(opponent_choice);
        // Choose a winning strategy
        let my_strategy = Strategy::from_opponent_strategy(&opponent_strategy);
        // Calculate score
        Outcome::from_strategies(&opponent_strategy, &my_strategy).points() + my_strategy.points()
    }).sum();

    println!("The optimal strategy results in {} points", points)
}
