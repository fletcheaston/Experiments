from dataclasses import dataclass, field
from heapq import heappop, heappush

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 17: Title"])


DOCUMENT_EXAMPLE = []


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

    edges: dict[Edge, list[Edge]] = field(default_factory=dict)

    max_x: int = 0
    max_y: int = 0

    def add_coordinate(self, coordinate: Coordinate, cost: int) -> None:
        self.max_x = max(self.max_x, coordinate.x + 1)
        self.max_y = max(self.max_y, coordinate.y + 1)
        self.grid[coordinate] = cost

    def run(self) -> int:
        # Build up the edges in our graph
        for x in range(self.max_x):
            for y in range(self.max_y):
                point = Coordinate(x=x, y=y)

                for backwards_offset in OFFSETS:
                    for distance in [1, 2]:
                        current = (point, backwards_offset, distance)
                        self.edges[current] = []

                        for next_offset in OFFSETS:
                            # Skip 180 degree turns
                            if next_offset == do_180(backwards_offset):
                                continue

                            next_point = Coordinate(
                                x=point.x + next_offset.x,
                                y=point.y + next_offset.y,
                            )

                            # Skip points that aren't in the grid
                            if next_point not in self.grid:
                                continue

                            if next_offset == backwards_offset:
                                self.edges[current].append(
                                    (next_point, next_offset, distance + 1)
                                )
                            else:
                                self.edges[current].append((next_point, next_offset, 1))

                    current = (point, backwards_offset, 3)
                    self.edges[current] = []

                    for next_offset in OFFSETS:
                        # Skip 180 degree turns
                        if next_offset == do_180(backwards_offset):
                            continue

                        # Skip redundant moves
                        if next_offset == backwards_offset:
                            continue

                        next_point = Coordinate(
                            x=point.x + next_offset.x,
                            y=point.y + next_offset.y,
                        )

                        # Skip points that aren't in the grid
                        if next_point not in self.grid:
                            continue

                        self.edges[current].append((next_point, next_offset, 1))

        # Account for starting position
        start = (Coordinate(x=0, y=0), None, 0)
        self.edges[start] = []

        for next_offset in OFFSETS:
            if next_offset not in self.grid:
                continue

            self.edges[start].append((next_offset, next_offset, 1))

        # Build up our cost path
        queue: list[tuple[int, int, Edge]] = [
            (0, (self.max_x - 1) + (self.max_y - 1), start)
        ]
        checked: set[Edge] = {start}

        while True:
            # Get the smallest-cost edge from our queue
            current_cost, edge_cost, current_edge = heappop(queue)

            current_position = current_edge[0]

            # If we're at the end, we're done
            if (
                current_position.x == self.max_x - 1
                and current_position.y == self.max_y - 1
            ):
                return current_cost

            # Iterate over edges and keep searching
            for next_edge in self.edges[current_edge]:
                if next_edge in checked:
                    continue

                checked.add(next_edge)
                next_point = next_edge[0]
                next_cost = current_cost + self.grid[next_point]

                heappush(
                    queue,
                    (
                        next_cost,
                        self.max_x - 1 - next_point.x + self.max_y - 1 - next_point.y,
                        next_edge,
                    ),
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
    )

    for y_index, line in enumerate(document):
        for x_index, character in enumerate(line):
            grid.add_coordinate(Coordinate(x=x_index, y=y_index), cost=int(character))

    return grid.run()


@router.post("/part-2")
async def year_2023_day_17_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    for line in document:
        pass

    return total
