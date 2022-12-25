import { resolvePath } from "../filePaths.ts";
import { sum } from "../utils.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const input = file.trim().split("\n");

const all = input.flatMap((row) => [...row].map(Number));
const width = input[0].length;

class VisibilityMap {
  map: number[][] = [];

  constructor(width: number, height: number) {
    this.map = new Array(height).fill(0).map((_el) => new Array(width).fill(0));
  }

  updateColumn(newCol: number[], index: number) {
    this.map = this.map.map((row, d1) => {
      row[index] = newCol[d1] || row[index];
      return row;
    });
  }

  updateRow(newRow: number[], index: number) {
    this.map[index] = this.map[index].map((prev, idx) => newRow[idx] || prev);
  }

  sum() {
    return sum(this.map.flat());
  }
}

function createMask(line: string[]) {
  // Takes a line and returns a mask of visible trees from left to right
  let largest = 0;
  const mask = [];

  for (let col = 0; col < line.length; col++) {
    const treeSize = parseInt(line[col]);
    switch (true) {
      case treeSize > largest:
        mask.push(1);
        largest = treeSize;
        break;
      case col === 0:
        mask.push(1);
        break;
      default:
        mask.push(0);
        break;
    }
  }
  return mask;
}

function getColum(map: string[], column: number) {
  return new Array(map.length)
    .fill(null)
    .map((_el, index) => map[index].charAt(column));
}

function task1() {
  const visibilityMap = new VisibilityMap(input.length, input[0].length);
  const t1 = performance.now();
  for (let d1 = 0; d1 < input.length; d1++) {
    const row = [...input[d1]];
    const col = getColum(input, d1);
    visibilityMap.updateRow(createMask(row), d1);
    visibilityMap.updateRow(createMask(row.reverse()).reverse(), d1);
    visibilityMap.updateColumn(createMask(col), d1);
    visibilityMap.updateColumn(createMask(col.reverse()).reverse(), d1);
  }

  console.log(
    `Visible trees from the outside: ${visibilityMap.sum()} (in ${t1}ms)`
  );
}

// ======================== Task 2 ===========================

type Direction = "NORTH" | "EAST" | "SOUTH" | "WEST";

function getNext(index: number, direction: Direction) {
  switch (direction) {
    case "NORTH":
      return index - width;
    case "EAST":
      return index + 1;
    case "SOUTH":
      return index + width;
    case "WEST":
      return index - 1;
    default:
      return -1;
  }
}

function checkConstraints(
  direction: Direction,
  vantagePoint: number,
  nextIndex: number
) {
  if (typeof all[nextIndex] === "undefined") {
    return false;
  }

  if (["EAST", "WEST"].includes(direction)) {
    // If we're going left/right, check that we're still on the same row
    return Math.floor(nextIndex / width) === Math.floor(vantagePoint / width);
  }
  return true;
}

function navigate(
  vantagePoint: number,
  direction: Direction,
  nextIndex: number,
  viewingDistance = 0
): number {
  const nextTreeSize = all[nextIndex];
  const isValid = checkConstraints(direction, vantagePoint, nextIndex);

  if (!isValid) {
    return viewingDistance;
  }

  if (nextTreeSize === all[vantagePoint]) {
    // Next tree has same height as vantagepoint. Add 1 and return
    return viewingDistance + 1;
  }
  if (nextTreeSize < all[vantagePoint]) {
    const next = getNext(nextIndex, direction);
    return navigate(vantagePoint, direction, next, viewingDistance + 1);
  }
  return viewingDistance + 1;
}

function calculateViewingDistance(vantagePoint: number) {
  const north = navigate(vantagePoint, "NORTH", getNext(vantagePoint, "NORTH"));
  const east = navigate(vantagePoint, "EAST", getNext(vantagePoint, "EAST"));
  const south = navigate(vantagePoint, "SOUTH", getNext(vantagePoint, "SOUTH"));
  const west = navigate(vantagePoint, "WEST", getNext(vantagePoint, "WEST"));
  return north * east * south * west;
}

function task2() {
  const t1 = performance.now();
  const viewingDistanceMap = [...all].fill(0);

  for (let i = 0; i < viewingDistanceMap.length; i++) {
    const viewingDistance = calculateViewingDistance(i);
    viewingDistanceMap[i] = viewingDistance;
  }

  const highestScenicScore = viewingDistanceMap.sort((a, b) => b - a)[0];

  console.log(
    `The highest possible scenic score is: ${highestScenicScore} (in ${t1} ms)`
  );
}

task1();
task2();
