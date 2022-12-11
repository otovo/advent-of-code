use std::collections::HashMap;
use std::str::FromStr;
use std::{env, fs};

enum Commands {
    Cd,
    Ls,
}

fn parse_cd(line: &str, current_dir: String) -> String {
    // Just assume `/` at index 5 means cd /
    if line.chars().collect::<Vec<char>>()[5] == '/' {
        println!("cd to root");
        return String::from("root");
    }

    // Parse target dir
    let target = line.chars().collect::<Vec<char>>()[5..]
        .into_iter()
        .collect::<String>();

    if &target == ".." {
        let pieces = current_dir.split("/").into_iter().collect::<Vec<&str>>();
        let mut new_directory = String::new();
        for i in 0..pieces.len() - 1 {
            new_directory += &format!("{}/", pieces[i]);
        }
        new_directory.pop();
        println!("cd back to {}", new_directory);
        return new_directory;
    }

    let new = current_dir + &format!("/{}", target);
    println!("cd to {}", new);
    new
}

fn main() {
    let input = fs::read_to_string(format!(
        "{}/src/input",
        &env::var("CARGO_MANIFEST_DIR").unwrap()
    ))
    .unwrap();
    let mut size_tree: HashMap<String, u32> = HashMap::new();
    let mut directory_tree: HashMap<String, Vec<String>> = HashMap::new();

    let mut current_command: Option<Commands> = None;

    // Keep this as a variable, so we can read multiple times in a loop as needed
    let mut lines = input.lines();

    // Keep these to record the contents of each dir
    let mut current_directory = String::from("root");
    let mut current_directory_directories = vec![];
    let mut current_directory_file_size = 0;

    loop {
        // Read line
        let line = match lines.next() {
            None => break,
            Some(t) => t,
        };

        // Parse command
        if line.starts_with('$') {
            match line.chars().collect::<Vec<char>>()[2] {
                'c' => {
                    // Clear the contents of the last dir before moving
                    {
                        // Record
                        if size_tree.contains_key(&current_directory) {
                            *size_tree.get_mut(&current_directory).unwrap() +=
                                current_directory_file_size;
                            directory_tree
                                .get_mut(&current_directory)
                                .unwrap()
                                .append(&mut current_directory_directories);
                        } else {
                            size_tree.insert(
                                current_directory.clone(),
                                current_directory_file_size.clone(),
                            );
                            directory_tree.insert(
                                current_directory.clone(),
                                current_directory_directories.clone(),
                            );
                        }

                        // Clear
                        current_directory_directories = vec![];
                        current_directory_file_size = 0;
                    }

                    current_directory = parse_cd(&line, current_directory);
                    current_command = Some(Commands::Cd);
                    continue;
                }
                'l' => {
                    println!("ls");
                    current_command = Some(Commands::Ls);
                    continue;
                }
                _ => panic!("unhandled path"),
            }
        }

        // Read output from command
        match current_command {
            None => panic!("No command found"),
            Some(Commands::Cd) => panic!("cd found"),
            Some(Commands::Ls) => println!("Recording ls output"),
        }

        if line.chars().collect::<Vec<char>>()[0].is_numeric() {
            // Add file sizes
            let first_part = line.split(" ").collect::<Vec<&str>>()[0];
            let size = u32::from_str(first_part).unwrap();
            println!("Found file of size {} in {}", size, current_directory);
            current_directory_file_size += size;
        } else {
            // Record directory
            let directory = line.split(" ").collect::<Vec<&str>>()[1].to_string();
            println!(
                "Recording directory {} for current dir {}",
                directory, current_directory
            );
            current_directory_directories.push(format!("{}/{}", current_directory, directory));
            println!("{:?}", current_directory_directories);
        }
    }

    // Record
    {
        if size_tree.contains_key(&current_directory) {
            *size_tree.get_mut(&current_directory).unwrap() += current_directory_file_size;
            directory_tree
                .get_mut(&current_directory)
                .unwrap()
                .append(&mut current_directory_directories);
        } else {
            size_tree.insert(
                current_directory.clone(),
                current_directory_file_size.clone(),
            );
            directory_tree.insert(
                current_directory.clone(),
                current_directory_directories.clone(),
            );
        }
    }

    let mut keys = vec![];
    for key in directory_tree.keys() {
        keys.push(key)
    }
    keys.sort();
    keys.reverse();

    let mut results = HashMap::new();
    for key in keys {
        let mut total_dir_size = 0;
        for nested_directory in directory_tree.get(key).unwrap() {
            println!("nested {}", nested_directory);
            total_dir_size += size_tree.get(nested_directory).unwrap();
        }
        total_dir_size += size_tree.get(key).unwrap();
        results.insert(key, total_dir_size);
    }

    let mut total = 0;
    for key in results.keys() {
        if &100000 >= results.get(key).unwrap() {
            total += results.get(key).unwrap();
        }
    }
    println!("{}", total);
}
