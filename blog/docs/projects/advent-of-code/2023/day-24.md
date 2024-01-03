# Day 24: Never Tell Me The Odds

## Part 1

### Prompt

It seems like something is going wrong with the snow-making process.
Instead of forming snow, the water that's been absorbed into the air seems to be forming hail!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories.
You make a note of each hailstone's **position** and **velocity** (your puzzle input).
For example:

```
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
```

Each line of text corresponds to the position and velocity of a single hailstone.
The positions indicate where the hailstones are **right now** (at time 0).
The velocities are constant and indicate exactly how far each hailstone will move in **one nanosecond**.

Each line of text uses the format `px py pz @ vx vy vz`.
For instance, the hailstone specified by `20, 19, 15 @ 1, -5, -3` has initial X position `20`, Y position `19`, Z position `15`, X velocity `1`, Y velocity `-5`, and Z velocity `-3`.
After one nanosecond, the hailstone would be at `21, 14, 12`.

Perhaps you won't have to do anything.
How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; **ignore the Z axis**.
Looking **forward in time**, how many of the hailstones' **paths** will intersect within a test area?
(The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least `7` and at most `27`; in your actual data, you'll need to check a much larger test area.
Comparing all pairs of hailstones' future paths produces the following results:

```
Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
```

So, in this example, **`2`** hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide.
Look for intersections that happen with an X and Y position each at least `200000000000000` and at most `400000000000000`.
Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections.
**How many of these intersections occur within the test area?**

### Solution

Find intersections between combinations of hailstones.
Check to see if that intersection is in the future for each hailstone.
Check to see if that intersection occurs within the specified boundary.

```python
import re
import uuid
from dataclasses import dataclass, field

from fastapi import APIRouter, Body

router = APIRouter()


DOCUMENT_EXAMPLE = [
    "19, 13, 30 @ -2,  1, -2",
    "18, 19, 22 @ -1, -1, -2",
    "20, 25, 34 @ -2, -2, -4",
    "12, 31, 28 @ -1, -2, -1",
    "20, 19, 15 @  1, -5, -3",
]


@dataclass
class Coordinate:
    x: int
    y: int
    z: int


@dataclass
class Velocity:
    x: int
    y: int
    z: int


@dataclass
class Hailstone:
    start: Coordinate
    velocity: Velocity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def next(self) -> Coordinate:
        return Coordinate(
            x=self.start.x + self.velocity.x,
            y=self.start.y + self.velocity.y,
            z=self.start.z + self.velocity.z,
        )

    def intersects(
        self, other: "Hailstone"
    ) -> tuple[float, float, float, float, float] | None:
        xdiff = (self.start.x - self.next.x, other.start.x - other.next.x)
        ydiff = (self.start.y - self.next.y, other.start.y - other.next.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            # Parallel, no intersections ever
            return None

        d = (
            det((self.start.x, self.start.y), (self.next.x, self.next.y)),
            det((other.start.x, other.start.y), (other.next.x, other.next.y)),
        )
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        return (
            x,
            y,
            0,
            (x - self.start.x) / self.velocity.x,
            (x - other.start.x) / other.velocity.x,
        )


@router.post("/part-1")
async def year_2023_day_24_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    lower: int = Body(
        ...,
        embed=True,
        examples=[7],
    ),
    upper: int = Body(
        ...,
        embed=True,
        examples=[27],
    ),
) -> int:
    hailstones: list[Hailstone] = []

    for index, line in enumerate(document):
        line = re.sub(" +", " ", line)
        px, py, pz, _, vx, vy, vz = line.replace(",", "").split(" ")
        hailstones.append(
            Hailstone(
                start=Coordinate(
                    x=int(px),
                    y=int(py),
                    z=int(pz),
                ),
                velocity=Velocity(
                    x=int(vx),
                    y=int(vy),
                    z=int(vz),
                ),
            ),
        )

    collisions = 0

    for start in range(len(hailstones) - 1):
        for end in range(start + 1, len(hailstones)):
            intersection = hailstones[start].intersects(hailstones[end])

            if intersection is not None:
                x, y, _, time_start, time_end = intersection

                if (
                    time_start > 0
                    and time_end > 0
                    and lower <= x <= upper
                    and lower <= y <= upper
                ):
                    collisions += 1

    return collisions
```

## Part 2

### Prompt

Upon further analysis, it doesn't seem like **any** hailstones will naturally collide.
It's up to you to fix that!

You find a rock on the ground nearby.
While it seems extremely unlikely, if you throw it just right, you should be able to **hit every hailstone in a single throw**!

You can use the probably-magical winds to reach **any integer position** you like and to propel the rock at **any integer velocity**.
Now **including the Z axis** in your calculations, if you throw the rock at time 0, where do you need to be so that the rock **perfectly collides with every hailstone**?
Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position `24, 13, 10` and throwing the rock at velocity `-3, 1, 2`.
If you do this, you will hit every hailstone as follows:

```
Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
```

Above, each hailstone is identified by its initial position and its velocity.
Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has **exactly the same position** as one of the hailstones, obliterating it into ice dust!
Another hailstone is smashed to bits two nanoseconds after that.
After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time `0`, the rock needs to be at X position `24`, Y position `13`, and Z position `10`.
Adding these three coordinates together produces **`47`**.
(Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time `0` so that it perfectly collides with every hailstone.
**What do you get if you add up the X, Y, and Z coordinates of that initial position?**

### Solution

Set up a [`z3.Solver`](https://z3prover.github.io/papers/programmingz3.html#sec-solver-interfacing) to solve the system of equations.
Add a constraint for time (must always be in the future).
For each hailstone, add a constraint on the future position of the hailstone to collide with our rock.
Extract the outputs.

```python
import re
import uuid
from dataclasses import dataclass, field

import z3
from fastapi import APIRouter, Body

router = APIRouter()


DOCUMENT_EXAMPLE = [
    "19, 13, 30 @ -2,  1, -2",
    "18, 19, 22 @ -1, -1, -2",
    "20, 25, 34 @ -2, -2, -4",
    "12, 31, 28 @ -1, -2, -1",
    "20, 19, 15 @  1, -5, -3",
]


@dataclass
class Coordinate:
    x: int
    y: int
    z: int


@dataclass
class Velocity:
    x: int
    y: int
    z: int


@dataclass
class Hailstone:
    start: Coordinate
    velocity: Velocity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@router.post("/part-2")
async def year_2023_day_24_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    hailstones: list[Hailstone] = []

    for index, line in enumerate(document):
        line = re.sub(" +", " ", line)
        px, py, pz, _, vx, vy, vz = line.replace(",", "").split(" ")
        hailstones.append(
            Hailstone(
                start=Coordinate(
                    x=int(px),
                    y=int(py),
                    z=int(pz),
                ),
                velocity=Velocity(
                    x=int(vx),
                    y=int(vy),
                    z=int(vz),
                ),
            ),
        )

    solver = z3.Solver()

    px = z3.Real("px")
    py = z3.Real("py")
    pz = z3.Real("pz")

    vx = z3.Real("vx")
    vy = z3.Real("vy")
    vz = z3.Real("vz")

    for hailstone in hailstones:
        time = z3.Real(f"hailstone_{hailstone.id}_time")

        # Must be in the future
        solver.add(time >= 0)

        # Solve for x-axis
        solver.add(px + vx * time == hailstone.start.x + hailstone.velocity.x * time)

        # Solve for y-axis
        solver.add(py + vy * time == hailstone.start.y + hailstone.velocity.y * time)

        # Solve for z-axis
        solver.add(pz + vz * time == hailstone.start.z + hailstone.velocity.z * time)

    assert solver.check() == z3.sat

    model = solver.model()

    x = model.eval(px).as_long()
    y = model.eval(py).as_long()
    z = model.eval(pz).as_long()

    return x + y + z
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 24  | 00:43:58    | 996         | 01:37:41    | 494         |

Part 1 wasn't all that hard.
But when I put together a library of helper functions, line intersections will definitely be in there.
I had a little bit of trouble figuring out **when** the hailstone paths intersected, so I could verify that an intersection was in the future, but it wasn't too bad to figure out.

I spent a lot of time thinking about how to solve Part 2, but couldn't make any real progress.
Lots of others used `z3`, so I figured I would as well.
It turned out to be super simple, but using a tool like `z3` kinda felt a little cheap.

To make up for it, I've done the system of equations by hand down below.
I don't need nearly as many constraints as I used in Part 2, the code over-constrains the solver, so it shouldn't be too bad.

## Part 2 Solution by Hand

### Variables to Solve For

- `xpr` - x-position of our rock
- `ypr` - y-position of our rock
- `zpr` - z-position of our rock
- `xvr` - x-velocity of our rock
- `yvr` - y-velocity of our rock
- `zvr` - z-velocity of our rock

### Variables and Equations

We need one equation for each variable.
Our rock has 6 variables, so we need 6 equations there.

For each hailstone, we get 3 equations, one for each of the `x`, `y`, and `z` components.
But we also get another variable of time for each hailstone.

If we have 1 hailstone, we end up with 7 variables (6 for the rock, 1 for hailstone time) and 3 equations.
If we have 2 hailstones, we end up with 8 variables (6 for the rock, 2 for hailstone times) and 6 equations.
If we have 3 hailstones, we end up with 9 variables (6 for the rock, 3 for hailstone times) and 9 equations.

So at minimum, we need 3 hailstones to calculate our final answer.

Format: `xp`, `yp`, `zp` @ `xv`, `yv`, `zv`

- `171178400007298`, `165283791547432`, `246565404194007` @ `190`, `186`, `60` - hailstone 1
- `250314870325177`, `283762496814661`, `272019235409859` @ `45`, `15`, `8` - hailstone 2
- `192727134181171`, `456146317292988`, `246796112051543` @ `22`, `-541`, `-70` - hailstone 3

We'll use these variables for each hailstone: `xph1`, `yph1`, etc.

Each hailstone also has a time for when it's hit by the rock, denoted as `th1`, etc.

### System of Equations

`Rock Position + Rock Velocity * Hailstone Time = Hailstone Position + Hailstone Velocity * Hailstone Time`

**Hailstone 1**

$$
xpr + xvr * th1 = 171178400007298 + 190 * th1
$$

$$
ypr + yvr * th1 = 165283791547432 + 186 * th1
$$

$$
zpr + zvr * th1 = 246565404194007 + 60 * th1
$$

**Hailstone 2**

$$
xpr + xvr * th2 = 250314870325177 + 45 * th2
$$

$$
ypr + yvr * th2 = 283762496814661 + 15 * th2
$$

$$
zpr + zvr * th2 = 283762496814661 + 8 * th2
$$

**Hailstone 3**

$$
xpr + xvr * th3 = 192727134181171 + 22 * th3
$$

$$
ypr + yvr * th3 = 456146317292988 + -541 * th3
$$

$$
zpr + zvr * th3 = 246796112051543 + -70 * th3
$$
