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

function findDuplicates(l: string, r: string) {
  const left = new Set(...[l]);
  const right = new Set(...[r]);
  return [...left].filter((char) => [...right].includes(char));
}

function task1() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const split = line.length / 2;
    const duplicates = findDuplicates(line.slice(0, split), line.slice(split));
    total += sum(duplicates.map((char) => getCharScore(char)));
  }
  console.log(`Task 1: Sum of priorities ${total} (in ${t} ms)`);
}

function task2() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i += 3) {
    const elf1 = new Set(...[lines[i]]);
    const elf2 = new Set(...[lines[i + 1]]);
    const elf3 = new Set(...[lines[i + 2]]);
    const duplicates = [...elf1]
      .filter((char) => [...elf2].includes(char))
      .filter((char) => [...elf3].includes(char));
    total += getCharScore(duplicates[0]);
  }
  console.log(`Task 2: Sum of priorities ${total} (in ${t} ms)`);
}

task1();
task2();
