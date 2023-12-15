from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 15: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_15_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    for line in document:
        line_total = 0

        for character in line:
            line_total += ord(character)

            line_total *= 17

            line_total %= 256

        total += line_total

    return total


@router.post("/part-2")
async def year_2023_day_15_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    boxes: list[list[str]] = [[] for _ in range(256)]

    for line in document:
        if "=" in line:
            label, focal_length = line.split("=")
            operator = "="

        elif "-" in line:
            label = line.split("-")[0]
            focal_length = None
            operator = "-"

        else:
            raise ValueError

        label_total = 0

        for character in label:
            label_total += ord(character)

            label_total *= 17

            label_total %= 256

        if operator == "=":
            found = False
            for index, box in enumerate(boxes[label_total]):
                if label in box:
                    found = True
                    boxes[label_total][index] = f"{label} {focal_length}"
                    break

            if not found:
                boxes[label_total].append(f"{label} {focal_length}")

        if operator == "-":
            found_boxes: list[str] = []

            for box in boxes[label_total]:
                if f"{label} " in box:
                    found_boxes.append(box)

            if len(found_boxes) > 1:
                raise ValueError

            for found_box in found_boxes:
                boxes[label_total].remove(found_box)

    total = 0

    for box_index, box in enumerate(boxes):
        if box:
            for lens_index, lens in enumerate(box):
                focal_length = int(lens.split(" ")[1])

                total += (box_index + 1) * (lens_index + 1) * focal_length

    return total
