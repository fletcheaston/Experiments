import re
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import z3


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


def part_1(
    document: list[str],
    lower: int,
    upper: int,
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


def part_2(document: list[str]) -> int:
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


@pytest.mark.parametrize(
    "filename,lower,upper,output",
    [
        ("example-1.txt", 7, 27, 2),
        ("input.txt", 200000000000000, 400000000000000, 15558),
    ],
)
def test_part_1(
    filename: str,
    lower: int,
    upper: int,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines(), lower, upper) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 47),
        ("input.txt", 765636044333842),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
