import { sum, ValueOf } from "../utils.ts";
import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const lines = file.trim().split("\n");

type Player1Keys = "A" | "B" | "C";
type Player2Keys = "X" | "Y" | "Z";

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

function getHandFromChar(char: Player1Keys | Player2Keys) {
  switch (char) {
    case "A":
    case "X":
      return hand.ROCK;
    case "B":
    case "Y":
      return hand.PAPER;
    case "C":
    case "Z":
      return hand.SCISSOR;
    default:
      throw new Error(`Unknown char <${char}>`);
  }
}

function playRound(
  p1: Player1Keys,
  p2: Player2Keys,
  mode: ValueOf<typeof strategy> = strategy.DEFAULT
) {
  const h1 = getHandFromChar(p1);
  const h2 = getHandFromChar(p2);

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
