from dataclasses import dataclass, field

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 10: Title"])


DOCUMENT_EXAMPLE = [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ...",
]


OPEN_CHARACTER = "\033[94m█\033[0m"
ENCLOSED_CHARACTER = "\033[31m█\033[0m"


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

EXPAND_MAP: dict[str, tuple[list[str], list[str], list[str]]] = {
    OPEN_CHARACTER: (
        [OPEN_CHARACTER, OPEN_CHARACTER, OPEN_CHARACTER],
        [OPEN_CHARACTER, OPEN_CHARACTER, OPEN_CHARACTER],
        [OPEN_CHARACTER, OPEN_CHARACTER, OPEN_CHARACTER],
    ),
    ENCLOSED_CHARACTER: (
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
    ),
    "S": (
        ["S", "S", "S"],
        ["S", "S", "S"],
        ["S", "S", "S"],
    ),
    "|": (
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
    ),
    "-": (
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
        ["-", "-", "-"],
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
    ),
    "L": (
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, "L", "-"],
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
    ),
    "J": (
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
        ["-", "J", ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
    ),
    "7": (
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
        ["-", "7", ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
    ),
    "F": (
        [ENCLOSED_CHARACTER, ENCLOSED_CHARACTER, ENCLOSED_CHARACTER],
        [ENCLOSED_CHARACTER, "F", "-"],
        [ENCLOSED_CHARACTER, "|", ENCLOSED_CHARACTER],
    ),
}


@dataclass
class Map:
    start: Position
    current: Position

    positions: list[Position]
    characters: list[list[str]]

    expanded_characters: list[list[str]] = field(default_factory=list)

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
                        self.characters[y_index][x_index] = ENCLOSED_CHARACTER
                        enclosed += 1

        return enclosed

    def cleanup(self) -> None:
        for y_index in range(len(self.characters)):
            for x_index in range(len(self.characters[0])):
                if not self.is_in_loop(x_index, y_index):
                    if y_index == 0:
                        self.characters[y_index][x_index] = OPEN_CHARACTER

                    elif y_index == len(self.characters) - 1:
                        self.characters[y_index][x_index] = OPEN_CHARACTER

                    elif x_index == 0:
                        self.characters[y_index][x_index] = OPEN_CHARACTER

                    elif x_index == len(self.characters[0]) - 1:
                        self.characters[y_index][x_index] = OPEN_CHARACTER

                    else:
                        self.characters[y_index][x_index] = ENCLOSED_CHARACTER

    def expand(self) -> None:
        # 3x the height of characters
        self.expanded_characters = [[] for _ in range(len(self.characters) * 3)]

        for y_index in range(len(self.characters)):
            for x_index in range(len(self.characters[0])):
                character = self.characters[y_index][x_index]

                first_line, second_line, third_line = EXPAND_MAP[character]

                self.expanded_characters[y_index * 3] += first_line
                self.expanded_characters[y_index * 3 + 1] += second_line
                self.expanded_characters[y_index * 3 + 2] += third_line

    def flood_fill(self) -> None:
        # {(x, y)}
        positions_to_check: set[tuple[int, int]] = set()

        # Fill positions to check with initial data of all Os
        for y_index in range(len(self.expanded_characters)):
            for x_index in range(len(self.expanded_characters[0])):
                character = self.expanded_characters[y_index][x_index]

                if character == OPEN_CHARACTER:
                    positions_to_check.add((x_index, y_index))

        while positions_to_check:
            x_index, y_index = positions_to_check.pop()

            # Check in cardinal directions
            for x_offset, y_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                try:
                    character = self.expanded_characters[y_index + y_offset][
                        x_index + x_offset
                    ]

                    if character == ENCLOSED_CHARACTER:
                        self.expanded_characters[y_index + y_offset][
                            x_index + x_offset
                        ] = OPEN_CHARACTER
                        positions_to_check.add((x_index + x_offset, y_index + y_offset))
                except IndexError:
                    pass

    def shrink(self) -> None:
        for y_index in range(0, len(self.expanded_characters), 3):
            for x_index in range(0, len(self.expanded_characters[0]), 3):
                # Get the center of each 3x3 grid
                character = self.expanded_characters[y_index - 2][x_index - 2]
                self.characters[y_index // 3 - 1][x_index // 3 - 1] = character

    def count(self, character: str) -> int:
        total = 0

        for y_index in range(len(self.characters)):
            for x_index in range(len(self.characters[0])):
                if self.characters[y_index][x_index] == character:
                    total += 1

        return total


@router.post("/part-1")
async def year_2023_day_10_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    character_map: list[list[str]] = []

    position = Position(x=0, y=0)

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

    position = Position(x=0, y=0)

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

    pipe_map.run()
    pipe_map.cleanup()
    pipe_map.expand()
    pipe_map.flood_fill()
    pipe_map.shrink()

    return pipe_map.count(ENCLOSED_CHARACTER)
