from dataclasses import dataclass

from fastapi import APIRouter, Body

from src.utils import chunks

router = APIRouter(tags=["2023 - Day 5: If You Give A Seed A Fertilizer"])


DOCUMENT_EXAMPLE = [
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]

SEED_EXAMPLE = [79, 14, 55, 13]


@router.post("/part-1")
async def year_2023_day_5_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    seeds: list[int] = Body(
        ...,
        embed=True,
        examples=[SEED_EXAMPLE],
    ),
) -> int:
    """
    You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

    "A water source?
    Island Island **is** the water source!"
    You point out that Snow Island isn't receiving any water.

    "Oh, we had to stop the water because we **ran out of sand** to filter it with!
    Can't make snow with dirty water.
    Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no."
    His face sinks into a look of horrified realization.

    "I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand!
    There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat.
    Could you please go check it out?"

    You barely have time to agree to this request when he brings up another.
    "While you wait for the ferry, maybe you can help us with our **food production problem**.
    The latest Island Island Almanac just arrived and we're having trouble making sense of it."

    The almanac (your puzzle input) lists all of the seeds that need to be planted.
    It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on.
    Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil `123` and fertilizer `123` aren't necessarily related to each other.

    For example:

    ```
    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4
    ```

    The almanac starts by listing which seeds need to be planted: seeds `79`, `14`, `55`, and `13`.

    The rest of the almanac contains a list of **maps** which describe how to convert numbers from a **source category** into numbers in a **destination category**.
    That is, the section that starts with `seed-to-soil map:` describes how to convert a **seed number** (the source) to a **soil number** (the destination).
    This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

    Rather than list every source number and its corresponding destination number one by one, the maps describe entire **ranges** of numbers that can be converted.
    Each line within a map contains three numbers: the **destination range start**, the **source range start**, and the **range length**.

    Consider again the example `seed-to-soil map`:

    ```
    50 98 2
    52 50 48
    ```

    The first line has a **destination range start** of `50`, a **source range start** of `98`, and a range length of `2`.
    This line means that the source range starts at `98` and contains two values: `98` and `99`.
    The destination range is the same length, but it starts at `50`, so its two values are `50` and `51`.
    With this information, you know that seed number `98` corresponds to soil number `50` and that seed number `99` corresponds to soil number `51`.

    The second line means that the source range starts at `50` and contains `48` values: `50`, `51`, ..., `96`, `97`.
    This corresponds to a destination range starting at `52` and also containing `48` values: `52`, `53`, ..., `98`, `99`.
    So, seed number `53` corresponds to soil number `55`.

    Any source numbers that **aren't mapped** correspond to the **same** destination number.
    So, seed number `10` corresponds to soil number `10`.

    So, the entire list of seed numbers and their corresponding soil numbers looks like this:

    ```
    seed  soil
    0     0
    1     1
    ...   ...
    48    48
    49    49
    50    52
    51    53
    ...   ...
    96    98
    97    99
    98    50
    99    51
    ```

    With this map, you can look up the soil number required for each initial seed number:

    - Seed number `79` corresponds to soil number `81`.
    - Seed number `14` corresponds to soil number `14`.
    - Seed number `55` corresponds to soil number `57`.
    - Seed number `13` corresponds to soil number `13`.

    The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed.
    Using these maps, find the **lowest location number that corresponds to any of the initial seeds**.
    To do this, you'll need to convert each seed number through other categories until you can find its corresponding **location number**.
    In this example, the corresponding types are:

    - Seed `79`, soil `81`, fertilizer `81`, water `81`, light `74`, temperature `78`, humidity `78`, **location `82`**.
    - Seed `14`, soil `14`, fertilizer `53`, water `49`, light `42`, temperature `42`, humidity `43`, **location `43`**.
    - Seed `55`, soil `57`, fertilizer `57`, water `53`, light `46`, temperature `82`, humidity `82`, **location `86`**.
    - Seed `13`, soil `13`, fertilizer `52`, water `41`, light `34`, temperature `34`, humidity `35`, **location `35`**.

    So, the lowest location number in this example is **`35`**.

    **What is the lowest location number that corresponds to any of the initial seed numbers?**
    """
    locations: list[int] = []

    mode = "seed-to-soil-map:"

    for seed in seeds:
        soil = 0
        fertilizer = 0
        water = 0
        light = 0
        temperature = 0
        humidity = 0
        location = 0

        for line in document:
            if not line:
                pass

            elif ":" in line:
                mode = line

                if mode == "seed-to-soil map:":
                    soil = seed

                if mode == "soil-to-fertilizer map:":
                    fertilizer = soil

                if mode == "fertilizer-to-water map:":
                    water = fertilizer

                if mode == "water-to-light map:":
                    light = water

                if mode == "light-to-temperature map:":
                    temperature = light

                if mode == "temperature-to-humidity map:":
                    humidity = temperature

                if mode == "humidity-to-location map:":
                    location = humidity

            else:
                destination_start_str, source_start_str, range_length_str = line.split(
                    " "
                )

                destination_start = int(destination_start_str)
                source_start = int(source_start_str)
                range_length = int(range_length_str)

                if mode == "seed-to-soil map:":
                    if source_start <= seed < source_start + range_length:
                        soil = seed + (destination_start - source_start)

                if mode == "soil-to-fertilizer map:":
                    if source_start <= soil < source_start + range_length:
                        fertilizer = soil + (destination_start - source_start)

                if mode == "fertilizer-to-water map:":
                    if source_start <= fertilizer < source_start + range_length:
                        water = fertilizer + (destination_start - source_start)

                if mode == "water-to-light map:":
                    if source_start <= water < source_start + range_length:
                        light = water + (destination_start - source_start)

                if mode == "light-to-temperature map:":
                    if source_start <= light < source_start + range_length:
                        temperature = light + (destination_start - source_start)

                if mode == "temperature-to-humidity map:":
                    if source_start <= temperature < source_start + range_length:
                        humidity = temperature + (destination_start - source_start)

                if mode == "humidity-to-location map:":
                    if source_start <= humidity < source_start + range_length:
                        location = humidity + (destination_start - source_start)

        locations.append(location)

    return min(locations)


@dataclass(frozen=True)
class Location:
    start: int
    end: int


@dataclass(frozen=True)
class Map:
    start: int
    end: int
    offset: int


@router.post("/part-2")
async def year_2023_day_5_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
    seeds: list[int] = Body(
        ...,
        embed=True,
        examples=[SEED_EXAMPLE],
    ),
) -> int:
    """
    Everyone will starve if you only plant such a small number of seeds.
    Re-reading the almanac, it looks like the seeds: line actually describes **ranges of seed numbers**.

    The values on the initial `seeds:` line come in pairs.
    Within each pair, the first value is the **start** of the range and the second value is the **length** of the range.
    So, in the first line of the example above:

    ```
    seeds: 79 14 55 13
    ```

    This line describes two ranges of seed numbers to be planted in the garden.
    The first range starts with seed number `79` and contains `14` values: `79`, `80`, ..., `91`, `92`.
    The second range starts with seed number `55` and contains `13` values: `55`, `56`, ..., `66`, `67`.

    Now, rather than considering four seed numbers, you need to consider a total of **`27`** seed numbers.

    In the above example, the lowest location number can be obtained from seed number `82`, which corresponds to soil `84`, fertilizer `84`, water `84`, light `77`, temperature `45`, humidity `46`, and **location `46`**.
    So, the lowest location number is **`46`**.

    Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
    **What is the lowest location number that corresponds to any of the initial seed numbers?**
    """
    modes = [
        "seed-to-soil map:",
        "soil-to-fertilizer map:",
        "fertilizer-to-water map:",
        "water-to-light map:",
        "light-to-temperature map:",
        "temperature-to-humidity map:",
        "humidity-to-location map:",
        "final",
    ]

    mode_to_locations: dict[str, list[Location]] = {
        "seed-to-soil map:": [
            Location(start=start, end=start + size - 1)
            for start, size in chunks(seeds, 2)
        ],
        "soil-to-fertilizer map:": [],
        "fertilizer-to-water map:": [],
        "water-to-light map:": [],
        "light-to-temperature map:": [],
        "temperature-to-humidity map:": [],
        "humidity-to-location map:": [],
    }

    mode_to_map: dict[str, list[Map]] = {
        "seed-to-soil map:": [],
        "soil-to-fertilizer map:": [],
        "fertilizer-to-water map:": [],
        "water-to-light map:": [],
        "light-to-temperature map:": [],
        "temperature-to-humidity map:": [],
        "humidity-to-location map:": [],
    }

    mode = "seed-to-soil map:"

    for line in document:
        if not line:
            pass

        elif ":" in line:
            mode = line

        else:
            destination_start_str, source_start_str, range_length_str = line.split(" ")

            destination_start = int(destination_start_str)
            source_start = int(source_start_str)
            range_length = int(range_length_str)

            mode_to_map[mode].append(
                Map(
                    start=source_start,
                    end=source_start + range_length - 1,
                    offset=destination_start - source_start,
                )
            )

    for index, mode in enumerate(modes[:-1]):
        maps = mode_to_map[mode]
        locations = mode_to_locations[mode]

        next_locations: list[Location] = []

        while locations:
            location = locations.pop()
            found = False

            for map in maps:
                if (
                    map.start <= location.start <= map.end
                    and map.start <= location.end <= map.end
                ):
                    next_locations.append(
                        Location(
                            start=location.start + map.offset,
                            end=location.end + map.offset,
                        )
                    )
                    found = True
                    break

                elif map.start <= location.start <= map.end:
                    next_locations.append(
                        Location(
                            start=location.start + map.offset,
                            end=map.end + map.offset,
                        )
                    )
                    locations.append(
                        Location(
                            start=map.end + 1,
                            end=location.end,
                        )
                    )
                    found = True
                    break

                elif map.start <= location.end <= map.end:
                    locations.append(
                        Location(
                            start=location.start,
                            end=map.start - 1,
                        )
                    )
                    next_locations.append(
                        Location(
                            start=map.start + map.offset,
                            end=location.end + map.offset,
                        )
                    )
                    found = True
                    break

                elif map.start > location.start and map.end < location.end:
                    locations.append(
                        Location(
                            start=map.end + 1,
                            end=location.end,
                        )
                    )
                    locations.append(
                        Location(
                            start=location.start,
                            end=map.start - 1,
                        )
                    )
                    next_locations.append(
                        Location(
                            start=map.start + map.offset,
                            end=map.end + map.offset,
                        )
                    )
                    found = True
                    break

            if not found:
                next_locations.append(location)

        mode_to_locations[modes[index + 1]] = next_locations

    final_locations = mode_to_locations["final"]

    return min([location.start for location in final_locations])
