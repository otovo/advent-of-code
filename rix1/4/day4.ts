import { resolvePath } from "../filePaths.ts";
import { findIntersection, ValueOf } from "../utils.ts";

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

const taskMode = {
  FULLY_OVERLAP: 1,
  PARTIAL_OVERLAP: 2,
};

function runTask(mode: ValueOf<typeof taskMode>) {
  // In how many assignment pairs does one range fully contain the other?
  let countOverlap = 0;
  const t = performance.now();
  for (let i = 0; i < lines.length; i++) {
    const [a, b] = lines[i].split(",");
    const arrA = createInputArray(a);
    const arrB = createInputArray(b);

    const intersection = findIntersection(arrA, arrB);
    if (mode === taskMode.FULLY_OVERLAP) {
      if ([arrA.length, arrB.length].includes(intersection.length)) {
        countOverlap += 1;
      }
    } else if (mode === taskMode.PARTIAL_OVERLAP) {
      if (intersection.length) {
        countOverlap += 1;
      }
    }
  }
  console.log(`Task ${mode}: Pairs overlapping ${countOverlap} (in ${t} ms)`);
}

runTask(taskMode.FULLY_OVERLAP);
runTask(taskMode.PARTIAL_OVERLAP);
