import { splitOnElement, sum } from "../utils.ts";

const input = await Deno.readTextFile("./input.txt");
const lines = input.split("\n");

const sortedElfCalories = splitOnElement(lines, "")
  .map(sum)
  .sort((a, b) => b - a);

const a = sortedElfCalories.at(0);
const b = sum(sortedElfCalories.slice(0, 3));

console.log(`Top dog carry ${a} calories`);
console.log(`3 top dogs carry ${b} calories`);
