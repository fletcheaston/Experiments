# Day 5: Organize Santa's List

Prompt by [Dimitri Mitropoulos](https://github.com/dimitropoulos) of [MiTS](https://www.youtube.com/@MichiganTypeScript).

## Prompt

*[The elves walk into work early on the morning of December 5th. A sign that reads "we're all about passion, not just paychecks" hangs above the entrance to the factory floor.]*

It's been a tough year for Santa's workshop.
The elves are a little behind schedule on getting Santa his list.
Santa *reallly really* likes to see the full list of names far in advance of Christmas Eve when he makes his deliveries.

Normally the elves get lists like this

```typescript
const badList = ["Tommy", "Trash", "Queen Blattaria", /* ... many more ... */];
const goodList = ["Jon", "David", "Captain Spectacular", /* ... many more ... */];
```

And they copy-pasta all the values into a TypeScript type to provide to Santa like this

```typescript
type SantasList = [
  "Tommy", "Trash", "Queen Blattaria", /* ... many more ... */
  "Jon", "David", "Captain Spectacular", /* ... many more ... */
];
```

But there's a problem.. There's one elf on the team, Frymagen, that constantly reminds the others how incredible his Vim skills are.
So he has always done it in years past.
However this year, Frymagen got one of those MacBook Pros without the escape key and his Vim speed is drastically reduced.
We need to find a better way to get Santa his list.

Let's implement `SantasList` such that it can be passed the types for the `badList` and `goodList` and it will return a TypeScript tuple with the values of both lists combined.

## Solution

```typescript
type SantasList<Bads extends Readonly<Array<any>>, Goods extends Readonly<Array<any>>> = [
	...Bads, ...Goods
];
```

## Tests

```typescript
import { Expect, Equal } from 'type-testing';

const bads = ['tommy', 'trash'] as const;
const goods = ['bash', 'tru'] as const;

type test_0_actual = SantasList<typeof bads, typeof goods>;
//   ^?
type test_0_expected = ['tommy', 'trash', 'bash', 'tru'];
type test_0 = Expect<Equal<test_0_actual, test_0_expected>>;

type test_1_actual = SantasList<[], []>;
//   ^?
type test_1_expected = [];
type test_1 = Expect<Equal<test_1_actual, test_1_expected>>;

type test_2_actual = SantasList<[], ['trash']>;
//   ^?
type test_2_expected = ['trash'];
type test_2 = Expect<Equal<test_2_actual, test_2_expected>>;

type test_3_actual = SantasList<['john'], ['ashley', 'elliot', 'ziltoid']>;
//   ^?
type test_3_expected = ['john', 'ashley', 'elliot', 'ziltoid'];
type test_3 = Expect<Equal<test_3_actual, test_3_expected>>;

type test_4_actual = SantasList<['1', 2, '3'], [false, boolean, '4', ['nested']]>;
//   ^?
type test_4_expected = ['1', 2, '3', false, boolean, '4', ['nested']];
type test_4 = Expect<Equal<test_4_actual, test_4_expected>>;

// @ts-expect-error
type error_0 = SantasList<null, undefined>;
```

## Recap

The first (slight) challenge for me, I almost never use the [Readonly](https://www.typescriptlang.org/docs/handbook/utility-types.html#readonlytype) type so this was a fun one 😁!
