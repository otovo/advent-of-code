import { splitOnElement } from "../utils.ts";

const input = await Deno.readTextFile("./input.txt");
const lines = input.split("\n");

const sortedElfCalories = splitOnElement(lines, "")
  .map((elf) => elf.reduce((prev, current) => prev + parseInt(current), 0))
  .sort((a, b) => b - a);

const a = sortedElfCalories.at(0);
const b = sortedElfCalories
  .slice(0, 3)
  .reduce((prev, current) => prev + current);

console.log(`Top dog carry ${a} calories`);
console.log(`3 top dogs carry ${b} calories`);
