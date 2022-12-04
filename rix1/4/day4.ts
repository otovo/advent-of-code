import { resolvePath } from "../filePaths.ts";
import { findIntersection } from "../utils.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

function createInputArray(line: string) {
  /**
   * Input: 2-4
   * Output: [2,3,4]
   **/
  const [a1, a2] = line.split("-").map(Number);
  return new Array(a2 + 1 - a1).fill("").map((_el, index) => a1 + index);
}

function task1() {
  // In how many assignment pairs does one range fully contain the other?
  let fullyContainedPairs = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const [a, b] = lines[i].split(",");
    const arrA = createInputArray(a);
    const arrB = createInputArray(b);

    const intersection = findIntersection(arrA, arrB);
    if ([arrA.length, arrB.length].includes(intersection.length)) {
      fullyContainedPairs += 1;
    }
  }
  console.log(
    `Task 1: Fully contained pairs ${fullyContainedPairs} (in ${t} ms)`
  );
}
task1();
