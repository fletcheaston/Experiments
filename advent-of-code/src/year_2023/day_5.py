from dataclasses import dataclass

from fastapi import APIRouter, Body

from src.utils import chunks

router = APIRouter(tags=["2023 - Day 5: Title"])


DOCUMENT_EXAMPLE = []


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
    ),
) -> int:
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

        # Iterate over lines
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
    ),
) -> int:
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

    # Iterate over lines
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
