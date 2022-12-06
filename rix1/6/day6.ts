import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const input = file.trim();

const t = performance.now();

function runTask(consecutiveCharacters: number) {
  for (let i = 0; i < input.length; i++) {
    const arr = new Array(consecutiveCharacters)
      .fill("")
      .map((_el, index) => input[index + i]);

    const chars = [...new Set(arr)];

    if (chars.length === consecutiveCharacters) {
      console.log(
        `Found start-of-packet marker at <${i + chars.length}> (in ${t} ms)`
      );
      break;
    }
  }
}

runTask(4);
runTask(14);
