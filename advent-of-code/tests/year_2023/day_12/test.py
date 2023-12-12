# from pathlib import Path

import pytest

from src.year_2023.day_12 import arrangements

# from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "springs,counts,output",
    [
        # ("#", (1,), 1),
        # ("#.", (1,), 1),
        # (".#", (1,), 1),
        # ("?#", (1,), 1),
        # ("#?", (1,), 1),
        # ("??", (1,), 2),
        # ("???", (1,), 3),
        # ("?.?", (1,), 2),
        # ("?.??", (1, 2,), 1),
        # ("??.??", (1, 2,), 2),
        # ("???.???", (1, 1,), 11),
        # ("???.###", (1, 3,), 3),
        # ("?.?.###", (1, 3,), 2),
        # ("???.#", (3, 1,), 1),
        # ("???.###", (1, 1, 3,), 1),
        (
            "???.###",
            (
                2,
                3,
            ),
            2,
        ),
        # (".??..??...?##.", (1, 1, 3,), 4),
        # ("?#?#?#?#?#?#?#?", (1, 3, 1, 6,), 1),
        # ("????.#...#...", (4, 1, 1,), 1),
        # ("????.######..#####.", (1, 6, 5,), 4),
        # ("?###????????", (3, 2, 1,), 10),
        # (".###...?????", (3, 2, 1,), 3),
        # (".??.?.????", (1, 1, 1,), 17),
        # ("???#???????##?", (1, 7, 3,), 4),
        # ("?#.???#???????##?.?", (2, 1, 7, 3, 1,), 4),
    ],
)
def test_arrangements(springs: str, counts: tuple[int], output: int) -> None:
    assert len(arrangements(springs, counts)) == output


# @pytest.mark.parametrize(
#     "filename,output",
#     [
#         ("example.txt", 21),
#         ("input.txt", 0),
#     ],
# )
# def test_part_1(
#     filename: str,
#     output: int,
#     test_client: TestClient,
# ) -> None:
#     with open(Path(__file__).with_name(filename), "r") as file:
#         response = test_client.post(
#             "2023/day-12/part-1",
#             json={
#                 "document": file.read().splitlines(),
#             },
#         )
#
#         assert response.status_code == 200
#         assert response.json() == output
#
#
# @pytest.mark.parametrize(
#     "filename,output",
#     [
#         ("example.txt", 0),
#         # ("input.txt", 0),
#     ],
# )
# def test_part_2(
#     filename: str,
#     output: int,
#     test_client: TestClient,
# ) -> None:
#     with open(Path(__file__).with_name(filename), "r") as file:
#         response = test_client.post(
#             "2023/day-12/part-2",
#             json={
#                 "document": file.read().splitlines(),
#             },
#         )
#
#         assert response.status_code == 200
#         assert response.json() == output
