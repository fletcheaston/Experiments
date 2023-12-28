# Day 5: Supply Stacks

## Part 1

### Prompt

The expedition can depart as soon as the final supplies have been unloaded from the ships.
Supplies are stored in stacks of marked **crates**, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a **giant cargo crane** capable of moving crates between stacks.
To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps.
After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her **which** crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

In this example, there are three stacks of crates.
Stack 1 contains two crates: crate `Z` is on the bottom, and crate `N` is on top.
Stack 2 contains three crates; from bottom to top, they are crates `M`, `C`, and `D`.
Finally, stack 3 contains a single crate, `P`.

Then, the rearrangement procedure is given.
In each step of the procedure, a quantity of crates is moved from one stack to a different stack.
In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```


In the second step, three crates are moved from stack 1 to stack 3.
Crates are moved **one at a time**, so the first crate to be moved (`D`) ends up below the second and third crates:

```
        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3 
```

Then, both crates are moved from stack 2 to stack 1.
Again, because crates are moved **one at a time**, crate `C` ends up below crate `M`:

```
        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3 
```

Finally, one crate is moved from stack 1 to stack 2:

```
        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3 
```

The Elves just need to know **which crate will end up on top of each stack**;
in this example, the top crates are `C` in stack 1, `M` in stack 2, and `Z` in stack 3, so you should combine these together and give the Elves the message **`CMZ`**.

**After the rearrangement procedure completes, what crate ends up on top of each stack?**

### Solution

For each line... 
1. Extract # of crates (count), stack to pull from (start), and stack to push to (end)
2. For each count, move a single crate
3. Iterate over stacks (in numerical order) and create a message from the top crate

```python
import re

from fastapi import APIRouter, Body

router = APIRouter()


STACK_EXAMPLE = {
    "1": ["N", "Z"],
    "2": ["D", "C", "M"],
    "3": ["P"],
}

DOCUMENT_EXAMPLE = [
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]


@router.post("/part-1")
async def year_2022_day_5_part_1(
    stacks: dict[str, list[str]] = Body(..., examples=[STACK_EXAMPLE]),
    document: list[str] = Body(..., examples=[DOCUMENT_EXAMPLE]),
) -> str:
    # Iterate over lines
    for line in document:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)

        count, start, end = match.groups()

        for _ in range(int(count)):
            # Remove from start
            crate = stacks[start].pop(0)
            stacks[end].insert(0, crate)

    # A few extra checks to preserve ordering
    stack_keys = [int(key) for key in stacks.keys()]
    stack_keys.sort()

    # Pull the top crate from each stack and create a message
    message = ""

    for key in stack_keys:
        crate = stacks[str(key)][0]
        message += crate

    return message
```

## Part 2

### Prompt

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a **CrateMover 9001**.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and **the ability to pick up and move multiple crates at once**.

Again considering the example above, the crates begin in the same configuration:

```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

Moving a single crate from stack 2 to stack 1 behaves the same as before:

```
[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 
```

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates **stay in the same order**, resulting in this new configuration:

```
        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
```

Next, as both crates are moved from stack 2 to stack 1, they **retain their order as well**:

```
        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
```

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate `C` that gets moved:

```
        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
```

In this example, the CrateMover 9001 has put the crates in a totally different order: **`MCD`**.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies.
**After the rearrangement procedure completes, what crate ends up on top of each stack?**

### Solution

For each line... 
1. Extract # of crates (count), stack to pull from (start), and stack to push to (end)
2. Move all crates from the start stack to the end stack (copy, clear, and add)
3. Iterate over stacks (in numerical order) and create a message from the top crate

```python
import re

from fastapi import APIRouter, Body

router = APIRouter()


STACK_EXAMPLE = {
    "1": ["N", "Z"],
    "2": ["D", "C", "M"],
    "3": ["P"],
}

DOCUMENT_EXAMPLE = [
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]


@router.post("/part-2")
async def year_2022_day_5_part_2(
    stacks: dict[str, list[str]] = Body(..., examples=[STACK_EXAMPLE]),
    document: list[str] = Body(..., examples=[DOCUMENT_EXAMPLE]),
) -> str:
    # Iterate over lines
    for line in document:
        match = re.search(r"move (\d+) from (\d+) to (\d+)", line)

        count, start, end = match.groups()

        # Pull off the top `count` crates
        crates = stacks[start][:int(count)]
        stacks[start] = stacks[start][int(count):]

        # Add crates to the new stack
        stacks[end] = crates + stacks[end]

    # A few extra checks to preserve ordering
    stack_keys = [int(key) for key in stacks.keys()]
    stack_keys.sort()

    # Pull the top crate from each stack and create a message
    message = ""

    for key in stack_keys:
        crate = stacks[str(key)][0]
        message += crate

    return message
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 5   | >24hr       | 159,128     | >24h        | 156,044     |

This is the first puzzle that made me think for a bit about what data structures I wanted to use.
It's also the first puzzle I used regex for 😒 but it was super useful for simple string parsing.

The puzzle itself was fairly straightforward, the logic to move crates between stacks only took a few minutes to create.
But I spent well over an hour on this puzzle 😖, with the vast majority of my time figuring out how to get data into my endpoint in a nice format.

What I **DID NOT** want to do was parse the initial crate positions from a file.
That would have been so much work, and I'm trying to get through these at a reasonable pace.
Instead, I settled on manually pulling out the initial crate positions and sending it to the endpoint as input data.

However, I really wanted to keep the same file input that I had used for many other endpoints.
Unfortunately, this meant I was stuck with using form data, and FastAPI's support for complex form data is a little lacking
(not through the fault of the framework, but due to ambiguous parsing rules).

I spent a ton of time trying to wrangle form data before giving up and settling on JSON.
This required very minor updates to the tests to pull out the lines from each file and include it in the request body,
and in retrospect, I should've done this from the start.

I'm fairly happy with the result, and the endpoint is something you can actually test (aka it has correct example data).
So I'll probably go back and update all other endpoints to take JSON instead of form data.
