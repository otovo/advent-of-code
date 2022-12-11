import { resolvePath } from "../filePaths.ts";
import { sum } from "../utils.ts";
import { getDirectorySizes } from "./getDirectorySizes.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const input = file.trim().split("\n");

const numberFormat = new Intl.NumberFormat().format;

function runTask1() {
  const sizeThreshold = 100000;
  const t = performance.now();
  const directories = getDirectorySizes(input);

  const sizeArray = Object.keys(directories).map(
    (absolutePath) => directories[absolutePath]
  );
  const directoriesAboveThreshold = sizeArray.filter(
    (size) => size < sizeThreshold
  );
  const totalSize = sum(directoriesAboveThreshold);

  console.log(
    `Task 1: Total size of directories with a size below ${numberFormat(
      sizeThreshold
    )}: ${totalSize} (in ${t} ms)`
  );
}

function runTask2() {
  const t = performance.now();
  const directories = getDirectorySizes(input);

  const diskSpace = 70000000;
  const updateSize = 30000000;

  const unusedSpace = diskSpace - directories["/"];

  const needToDelete = updateSize - unusedSpace;

  const sizeArray = Object.keys(directories).map(
    (absolutePath) => directories[absolutePath]
  );
  const directoriesAboveThreshold = sizeArray.filter(
    (size) => size > needToDelete
  );
  const smallestAboveThreshold = directoriesAboveThreshold.sort(
    (a, b) => a - b
  )[0];

  console.log(
    `Task 2: Need to delete ${numberFormat(
      needToDelete
    )}. Will delete ${smallestAboveThreshold} (in ${t} ms)`
  );
}

runTask1();
runTask2();
