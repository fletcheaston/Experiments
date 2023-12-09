# Day 8: Haunted Wasteland

## Part 1

### Prompt

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching.
When you turn to warn the Elf, she disappears before your eyes!
To be fair, she had just finished warning you about **ghosts** a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert.
At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of **network** of labeled nodes.

It seems like you're meant to use the **left/right** instructions to **navigate the network**.
Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: `AAA` and `ZZZ`.
You feel like `AAA` is where you are now, and you have to follow the left/right instructions until you reach `ZZZ`.

This format defines each **node** of the network individually.
For example:

```
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
```

Starting with AAA, you need to **look up the next element** based on the next left/right instruction in your input.
In this example, start with `AAA` and go **right** (`R`) by choosing the right element of `AAA`, **`CCC`**.
Then, `L` means to choose the **left** element of `CCC`, **`ZZZ`**.
By following the left/right instructions, you reach `ZZZ` in **`2`** steps.

Of course, you might not find `ZZZ` right away.
If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: `RL` really means `RLRLRLRLRLRLRLRL...` and so on.
For example, here is a situation that takes **`6`** steps to reach `ZZZ`:

```
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
```

Starting at `AAA`, follow the left/right instructions.
**How many steps are required to reach ZZZ?**

### Solution

Brute-force solution of walking through the steps.

```python
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 8: Haunted Wasteland"])


INSTRUCTIONS_EXAMPLE = ""

DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_8_part_1(
    instructions: str = Body(
        ...,
        embed=True,
        examples=[INSTRUCTIONS_EXAMPLE],
    ),
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    steps = 0
    current_step = "AAA"

    maps: dict[str, tuple[str, str]] = {}

    # Iterate over lines
    for line in document:
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

    while current_step != "ZZZ":
        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            current_step = maps[current_step][0]
        elif instruction == "R":
            current_step = maps[current_step][1]
        else:
            raise AssertionError

        steps += 1

    return steps
```

## Part 2

### Prompt

The sandstorm is upon you and you aren't any closer to escaping the wasteland.
You had the camel follow the instructions, but you've barely left your starting position.
It's going to take **significantly more steps** to escape!

What if the map isn't for people - what if the map is for **ghosts**?
Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in `A` is equal to the number ending in `Z`!
If you were a ghost, you'd probably just **start at every node that ends with `A`** and follow all of the paths at the same time until they all simultaneously end up at nodes that end with `Z`.

For example:

```
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
```

Here, there are two starting nodes, `11A` and `22A` (because they both end with `A`).
As you follow each left/right instruction, use that instruction to **simultaneously** navigate away from both nodes you're currently on.
Repeat this process until **all** of the nodes you're currently on end with `Z`.
(If only some of the nodes you're on end with `Z`, they act like any other node and you continue as normal.)
In this example, you would proceed as follows:

- Step 0: You are at `11A` and `22A`.
- Step 1: You choose all of the **left** paths, leading you to `11B` and `22B`.
- Step 2: You choose all of the **right** paths, leading you to **`11Z`** and `22C`.
- Step 3: You choose all of the **left** paths, leading you to `11B` and **`22Z`**.
- Step 4: You choose all of the **right** paths, leading you to **`11Z`** and `22B`.
- Step 5: You choose all of the **left** paths, leading you to `11B` and `22C`.
- Step 6: You choose all of the **right** paths, leading you to **`11Z`** and **`22Z`**.

So, in this example, you end up entirely on nodes that end in `Z` after **`6`** steps.

Simultaneously start on every node that ends with `A`.
**How many steps does it take before you're only on nodes that end with Z?**

### Solution

Instead of a brute-force solution, I counted steps per cycle for each path.
I could then take the least common multiple of these steps per cycle to get the final number of steps required for all these to sync up on the end positions.

```python
import math

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 8: Haunted Wasteland"])


INSTRUCTIONS_EXAMPLE = ""

DOCUMENT_EXAMPLE = []


@router.post("/part-2")
async def year_2023_day_8_part_2(
    instructions: str = Body(
        ...,
        embed=True,
        examples=[INSTRUCTIONS_EXAMPLE],
    ),
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    steps: list[str] = []
    maps: dict[str, tuple[str, str]] = {}

    # Iterate over lines
    for index, line in enumerate(document):
        start, rest = line.split(" = ")
        left, right = rest.replace("(", "").replace(")", "").split(", ")

        maps[start] = (left, right)

        if start.endswith("A"):
            steps.append(start)

    steps_index = 0
    cycles = []

    while True:
        for index, previous_step in enumerate(steps):
            current_step = maps[previous_step]
            instruction = instructions[steps_index % len(instructions)]

            if instruction == "L":
                next_step = current_step[0]
            elif instruction == "R":
                next_step = current_step[1]
            else:
                raise AssertionError

            if next_step.endswith("Z"):
                cycles.append(steps_index + 1)

            steps[index] = next_step

        if len(cycles) == len(steps):
            break

        steps_index += 1

    return math.lcm(*cycles)
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 8   | 00:09:41    | 2,164       | 02:16:39    | 9,554       |

Part 1 was very easy and the kind of problem I really enjoy!

I first tried the brute-force solution on Part 2.
Once it didn't complete within 30 seconds, I knew I'd need to implement cycle counting to get a reasonably-fast answer, but I left the script running anyway just in case it happened to complete eventually.
That script didn't complete with >2 hours of runtime 😬.

Cycle counting was simple *in theory*, but *in practice*, I had a lot of trouble figuring out how to do it properly.
I did use custom test cases like I did in [Day 7](day-7.md), but even then, it took a really long time to figure out a correct implementation 😖.
