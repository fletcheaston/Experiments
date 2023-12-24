import re
import uuid
from dataclasses import dataclass, field

import z3
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 24: Title"])


DOCUMENT_EXAMPLE = []


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

    def __repr__(self) -> str:
        return f"{self.id} | ({self.start}, {self.velocity})"


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

    px = z3.BitVec("px", 64)
    py = z3.BitVec("py", 64)
    pz = z3.BitVec("pz", 64)

    vx = z3.BitVec("vx", 64)
    vy = z3.BitVec("vy", 64)
    vz = z3.BitVec("vz", 64)

    for hailstone in hailstones:
        time = z3.BitVec(f"hailstone_{hailstone.id}_time", 64)

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
