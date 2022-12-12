import { resolvePath } from "../filePaths.ts";
import { sum } from "../utils.ts";

const file = await Deno.readTextFile(resolvePath("./input.txt"));
const input = file.trim().split("\n");
