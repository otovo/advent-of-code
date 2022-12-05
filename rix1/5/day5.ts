import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trimEnd().split("\n");

const divider = "";
const dividerIndex = lines.indexOf(divider);

function createMap() {
  const originalMap = lines.slice(0, dividerIndex - 1);
  const lineLength = originalMap[0].length;

  const preparedMap = originalMap.reverse().join("");

  const columnMap = [];
  for (let i = 0; i < preparedMap.length; i++) {
    const char = preparedMap[i];

    if (/[A-Z]/.test(char)) {
      const column: string[] = columnMap[i % lineLength] || [];
      column.push(char);
      columnMap[i % lineLength] = column;
    }
  }
  // Because we use direct index assignments above, we need to filter out empty
  // values before returning: [<empty>,<empty>,[A,B,C],<empty>] -> [[A,B,C]]
  return columnMap.filter(Boolean);
}

function createInstructions(): number[][] {
  const textInstructions = lines.slice(dividerIndex + 1);
  const rawInstructions = [];
  for (let i = 0; i < textInstructions.length; i++) {
    const instructionLine = textInstructions[i];
    const instructions = instructionLine.match(/\d{1,2}/g) || [];
    if (instructions) {
      rawInstructions.push(instructions.map((el) => parseInt(el)));
    } else {
      throw new Error(
        `Could not create instructions. Error occured when parsing line <${instructionLine}>`
      );
    }
  }
  return rawInstructions;
}

function task1() {
  const instructions = createInstructions();
  const map = createMap();
  const t = performance.now();
  for (let i = 0; i < instructions.length; i++) {
    const [move, from, to] = instructions[i];
    console.log(move, from, to);

    const characters = map[from - 1].splice(map[from - 1].length - move, move);
    map[to - 1].push(...characters.reverse());
  }
  const str = map.map((column) => column.at(-1));
  console.log(
    `Task 1: Crates that end up on top: <${str.join("")}> (in ${t} ms)`
  );
}

task1();
