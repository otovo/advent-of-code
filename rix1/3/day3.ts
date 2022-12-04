import { resolvePath } from "../filePaths.ts";
import { sum } from "../utils.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

function getCharScore(char: string) {
  const charCode = char.charCodeAt(0);
  if (charCode > 96) {
    return charCode - 96;
  }
  return charCode - 38;
}

function findIntersection(l: string[], r: string[]) {
  const left = new Set(l);
  const right = new Set(r);
  return [...left].filter((char) => [...right].includes(char));
}

function task1() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const split = line.length / 2;
    const duplicates = findIntersection(
      [...line.slice(0, split)],
      [...line.slice(split)]
    );
    total += sum(duplicates.map((char) => getCharScore(char)));
  }
  console.log(`Task 1: Sum of priorities ${total} (in ${t} ms)`);
}

function task2() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i += 3) {
    const duplicates = findIntersection(
      findIntersection([...lines[i]], [...lines[i + 1]]),
      [...lines[i + 2]]
    );
    total += getCharScore(duplicates[0]);
  }
  console.log(`Task 2: Sum of priorities ${total} (in ${t} ms)`);
}

task1();
task2();
