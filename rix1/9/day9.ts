import { z } from "https://deno.land/x/zod/mod.ts";
import { resolvePath } from "../filePaths.ts";
const file = await Deno.readTextFile(resolvePath("./input.test.txt"));
const input = file.trim().split("\n");

const Direction = z.enum(["U", "D", "L", "R"]);
const Moves = z.number();
// type Direction = "UP" | "DOWN" | "LEFT" | "RIGHT"
type Pos = [number, number];

function moveHead(pos: Pos, direction: z.infer<typeof Direction>): Pos {
  switch (direction[0]) {
    case "U":
      return [pos[0], pos[1] - 1];
    case "D":
      return [pos[0], pos[1] + 1];
    case "L":
      return [pos[0] - 1, pos[1]];
    case "R":
      return [pos[0] + 1, pos[1]];
    default:
      throw new Error(
        `Cannot move head, <${direction[0]}> is not a supported direction.`
      );
  }
}

function moveTail(tail: Pos, head: Pos) {
  // [0,0] -> [0,1] dx:0, dy: 1
  // [0,0] -> [1,0] dx:1, dy:0
  // [1,1] -> [0,1] dx: -1, dy:0
  // [3,2] -> [4,2]
  // it should never be the same as head (cant catch up)
  const dx = head[0] - tail[0];
  const dy = head[1] - tail[1];
  const newPos: Pos = [tail[0] + dx, tail[1] + dy];
  if (createKey(newPos) === createKey(tail)) {
    return tail;
  }
  return newPos;
}

function parseInstruction(line: string) {
  const [d, m] = line.split(" ");
  return [Direction.parse(d), Moves.parse(parseInt(m))] as const;
}

function createKey(pos: Pos) {
  return `${pos[0]}:${pos[1]}`;
}

function task1() {
  const t1 = performance.now();
  const headTrail = new Set();
  const tailTrail = new Set();
  for (let i = 0; i < input.length; i++) {
    let head = [0, 0] as Pos;
    let tail = [0, 0] as Pos;
    const line = input[i];
    const [direction, moves] = parseInstruction(line);
    for (let step = 0; step < moves; step++) {
      head = moveHead(head, direction);
      headTrail.add(createKey(head));
      tail = moveTail(tail, head);
      tailTrail.add(createKey(tail));
    }
  }
  console.log([...headTrail], [...tailTrail].length);

  console.log(`Done (in ${t1} ms)`);
}

task1();
