# Day 17: Clumsy Crucible

## Part 1

### Prompt

The lava starts flowing rapidly once the Lava Production Facility is operational.
As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new **lavafall**.
Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand.
Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible **from the lava pool to the machine parts factory**.
To do this, you need to minimize **heat loss** while choosing a route that doesn't require the crucible to go in a **straight line** for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

For example:

```
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
```

Each city block is marked by a single digit that represents the **amount of heat loss if the crucible enters that block**.
The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block.
(Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move **at most three blocks** in a single direction before it must turn 90 degrees left or right.
The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to **minimize heat loss** is this path:

```
2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
```

This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only **`102`**.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, **what is the least heat loss it can incur?**

### Solution

[Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm), but limit the possible steps at each junction based on the "history" of steps (aka limit the maximum number of steps in a given direction).

We prefer steps that produce a lower-cost path, with steps moving towards the goal as a tiebreaker.

This uses a [heap queue](https://docs.python.org/3/library/heapq.html) to iterate over steps along the path.

```python
from dataclasses import dataclass, field
from heapq import heappop, heappush

from fastapi import APIRouter, Body

router = APIRouter()


DOCUMENT_EXAMPLE = [
    "2413432311323",
    "3215453535623",
    "3255245654254",
    "3446585845452",
    "4546657867536",
    "1438598798454",
    "4457876987766",
    "3637877979653",
    "4654967986887",
    "4564679986453",
    "1224686865563",
    "2546548887735",
    "4322674655533",
]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __lt__(self, other: "Coordinate") -> bool:
        if self.x != other.x:
            return self.x < other.x

        return self.y < other.y


OFFSETS: list[Coordinate] = [
    Coordinate(x=0, y=-1),  # Up
    Coordinate(x=0, y=1),  # Down
    Coordinate(x=1, y=0),  # Right
    Coordinate(x=-1, y=0),  # Left
]


def do_180(coordinate: Coordinate) -> Coordinate:
    return Coordinate(x=-coordinate.x, y=-coordinate.y)


Edge = tuple[Coordinate, Coordinate | None, int]


@dataclass
class Grid:
    grid: dict[Coordinate, int]

    minimum_distance: int
    maximum_distance: int

    edges: dict[Edge, list[Edge]] = field(default_factory=dict)

    max_x: int = 0
    max_y: int = 0

    def add_coordinate(self, coordinate: Coordinate, cost: int) -> None:
        self.max_x = max(self.max_x, coordinate.x + 1)
        self.max_y = max(self.max_y, coordinate.y + 1)
        self.grid[coordinate] = cost

    def run(self) -> int:
        start = (Coordinate(x=0, y=0), None, 0)

        # Build up our cost path
        queue: list[tuple[int, Edge]] = [(0, start)]
        checked: set[Edge] = {start}

        while True:
            current_cost, (point, backwards_offset, distance) = heappop(queue)

            if (
                self.minimum_distance <= distance <= self.maximum_distance
                and point.x == self.max_x - 1
                and point.y == self.max_y - 1
            ):
                return current_cost

            edges: list[Edge] = []

            if backwards_offset is None:
                for next_offset in OFFSETS:
                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            elif distance < self.minimum_distance:
                # Gotta keep moving in the same direction
                next_point = Coordinate(
                    x=point.x + backwards_offset.x,
                    y=point.y + backwards_offset.y,
                )

                if next_point not in self.grid:
                    continue

                edges.append((next_point, backwards_offset, distance + 1))

            elif distance < self.maximum_distance:
                # Can turn now
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    if next_offset == backwards_offset:
                        edges.append((next_point, next_offset, distance + 1))

                    else:
                        edges.append((next_point, next_offset, 1))

            else:
                # Over the maximum, gotta turn
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    if next_offset == backwards_offset:
                        # No going straight
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            for edge in edges:
                if edge in checked:
                    continue

                checked.add(edge)
                current_point = edge[0]

                next_cost = current_cost + self.grid[current_point]
                heappush(
                    queue,
                    (next_cost, edge),
                )


@router.post("/part-1")
async def year_2023_day_17_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid(
        grid={},
        minimum_distance=0,
        maximum_distance=3,
    )

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(Coordinate(x=x_index, y=y_index), cost=int(character))

    return grid.run()
```

## Part 2

### Prompt

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory.
Instead, the Elves are going to upgrade to **ultra crucibles**.

Ultra crucibles are even more difficult to steer than normal crucibles.
Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move **a minimum of four blocks** in that direction before it can turn (or even before it can stop at the end).
However, it will eventually start to get wobbly: an ultra crucible can move a maximum of **ten consecutive blocks** without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

```
2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
```

In the above example, an ultra crucible would incur the minimum possible heat loss of **`94`**.

Here's another example:

```
111111111111
999999999991
999999999991
999999999991
999999999991
```

Sadly, an ultra crucible would need to take an unfortunate path like this one:

```
1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
```

This route causes the ultra crucible to incur the minimum possible heat loss of **`71`**.

Directing the ultra crucible from the lava pool to the machine parts factory, **what is the least heat loss it can incur?**

### Solution

Identical to Part 1 with a different minimum/maximum distance.

```python
from dataclasses import dataclass, field
from heapq import heappop, heappush

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 17: Clumsy Crucible"])


DOCUMENT_EXAMPLE = [
    "2413432311323",
    "3215453535623",
    "3255245654254",
    "3446585845452",
    "4546657867536",
    "1438598798454",
    "4457876987766",
    "3637877979653",
    "4654967986887",
    "4564679986453",
    "1224686865563",
    "2546548887735",
    "4322674655533",
]


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def __lt__(self, other: "Coordinate") -> bool:
        if self.x != other.x:
            return self.x < other.x

        return self.y < other.y


OFFSETS: list[Coordinate] = [
    Coordinate(x=0, y=-1),  # Up
    Coordinate(x=0, y=1),  # Down
    Coordinate(x=1, y=0),  # Right
    Coordinate(x=-1, y=0),  # Left
]


def do_180(coordinate: Coordinate) -> Coordinate:
    return Coordinate(x=-coordinate.x, y=-coordinate.y)


Edge = tuple[Coordinate, Coordinate | None, int]


@dataclass
class Grid:
    grid: dict[Coordinate, int]

    minimum_distance: int
    maximum_distance: int

    edges: dict[Edge, list[Edge]] = field(default_factory=dict)

    max_x: int = 0
    max_y: int = 0

    def add_coordinate(self, coordinate: Coordinate, cost: int) -> None:
        self.max_x = max(self.max_x, coordinate.x + 1)
        self.max_y = max(self.max_y, coordinate.y + 1)
        self.grid[coordinate] = cost

    def run(self) -> int:
        start = (Coordinate(x=0, y=0), None, 0)

        # Build up our cost path
        queue: list[tuple[int, Edge]] = [(0, start)]
        checked: set[Edge] = {start}

        while True:
            current_cost, (point, backwards_offset, distance) = heappop(queue)

            if (
                self.minimum_distance <= distance <= self.maximum_distance
                and point.x == self.max_x - 1
                and point.y == self.max_y - 1
            ):
                return current_cost

            edges: list[Edge] = []

            if backwards_offset is None:
                for next_offset in OFFSETS:
                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            elif distance < self.minimum_distance:
                # Gotta keep moving in the same direction
                next_point = Coordinate(
                    x=point.x + backwards_offset.x,
                    y=point.y + backwards_offset.y,
                )

                if next_point not in self.grid:
                    continue

                edges.append((next_point, backwards_offset, distance + 1))

            elif distance < self.maximum_distance:
                # Can turn now
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    if next_offset == backwards_offset:
                        edges.append((next_point, next_offset, distance + 1))

                    else:
                        edges.append((next_point, next_offset, 1))

            else:
                # Over the maximum, gotta turn
                for next_offset in OFFSETS:
                    if next_offset == do_180(backwards_offset):
                        # No 180 degree turns
                        continue

                    if next_offset == backwards_offset:
                        # No going straight
                        continue

                    next_point = Coordinate(
                        x=point.x + next_offset.x,
                        y=point.y + next_offset.y,
                    )

                    if next_point not in self.grid:
                        continue

                    edges.append((next_point, next_offset, 1))

            for edge in edges:
                if edge in checked:
                    continue

                checked.add(edge)
                current_point = edge[0]

                next_cost = current_cost + self.grid[current_point]
                heappush(
                    queue,
                    (next_cost, edge),
                )


@router.post("/part-2")
async def year_2023_day_17_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    grid = Grid(
        grid={},
        minimum_distance=4,
        maximum_distance=10,
    )

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(Coordinate(x=x_index, y=y_index), cost=int(character))

    return grid.run()
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 17  | 02:59:03    | 3,584       | 03:23:31    | 3,315       |

This was my first time using the [`heapq`](https://docs.python.org/3/library/heapq.html) module.
I really tried getting this to work with [`bisect.insort`](https://docs.python.org/3/library/bisect.html#bisect.insort), but wasn't able to get this working for unknown reasons 😒.

Keeping track of the "history" was mildly challenging, until I realized I could just keep track of the number of steps in the same direction we're moving in.
If I change direction, reset the step history counter.
