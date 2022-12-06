use std::collections::VecDeque;
use std::str::FromStr;
use std::{env, fs};

#[derive(Debug)]
struct Stacks {
    stacks: Vec<Stack>,
}

impl Stacks {
    fn from_input(input: &str, columns: usize, rows: usize) -> Self {
        let mut stacks = vec![];
        for column in 0..columns {
            stacks.push(Stack::from_input(input, column, rows))
        }
        Self { stacks }
    }

    fn move_crate(&mut self, source_stack_index: u32, destination_stack_index: u32) {
        let crate_ = self.stacks[source_stack_index as usize - 1]
            .crates
            .pop_back()
            .unwrap();
        println!(
            "Moving crate {} from stack {} to {}",
            crate_.identifier, source_stack_index, destination_stack_index
        );

        self.stacks[destination_stack_index as usize - 1]
            .crates
            .push_back(crate_);
    }

    fn move_multiple_crates(
        &mut self,
        n: u32,
        source_stack_index: u32,
        destination_stack_index: u32,
    ) {
        let mut crates_to_move = vec![];

        for _ in 0..n {
            crates_to_move.push(
                self.stacks[source_stack_index as usize - 1]
                    .crates
                    .pop_back()
                    .unwrap(),
            )
        }

        println!(
            "Moving crates {:?} from stack {} to {}",
            crates_to_move, source_stack_index, destination_stack_index
        );

        let crate_count = crates_to_move.len();
        for i in 0..crate_count {
            self.stacks[destination_stack_index as usize - 1]
                .crates
                .push_back(crates_to_move[crate_count - i - 1].clone());
        }
    }

    fn execute_commands(&mut self, commands: Commands) {
        for command in commands.commands {
            self.move_multiple_crates(command.quantity, command.source, command.destination)
        }
    }

    fn print_top_crates(self) {
        for stack in self.stacks {
            println!("{}", stack.crates.back().unwrap().identifier)
        }
    }
}

#[derive(Debug)]
struct Stack {
    crates: VecDeque<Crate>,
}

impl Stack {
    fn from_input(input: &str, column: usize, rows: usize) -> Self {
        let mut crates = VecDeque::new();
        for row in 0..rows {
            let identifier = input
                .lines()
                .nth(row)
                .unwrap()
                .chars()
                .nth(((column + 1) * 4) - 3);
            if identifier.is_some() && !identifier.unwrap().to_string().replace(" ", "").is_empty()
            {
                crates.push_front(Crate {
                    identifier: identifier.unwrap(),
                })
            }
        }
        Self { crates }
    }
}

#[derive(Debug, Clone)]
struct Crate {
    identifier: char,
}

#[derive(Debug)]
struct Command {
    quantity: u32,
    source: u32,
    destination: u32,
}

impl Command {
    fn from_line(line: &str) -> Self {
        // 1 from 2 to 1
        let line = line.replace("move ", "");
        let quantity = u32::from_str(line.split(" ").next().unwrap()).unwrap();
        let source = u32::from_str(
            line.split("to")
                .next()
                .unwrap()
                .split("from")
                .last()
                .unwrap()
                .trim(),
        )
        .unwrap();
        let destination = u32::from_str(line.split("to").last().unwrap().trim()).unwrap();
        Self {
            quantity,
            source,
            destination,
        }
    }
}

#[derive(Debug)]
struct Commands {
    commands: Vec<Command>,
}

impl Commands {
    fn from_input(input: &str, starting_index: usize) -> Self {
        let mut commands = vec![];
        for (index, line) in input.lines().enumerate() {
            if index >= starting_index {
                commands.push(Command::from_line(line))
            }
        }
        Self { commands }
    }
}

fn find_separation(input: &str) -> usize {
    let mut separation_index = 0;
    for line in input.lines() {
        if line.is_empty() {
            break;
        }
        separation_index += 1;
    }
    separation_index
}

fn main() {
    let input = fs::read_to_string(format!(
        "{}/src/input",
        &env::var("CARGO_MANIFEST_DIR").unwrap()
    ))
    .unwrap();
    let separation_index = find_separation(&input);
    let columns = 9;
    let mut stacks = Stacks::from_input(&input, columns, separation_index - 1);
    let commands = Commands::from_input(&input, separation_index + 1);
    stacks.execute_commands(commands);
    stacks.print_top_crates();
}
