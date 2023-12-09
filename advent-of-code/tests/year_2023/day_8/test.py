from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,instructions,output",
    [
        ("part-1.txt", "RL", 2),
        ("part-1-2.txt", "LLR", 6),
        (
            "input.txt",
            "LLRLRLLRRLRLRLLRRLRRRLRRRLRRLRRLRLRLRRRLLRLRRLRLRRRLRLLRRLRLRLLRRRLLRLRRRLRLRRLRRLRLLRRLRRLRLRLRLLRLLRRLRRLRRLRRLRRLRLLRLRLRRRLRRRLRRLRLRLRRLRRRLRLRRRLRLRLRLRRRLRRLRRLRRRLLLLRRLRRLRLRRRLRLRRRLRRLLLLRLRLRRRLRRRLRLRRLLRLRLRRRLRLRLRRRLRLLRRRLRRLRLRLRRRLRLLRRLLRRRLRRRLRRRLRRLRLRLRRRLRRRLRRRLLRRRR",
            23147,
        ),
    ],
)
def test_part_1(
    filename: str, instructions: str, output: int, test_client: TestClient
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-8/part-1",
            json={
                "instructions": instructions,
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output


@pytest.mark.parametrize(
    "filename,instructions,output",
    [
        ("part-2.txt", "LR", 6),
        (
            "input.txt",
            "LLRLRLLRRLRLRLLRRLRRRLRRRLRRLRRLRLRLRRRLLRLRRLRLRRRLRLLRRLRLRLLRRRLLRLRRRLRLRRLRRLRLLRRLRRLRLRLRLLRLLRRLRRLRRLRRLRRLRLLRLRLRRRLRRRLRRLRLRLRRLRRRLRLRRRLRLRLRLRRRLRRLRRLRRRLLLLRRLRRLRLRRRLRLRRRLRRLLLLRLRLRRRLRRRLRLRRLLRLRLRRRLRLRLRRRLRLLRRRLRRLRLRLRRRLRLLRRLLRRRLRRRLRRRLRRLRLRLRRRLRRRLRRRLLRRRR",
            22289513667691,
        ),
    ],
)
def test_part_2(
    filename: str,
    instructions: str,
    output: int,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2023/day-8/part-2",
            json={
                "instructions": instructions,
                "document": file.read().splitlines(),
            },
        )

        assert response.status_code == 200
        assert response.json() == output
