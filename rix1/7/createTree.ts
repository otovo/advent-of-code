import { sum } from "../utils.ts";

export type File = {
  name: string;
  size: number;
};
export type Directory = {
  files: File[];
  subDirectories: string[];
};

export type Tree = Record<string, Directory>;
export type TreeWithSize = Record<string, Directory & { totalSize: number }>;

const cdRegex = /\$\scd\s([\/a-z]+)/;

function calculateSize(dir: Directory, tree: Tree) {
  let size = sum(dir.files.map((file) => file.size));

  if (dir.subDirectories.length) {
    size += sum(
      dir.subDirectories.map((subDir) => {
        return calculateSize(tree[subDir], tree);
      })
    );
  }
  return size;
}

function annotateSize(tree: Tree) {
  return Object.keys(tree).reduce((prev, key) => {
    const dir = tree[key];

    const totalSize = calculateSize(dir, tree);
    return { ...prev, [key]: { ...dir, totalSize: totalSize } };
  }, {});
}

export function createTree(input: string[]): [TreeWithSize, string[]] {
  let level = 0;
  let count = 0;
  let errCount = 0;
  const nodes: Record<string, Directory> = {};

  for (let i = 0; i < input.length; i++) {
    const line = input[i];

    switch (true) {
      case line === "$ ls":
        break;
      case line === "$ cd ..": {
        level = level - 1;
        break;
      }
      case cdRegex.test(line): {
        const dir = line.match(cdRegex)?.[1] || "";
        count++;

        nodes[`${dir}:${level}`] = {
          files: [],
          subDirectories: [],
        };
        level++;
        break;
      }
      case line.startsWith("dir"): {
        const dir = line.slice(4);
        const parentKey = Object.keys(nodes).at(-1);
        if (parentKey) {
          const subDirectories = nodes[parentKey].subDirectories;
          subDirectories.push(`${dir}:${level}`);
        }
        break;
      }
      default: {
        // It's a file
        const parentKey = Object.keys(nodes).at(-1);
        if (parentKey) {
          const files = nodes[parentKey]?.files || [];
          const [fileSize, fileName] = line.split(" ");
          files.push({ name: fileName, size: parseInt(fileSize) });
        }
        break;
      }
    }
  }
  console.log(nodes);

  const directoryNames = Object.keys(nodes);
  console.log(
    `done. created a total of ${count} directories, ${errCount} errors and we got ${directoryNames.length} dirs created.`
  );
  return [annotateSize(nodes), directoryNames];
}
