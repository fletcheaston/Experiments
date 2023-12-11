from dataclasses import dataclass

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 10: Title"])


DOCUMENT_EXAMPLE = []


@dataclass
class Position:
    x: int
    y: int


# (character, x-offset, y-offset) -> (x-offset, y-offset)
OFFSET_MAP: dict[tuple[str, int, int], Position] = {
    ("|", 0, 1): Position(x=0, y=1),
    ("|", 0, -1): Position(x=0, y=-1),
    ("-", 1, 0): Position(x=1, y=0),
    ("-", -1, 0): Position(x=-1, y=0),
    ("L", 0, 1): Position(x=1, y=0),
    ("L", -1, 0): Position(x=0, y=-1),
    ("J", 1, 0): Position(x=0, y=-1),
    ("J", 0, 1): Position(x=-1, y=0),
    ("7", 1, 0): Position(x=0, y=1),
    ("7", 0, -1): Position(x=-1, y=0),
    ("F", -1, 0): Position(x=0, y=1),
    ("F", 0, -1): Position(x=1, y=0),
}


@dataclass
class Map:
    start: Position
    current: Position
    positions: list[Position]

    characters: list[list[str]]

    def get_character(self, x: int, y: int) -> str | None:
        if 0 <= x < len(self.characters[0]) and 0 <= y <= len(self.characters):
            return self.characters[y][x]

        return None

    def run(self) -> int:
        steps = 0

        # Move one position manually
        next_offset: Position | None = None

        for x_offset, y_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_character = self.get_character(
                x=self.current.x + x_offset,
                y=self.current.y + y_offset,
            )

            if OFFSET_MAP.get((next_character, x_offset, y_offset)):
                next_offset = OFFSET_MAP[(next_character, x_offset, y_offset)]
                self.current = Position(
                    x=self.current.x + x_offset, y=self.current.y + y_offset
                )

                steps += 1

                break

        while self.current != self.start:
            # Get the character at the next position
            next_character = self.get_character(
                x=self.current.x + next_offset.x,
                y=self.current.y + next_offset.y,
            )

            self.positions.append(self.current)
            self.current = Position(
                x=self.current.x + next_offset.x, y=self.current.y + next_offset.y
            )

            steps += 1

            next_offset = OFFSET_MAP.get((next_character, next_offset.x, next_offset.y))

        return steps // 2

    def is_in_loop(self, x: int, y: int) -> bool:
        for position in self.positions:
            if position.x == x and position.y == y:
                return True

        return False

    def get_enclosed_positions(self) -> int:
        enclosed = 0

        for y_index in range(len(self.characters)):
            for x_index in range(len(self.characters[0])):
                if not self.is_in_loop(x_index, y_index):
                    crosses = 0

                    # Offset by 0.5 to account for corners, points, etc.
                    y_position = y_index + 0.5

                    # For each point pair in the loop, see if we intersect it
                    for p_index in range(len(self.positions) - 1):
                        a = self.positions[p_index]
                        b = self.positions[p_index + 1]

                        if a.y == b.y:
                            continue

                        if a.y > y_position > b.y or a.y < y_position < b.y:
                            if a.x > x_index and b.x > x_index:
                                crosses += 1

                    if crosses % 2 == 1:
                        self.characters[y_index][x_index] = "E"
                        enclosed += 1

        return enclosed

    # def open_borders(self) -> None:
    #     for y_index in range(len(self.characters)):
    #         for x_index in range(len(self.characters[0])):
    #             if not self.is_in_loop(x_index, y_index):
    #                 if y_index == 0:
    #                     self.characters[y_index][x_index] = "O"
    #
    #                 if y_index == len(self.characters) - 1:
    #                     self.characters[y_index][x_index] = "O"
    #
    #                 if x_index == 0:
    #                     self.characters[y_index][x_index] = "O"
    #
    #                 if x_index == len(self.characters[0]) - 1:
    #                     self.characters[y_index][x_index] = "O"
    #
    # def expand(self) -> None:
    #     pass

    def show(self) -> None:
        for line in self.characters:
            print(line)


@router.post("/part-1")
async def year_2023_day_10_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    character_map: list[list[str]] = []

    # (x, y)
    position = Position(x=0, y=0)

    # Iterate over lines
    for y_index, line in enumerate(document):
        character_map.append(list(line))

        for x_index, character in enumerate(line):
            if character == "S":
                position = Position(x=x_index, y=y_index)

    pipe_map = Map(
        start=position,
        current=position,
        positions=[position],
        characters=character_map,
    )

    # Check around the start position for connected positions
    return pipe_map.run()


@router.post("/part-2")
async def year_2023_day_10_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    character_map: list[list[str]] = []

    # (x, y)
    position = Position(x=0, y=0)

    # Iterate over lines
    for y_index, line in enumerate(document):
        character_map.append(list(line))

        for x_index, character in enumerate(line):
            if character == "S":
                position = Position(x=x_index, y=y_index)

    pipe_map = Map(
        start=position,
        current=position,
        positions=[position],
        characters=character_map,
    )

    # Check around the start position for connected positions
    pipe_map.run()

    print()

    pipe_map.show()

    value = pipe_map.get_enclosed_positions()

    print()

    pipe_map.show()

    # Get enclosed positions
    return value
