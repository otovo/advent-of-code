import { resolvePath } from "../filePaths.ts";
const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

const score = {
  WIN: 6,
  DRAW: 3,
  LOOSE: 0,
} as const;

const handPoints = {
  ROCK: 1,
  PAPER: 2,
  SCISSOR: 3,
} as const;

const scoreMap = {
  "A X": score.DRAW + handPoints.ROCK,
  "A Y": score.WIN + handPoints.PAPER,
  "A Z": score.LOOSE + handPoints.SCISSOR,
  "B X": score.LOOSE + handPoints.ROCK,
  "B Y": score.DRAW + handPoints.PAPER,
  "B Z": score.WIN + handPoints.SCISSOR,
  "C X": score.WIN + handPoints.ROCK,
  "C Y": score.LOOSE + handPoints.PAPER,
  "C Z": score.DRAW + handPoints.SCISSOR,
} as const;

const scoreMap2 = {
  "A X": score.LOOSE + handPoints.SCISSOR,
  "A Y": score.DRAW + handPoints.ROCK,
  "A Z": score.WIN + handPoints.PAPER,
  "B X": score.LOOSE + handPoints.ROCK,
  "B Y": score.DRAW + handPoints.PAPER,
  "B Z": score.WIN + handPoints.SCISSOR,
  "C X": score.LOOSE + handPoints.PAPER,
  "C Y": score.DRAW + handPoints.SCISSOR,
  "C Z": score.WIN + handPoints.ROCK,
} as const;

type Round = keyof typeof scoreMap;

function play(map: typeof scoreMap | typeof scoreMap2) {
  let totalScore = 0;

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index] as Round;
    totalScore += map[line];
  }
  return totalScore;
}

const t = performance.now();
const task1Score = play(scoreMap);
console.log(`Task 1: Your score is ${task1Score} in ${t} ms`);

const t2 = performance.now();
const task2Score = play(scoreMap2);
console.log(
  `Task 2: Your score would be ${task2Score} using the strategy guide in ${t2} ms`
);
