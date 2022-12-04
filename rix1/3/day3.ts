import { resolvePath } from "../filePaths.ts";
import { findIntersection, sum } from "../utils.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

function getCharScore(char: string) {
  const charCode = char.charCodeAt(0);
  if (charCode > 96) {
    return charCode - 96;
  }
  return charCode - 38;
}

function task1() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const split = line.length / 2;
    const intersection = findIntersection(
      [...line.slice(0, split)],
      [...line.slice(split)]
    );
    total += sum(intersection.map((char) => getCharScore(String(char))));
  }
  console.log(`Task 1: Sum of priorities ${total} (in ${t} ms)`);
}

function task2() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i += 3) {
    const intersection = findIntersection(
      findIntersection([...lines[i]], [...lines[i + 1]]),
      [...lines[i + 2]]
    );
    total += getCharScore(String(intersection[0]));
  }
  console.log(`Task 2: Sum of priorities ${total} (in ${t} ms)`);
}

task1();
task2();
