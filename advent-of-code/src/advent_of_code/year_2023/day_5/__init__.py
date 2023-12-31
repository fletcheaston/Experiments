from dataclasses import dataclass
from pathlib import Path

import pytest

from src.advent_of_code.utils import chunks


def part_1(document: list[str], seeds: list[int]) -> int:
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


def part_2(document: list[str], seeds: list[int]) -> int:
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


@pytest.mark.parametrize(
    "filename,seeds,total",
    [
        ("example.txt", [79, 14, 55, 13], 35),
        (
            "input.txt",
            [
                1972667147,
                405592018,
                1450194064,
                27782252,
                348350443,
                61862174,
                3911195009,
                181169206,
                626861593,
                138786487,
                2886966111,
                275299008,
                825403564,
                478003391,
                514585599,
                6102091,
                2526020300,
                15491453,
                3211013652,
                546191739,
            ],
            662197086,
        ),
    ],
)
def test_part_1(filename: str, seeds: list[int], total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert (
            part_1(
                file.read().splitlines(),
                seeds,
            )
            == total
        )


@pytest.mark.parametrize(
    "filename,seeds,total",
    [
        ("example.txt", [79, 14, 55, 13], 46),
        (
            "input.txt",
            [
                1972667147,
                405592018,
                1450194064,
                27782252,
                348350443,
                61862174,
                3911195009,
                181169206,
                626861593,
                138786487,
                2886966111,
                275299008,
                825403564,
                478003391,
                514585599,
                6102091,
                2526020300,
                15491453,
                3211013652,
                546191739,
            ],
            52510809,
        ),
    ],
)
def test_part_2(filename: str, seeds: list[int], total: int) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert (
            part_2(
                file.read().splitlines(),
                seeds,
            )
            == total
        )
