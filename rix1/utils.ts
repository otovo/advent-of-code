export function splitOnElement(arr: string[], separator: string) {
  const result: string[][] = [[]];
  for (let index = 0; index < arr.length; index++) {
    const el = arr[index];
    if (el === separator) {
      result.push([]);
    } else {
      result.at(-1)?.push(el);
    }
  }
  return result;
}

export function sum(arr: string[] | number[]) {
  return arr.map(Number).reduce((prev, next) => prev + next, 0);
}

type StringOrNum = string | number;
export function findIntersection(l: StringOrNum[], r: StringOrNum[]) {
  const left = new Set(l);
  const right = new Set(r);
  return [...left].filter((char) => [...right].includes(char));
}

export type ValueOf<T> = T[keyof T];
