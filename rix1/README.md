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
but this is not (yet) a primitive feature in JavaScript... So I read a bit
around and learned from [1](https://kyleshevlin.com/pattern-matching) that I can
actually use `switch(true)` statements to _sorta_ mimic pattern matching. The
article also reminded me about
["Katas"](https://en.wikipedia.org/wiki/Kata#:~:text=Kata%20is%20a%20term%20used,memory%20and%20practise%20their%20craft.),
a concept I've [completely forgotten existed](https://kata-log.rocks/).

I'm quite happy with how my `playRound()` function turned out, as it was super
easy to extend the code to support the new constraints in task 2.

The only thing I want to improve is to validate the input. Right now I'm just
casting the input to get the correct type at the boundary, but ideally this
should be validated at runtime as well.
