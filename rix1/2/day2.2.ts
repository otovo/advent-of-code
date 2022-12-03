import { z } from "https://deno.land/x/zod/mod.ts";
import { sum, ValueOf } from "../utils.ts";
import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

const p1Keys = z.enum(["A", "B", "C"]);
const p2Keys = z.enum(["X", "Y", "Z"]);

const hand = {
  ROCK: {
    name: "ROCK",
    score: 1,
    beats: "SCISSOR",
    weakTo: "PAPER",
  },
  PAPER: {
    name: "PAPER",
    score: 2,
    beats: "ROCK",
    weakTo: "SCISSOR",
  },
  SCISSOR: {
    name: "SCISSOR",
    score: 3,
    beats: "PAPER",
    weakTo: "ROCK",
  },
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

const charToStrategyMap = {
  X: strategy.LOOSE,
  Y: strategy.DRAW,
  Z: strategy.WIN,
} as const;

const charToHandMap = {
  A: hand.ROCK,
  X: hand.ROCK,
  B: hand.PAPER,
  Y: hand.PAPER,
  C: hand.SCISSOR,
  Z: hand.SCISSOR,
};

function playRound(
  h1: ValueOf<typeof hand>,
  h2: ValueOf<typeof hand>,
  mode: ValueOf<typeof strategy> = strategy.DEFAULT
) {
  switch (true) {
    case mode === strategy.DRAW:
      return [h1.score + score.DRAW, h1.score + score.DRAW];
    case mode === strategy.WIN:
      return [h1.score + score.LOOSE, hand[h1.weakTo].score + score.WIN];
    case mode === strategy.LOOSE:
      return [h1.score + score.WIN, hand[h1.beats].score + score.LOOSE];
    case h1.score === h2.score:
      return [h1.score + score.DRAW, h1.score + score.DRAW];
    case h1.beats === h2.name:
      return [h1.score + score.WIN, h2.score + score.LOOSE];
    default:
      return [h1.score + score.LOOSE, h2.score + score.WIN];
  }
}

type Options = {
  useStrategyGuide: boolean;
};

function play(options?: Options) {
  const { useStrategyGuide = false } = options || {};
  const myScores = [];
  for (let i = 0; i < lines.length; i++) {
    const [p1, p2] = lines[i].split(" ");

    const elfHand = charToHandMap[p1Keys.parse(p1)];
    const myHand = charToHandMap[p2Keys.parse(p2)];

    if (useStrategyGuide) {
      myScores.push(
        playRound(elfHand, myHand, charToStrategyMap[p2Keys.parse(p2)])[1]
      );
    } else {
      myScores.push(playRound(elfHand, myHand)[1]);
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
