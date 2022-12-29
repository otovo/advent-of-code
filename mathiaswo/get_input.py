import argparse
import os
import textwrap
from datetime import datetime
from pathlib import Path

import black
import requests
from dotenv import dotenv_values

env_config = dotenv_values(".env")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", type=int, default=datetime.now().day)
    args = parser.parse_args()
    day: int = args.day

    assert 1 <= day <= 25, "Day must be between 1 and 25"

    input_response = requests.get(
        f"https://adventofcode.com/2022/day/{day}/input",
        cookies={"session": env_config["SESSION_COOKIE"]},
    )

    input_response.raise_for_status()

    out_dir = Path("days")
    os.makedirs(out_dir, exist_ok=True)

    input_dir = Path("inputs")
    os.makedirs(input_dir, exist_ok=True)

    input_file = input_dir / f"input_{day}.txt"
    input_file.write_text(input_response.text)

    main_file = out_dir / f"day_{day}.py"

    if not main_file.exists():
        main_file.write_text(
            textwrap.dedent(
                f"""
                from pathlib import Path

                def main(input_string: str):
                    print(input_string)


                if __name__ == "__main__":
                    input_path = Path(__file__).parents[1] / "inputs" / "input_{day}.txt"
                    with open(input_path) as f:
                        input_string = f.read().strip()
                    main(input_string)
                """
            )
        )
        black.main(["-q", str(main_file)])
