#!/usr/bin/env python3

import os
from datetime import datetime
from pathlib import Path

import click
import requests
from dotenv import load_dotenv

day = datetime.now().day


@click.command()
@click.option("--day", default=day, type=int, help="Which day to get")
def get(day):
    root = f"https://adventofcode.com/2022/day/{day}"
    session = os.getenv("AOC_SESSION")
    resp = requests.get(root + "/input", cookies={"session": session})
    resp.raise_for_status()

    out_dir = Path("input")
    if not out_dir.is_dir():
        out_dir.mkdir()

    out_file = out_dir / f"/day_{day:02d}.txt"
    out_file.write_text(resp.text)

    test_file = out_dir / f"day_{day:02d}-test.txt"
    if not test_file.is_file():
        test_file.touch()

    click.echo(
        f"Fetching day {day} complete.\nLink to challenge:\n\t{root}\nInput written to:\n\t{out_file}"
    )


if __name__ == "__main__":
    load_dotenv()
    get()
