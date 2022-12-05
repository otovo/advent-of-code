## Rix1's solutions 👋

I'm currently solving these using Deno (TypeScript).

### How to run

1. Install [Deno](https://deno.land/manual@v1.28.3/getting_started/installation) 🦕
2. Run a solution with `cd <DAY/> && deno run --allow-read dayX.ts`. The
   `allow-read` flag will allow Deno to read files from your file system.

### Captains log 📝

#### Day 1

**🎉 TIL:** about the new `Array.at(integer)` syntax! It's similar to the Python array lookup, supporting negative numbers. No more `arr[arr.length - 1]`, this can now be done with `arr.at(-1)` 🎉

#### Day 2

My immediate apporach started with typing out all the characters and their
meaning. This quickly became quite tedious and I fell into several pits that I
had to backtrack my way out of.

After 3-4 such pits, my patience was running out, so I decided to just type out
the different combinations in lookup objects and attach "my" score as value. See solution in `day2.1.ts`.

This solved the problem, but felt very hard coded. So on day 3 I picked it up
again and gave it another go in `day2.2.ts`.

It's obviously more code, and to be frank, I'm not sure if it's more readable –
at least not on first glance. It is more exstensible though.

**🎉 TIL:** During my second attempt, I really wanted to use pattern matching –
but this is not ([yet](https://github.com/tc39/proposal-pattern-matching)) a primitive feature in JavaScript... So I read a bit
around and learned from [1](https://kyleshevlin.com/pattern-matching) that I can
actually use `switch(true)` statements to _sorta_ mimic pattern matching. The
article also reminded me about
["Katas"](https://en.wikipedia.org/wiki/Kata#:~:text=Kata%20is%20a%20term%20used,memory%20and%20practise%20their%20craft.),
a concept I've [completely forgotten existed](https://kata-log.rocks/).

I'm happy with how my `playRound()` function turned out. The `switch(true)`
statement in combination with the simple tree structure (embedding the game
rules in the data structure) made it super easy to extend the code to support
the new constraints in task 2.

~~The only thing I want to improve is to validate the input. Right now I'm just
casting the input to get the correct type at the boundary, but ideally this
should be validated at runtime as well.~~ Edit: I just added
[Zod](https://zod.dev/) for static + runtime type checking.

#### Day 3

Key learning today was to create a `input.test.txt` file that I use to validate and debug my code. I think I'll continue doing that.

I think the only pitfall I had to backtrack from was that I started out using `Map()` instead of `Set()`. Because I wans't sure if I later would need both a reference to the original character and it's position, I tried to store both in a data structure looking something like this

```js
Map { [ "v" ] => [ [1, 4], [12] ] }
```

where each sub-array represented the left and right side of the string along with the position of the character. However, I quickly realized how cumbersome this was to work with. So I took a bet that the position wouldn't matter (the character reference could easily be transformed back from the "priority value" if I needed that.

#### Day 4

Fun to see [leverage](https://www.amazon.com/Effective-Engineer-Engineering-Disproportionate-Meaningful/dp/0996128107) in practice! Since I created the `findIntersection()` utility for day 3, I mostly had to think of how to transform the input to the right format for task 1. When task 2 came around, I already had the answer, so I meerly needed to add a condition to count `PARTIAL_OVERLAP` in addition to `FULLY_OVERLAP`.

<img src="https://i.kym-cdn.com/entries/icons/original/000/000/142/feelsgoodman.png" alt="Feelsgoodman" width="120px">

#### Day 5

Not surprisingly, most of today was about parsing and massaging the input to a
format that made sense. But all in all, I'm pretty happy with how this turned
out. After that was done, doing the actual transformations was meerly 17 lines
of code.

If there are any TIL's today, I guess it would be that (again) it pays off to
have a nice datastructure. Solving task 2 was done on a single line, just
avoiding reversing the array before moving it to the new column.
