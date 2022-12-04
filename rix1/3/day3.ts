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

function run() {
  let total = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const split = line.length / 2;
    const duplicates = findDuplicates(line.slice(0, split), line.slice(split));
    total += sum(duplicates.map((char) => getCharScore(char)));
  }
  console.log(`Sum of priorities ${total} (in ${t} ms)`);
}

run();
