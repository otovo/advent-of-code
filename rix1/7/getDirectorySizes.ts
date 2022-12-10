type DirectoryRecord = Record<string, number>;

const removeTrailingSlash = (str: string) => str.slice(0, str.length - 1);

function updateDirectorySizes(
  rootPath: string,
  directories: DirectoryRecord,
  fileSize: number
) {
  const rootPathArray = removeTrailingSlash(rootPath).split("/");

  for (let i = rootPathArray.length; i > 0; i--) {
    // Note: We're going backwards
    const dir = rootPathArray.slice(0, i).join("/");
    directories[`${dir}/`] += fileSize;
  }
  return directories;
}

export function getDirectorySizes(lines: string[]): DirectoryRecord {
  const currentPath: string[] = [];
  let directories: DirectoryRecord = {};
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    switch (true) {
      case line === "$ ls":
      case line.startsWith("dir"):
        // Ignore these lines
        break;
      case line === "$ cd ..":
        currentPath.pop();
        break;
      case line.startsWith("$ cd"): {
        const dir = line.slice(5);
        if (dir === "/") {
          currentPath.push(dir);
        } else {
          currentPath.push(`${dir}/`);
        }
        const absolutePath = currentPath.join("");

        // Create and initialize key if it doesn't exist.
        // If we're jumping back into a folder (for some reason) just reuse the previous value
        const prev = directories[absolutePath] || 0;
        directories[absolutePath] = prev;
        break;
      }
      default: {
        // Because of the above conditions, we know this will be a file
        const [fileSize] = line.split(" ");
        const absolutePath = currentPath.join("");
        directories = updateDirectorySizes(
          absolutePath,
          directories,
          parseInt(fileSize)
        );
        break;
      }
    }
  }
  return directories;
}
