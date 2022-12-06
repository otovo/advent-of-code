import { resolvePath } from "../filePaths.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const input = file.trim();

const t = performance.now();
for (let i = 0; i < input.length; i++) {
  const chars = [
    ...new Set([input[i], input[i + 1], input[i + 2], input[i + 3]]),
  ];

  if (chars.length === 4) {
    console.log(
      `Found start-of-packet marker at <${i + chars.length}> (in ${t} ms)`
    );
    break;
  }
}
