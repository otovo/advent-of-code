use std::fs;

struct MoveCommand {
    amount: usize,
    from: usize,
    to: usize,
}

impl MoveCommand {
    fn from_string(string: &str) -> Self {
        let parts = string.split(" ").collect::<Vec<&str>>();
        Self {
            amount: parts[1].parse::<usize>().unwrap(),
            from: parts[3].parse::<usize>().unwrap(),
            to: parts[5].parse::<usize>().unwrap(),
        }
    }
}

#[derive(Debug)]
struct SupplyStack {
    supplies: Vec<Vec<char>>,
}

impl SupplyStack {

    fn move_cargo_as_stack(&mut self, command: &MoveCommand) {
        let supply_length = self.supplies[command.from - 1].len();
        let range = supply_length - command.amount..;
        let mut popped = self.supplies[command.from - 1].drain(range).collect();
        self.supplies[command.to - 1].append(&mut popped);
    }

    fn move_cargo_amount(&mut self, command: &MoveCommand) {
        for _ in 0..command.amount {
            self.move_cargo(command.from, command.to);
        }
    }

    fn move_cargo(&mut self, from: usize, to: usize) {
        let cargo = self.supplies[from - 1].pop().unwrap();
        self.supplies[to - 1].push(cargo);
    }

    fn from_drawing(drawing: &str) -> SupplyStack {
        let supplie_count = drawing.lines().take(1).next().unwrap().len() / 4 + 1;
        let mut supplies: Vec<Vec<char>> = Vec::with_capacity(supplie_count);
        let first_number_line = drawing.lines().enumerate()
            .find_map(|(index, line)| line.contains('1').then(|| Some(index))).unwrap().unwrap();
        
        let stacks = drawing.lines().take(first_number_line).collect::<Vec<&str>>();

        for i in 0..supplie_count {
            let char_index = i * 4 + 1;
            let mut stack = Vec::new();
            for line in stacks.iter().rev() {
                let char = line.chars().nth(char_index).unwrap();
                if char.is_alphabetic() {
                    stack.push(char);   
                }
            }
            supplies.push(stack);
        }
        
        return SupplyStack { supplies };
    }

    fn top_cargo(&self) -> Vec<char> {
        self.supplies.iter().map(|stack| stack.last().unwrap().clone()).collect()
    }
}
fn main() {

    let input = fs::read_to_string("day5/input.txt").unwrap();

    let mut stack = SupplyStack::from_drawing(input.as_str());
    for line in input.lines() {
        if !line.starts_with("move") {
            continue;
        }
        let command = MoveCommand::from_string(line);
        stack.move_cargo_amount(&command);
    }
    // Joine a vec of chars into a string
    let top_cargo = stack.top_cargo().into_iter().collect::<String>();
 
    println!("{:?}", top_cargo);

    // Part 2
    let mut stack = SupplyStack::from_drawing(input.as_str());
    for line in input.lines() {
        if !line.starts_with("move") {
            continue;
        }
        let command = MoveCommand::from_string(line);
        stack.move_cargo_as_stack(&command);
    }
    // Joine a vec of chars into a string
    let top_cargo = stack.top_cargo().into_iter().collect::<String>();
    println!("{:?}", top_cargo);
}
