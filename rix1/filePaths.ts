import * as path from "https://deno.land/std@0.102.0/path/mod.ts";
const mainModuleDir = path.dirname(path.fromFileUrl(Deno.mainModule));

export function resolvePath(filePath: string) {
  Deno.chdir(mainModuleDir);
  return path.resolve(filePath);
}
