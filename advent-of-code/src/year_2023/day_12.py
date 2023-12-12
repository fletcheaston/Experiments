from functools import cache

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 12: Title"])


DOCUMENT_EXAMPLE = []


@cache
def arrangements(springs: str, counts: tuple[int]) -> set[str]:
    joins: list[str] = []
    join: str = ""

    sub_springs: list[str] = []
    sub_spring: str = ""

    contigs: list[int] = []
    contig: int = 0

    for spring in springs:
        if spring == ".":
            join += "."

            if contig:
                contigs.append(contig)
                contig = 0

            if sub_spring:
                sub_springs.append(sub_spring)
                sub_spring = ""

        else:
            sub_spring += spring

            if join:
                joins.append(join)

        if spring == "#":
            contig += 1

    if join:
        joins.append(join)

    if sub_spring:
        sub_springs.append(sub_spring)

    if contig:
        contigs.append(contig)

    # If spring groups == counts, we're good
    # Clear out the remaining ?s
    if contigs == list(counts):
        # If we have ?s, replace with . and try again just to confirm
        if "?" in springs:
            return arrangements(springs.replace("?", "."), counts)

        # Otherwise, we're all good!
        return {springs}

    # We have correct group sizes, just split and look for different sub-springs
    if len(contigs) == len(counts):
        print(springs, sub_springs, joins, contigs, counts)

        possible_arrangements: set[str] = set()

        for index, (sub_spring, count) in enumerate(zip(sub_springs, counts)):
            if sub_spring.count("#") != count:
                # Try with sub-spring
                sub_arrangements = arrangements(sub_spring, (count,))

                for sub_arrangement in sub_arrangements:
                    pass

        return possible_arrangements

    if len(contigs) <= len(counts):
        possible_arrangements: set[str] = set()

        # Replace a ? and try again
        springs_list = list(springs)

        for index in range(len(springs_list)):
            if springs_list[index] == "?":
                # Try with a #
                broken_springs_list = springs_list.copy()
                broken_springs_list[index] = "#"
                broken_springs = "".join(broken_springs_list)

                possible_arrangements.update(
                    arrangements("".join(broken_springs), counts)
                )

                # Try with a .
                broken_springs_list = springs_list.copy()
                broken_springs_list[index] = "."
                broken_springs = "".join(broken_springs_list)

                possible_arrangements.update(
                    arrangements("".join(broken_springs), counts)
                )

        return possible_arrangements

    # Invalid arrangement
    return set()


@router.post("/part-1")
async def year_2023_day_12_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for index, line in enumerate(document):
        print(index)
        springs, count_str = line.split(" ")
        counts = tuple(int(value) for value in count_str.split(","))

        print(springs, counts)

        total += len(arrangements(springs, counts))

    return total


@router.post("/part-2")
async def year_2023_day_12_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    # Iterate over lines
    for line in document:
        pass

    return total
