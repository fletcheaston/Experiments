from fastapi import APIRouter

from src.types import Lines

router = APIRouter(tags=["2022 - Day 4: Camp Cleanup"])


@router.post("/part-1")
async def year_2022_day_4_part_1(lines: Lines) -> int:
    total = 0

    # Iterate over lines
    for line in lines:
        assignment_left, assignment_right = line.split(",")

        # Parse the left assignment
        assignment_left_start = int(assignment_left.split("-")[0])
        assignment_left_end = int(assignment_left.split("-")[1])

        assignment_left_all = set(range(assignment_left_start, assignment_left_end + 1))

        # Parse the right assignment
        assignment_right_start = int(assignment_right.split("-")[0])
        assignment_right_end = int(assignment_right.split("-")[1])

        assignment_right_all = set(
            range(assignment_right_start, assignment_right_end + 1)
        )

        # Check for assignment containment
        if assignment_left_all.issubset(
            assignment_right_all
        ) or assignment_right_all.issubset(assignment_left_all):
            total += 1

    return total


@router.post("/part-2")
async def year_2022_day_4_part_2(lines: Lines) -> int:
    total = 0

    # Iterate over lines
    for line in lines:
        assignment_left, assignment_right = line.split(",")

        # Parse the left assignment
        assignment_left_start = int(assignment_left.split("-")[0])
        assignment_left_end = int(assignment_left.split("-")[1])

        assignment_left_all = set(range(assignment_left_start, assignment_left_end + 1))

        # Parse the right assignment
        assignment_right_start = int(assignment_right.split("-")[0])
        assignment_right_end = int(assignment_right.split("-")[1])

        assignment_right_all = set(
            range(assignment_right_start, assignment_right_end + 1)
        )

        # Check for assignment containment
        if assignment_left_all.intersection(assignment_right_all):
            total += 1

    return total
