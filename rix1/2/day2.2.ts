import { sum, ValueOf } from "../utils.ts";
import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

type Player1Keys = "A" | "B" | "C";
type Player2Keys = "X" | "Y" | "Z";

const hand = {
  ROCK: 1,
  PAPER: 2,
  SCISSOR: 3,
} as const;

const score = {
  LOOSE: 0,
  DRAW: 3,
  WIN: 6,
} as const;

const strategy = {
  DEFAULT: "DEFAULT",
  WIN: "WIN",
  LOOSE: "LOOSE",
  DRAW: "DRAW",
} as const;

const charToHandMap = {
  A: hand.ROCK,
  X: hand.ROCK,
  B: hand.PAPER,
  Y: hand.PAPER,
  C: hand.SCISSOR,
  Z: hand.SCISSOR,
} as const;

const charToStrategyMap = {
  X: strategy.LOOSE,
  Y: strategy.DRAW,
  Z: strategy.WIN,
} as const;

const inverseMap = {
  // Returns the loosing (inverse) hand
  [hand.ROCK]: hand.SCISSOR,
  [hand.PAPER]: hand.ROCK,
  [hand.SCISSOR]: hand.PAPER,
} as const;

function playRound(
  p1: Player1Keys,
  p2: Player2Keys,
  mode: ValueOf<typeof strategy> = strategy.DEFAULT
) {
  const hs1 = charToHandMap[p1];
  const hs2 = charToHandMap[p2];

  switch (true) {
    case hs1 === hs2:
    case mode === strategy.DRAW:
      return [hs1 + score.DRAW, hs1 + score.DRAW];
    case mode === strategy.WIN:
      return [hs1 + score.LOOSE, inverseMap[hs1] + score.WIN];
    case mode === strategy.LOOSE:
      return [hs1 + score.WIN, inverseMap[hs1] + score.LOOSE];
    case hs1 === hand.ROCK && hs2 === hand.SCISSOR:
    case hs1 === hand.PAPER && hs2 === hand.ROCK:
    case hs1 === hand.SCISSOR && hs2 === hand.PAPER:
      return [hs1 + score.WIN, hs2 + score.LOOSE];
    default:
      return [hs1 + score.LOOSE, hs2 + score.WIN];
  }
}

type Options = {
  useStrategyGuide: boolean;
};

function play(options?: Options) {
  const { useStrategyGuide = false } = options || {};
  const myScores = [];
  for (let i = 0; i < lines.length; i++) {
    const [elf, me] = lines[i].split(" ") as [Player1Keys, Player2Keys];

    if (useStrategyGuide) {
      myScores.push(playRound(elf, me, charToStrategyMap[me])[1]);
    } else {
      myScores.push(playRound(elf, me)[1]);
    }
  }
  return sum(myScores);
}

const t = performance.now();
const task1Score = play();
console.log(`Task 1: Your score is ${task1Score} (in ${t} ms)`);

const t2 = performance.now();
const task2Score = play({ useStrategyGuide: true });
console.log(
  `Task 2: Your score would be ${task2Score} using the strategy guide (in ${t2} ms)`
);
