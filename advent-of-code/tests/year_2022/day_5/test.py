from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,stacks,message",
    [
        (
            "part-1.txt",
            {
                "1": ["N", "Z"],
                "2": ["D", "C", "M"],
                "3": ["P"],
            },
            "CMZ",
        ),
        (
            "input.txt",
            {
                "1": ["D", "H", "R", "Z", "S", "P", "W", "Q"],
                "2": ["F", "H", "Q", "W", "R", "B", "V"],
                "3": ["H", "S", "V", "C"],
                "4": ["G", "F", "H"],
                "5": ["Z", "B", "J", "G", "P"],
                "6": ["L", "F", "W", "H", "J", "T", "Q"],
                "7": ["N", "J", "V", "L", "D", "W", "T", "Z"],
                "8": ["F", "H", "G", "J", "C", "Z", "T", "D"],
                "9": ["H", "B", "M", "V", "P", "W"],
            },
            "ZWHVFWQWW",
        ),
    ],
)
def test_part_1(
    filename: str,
    stacks: dict[str, list[str]],
    message: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2022/day-5/part-1",
            json={
                "document": file.read().splitlines(),
                "stacks": stacks,
            },
        )

        assert response.status_code == 200
        assert response.json() == message


@pytest.mark.parametrize(
    "filename,stacks,message",
    [
        (
            "part-2.txt",
            {
                "1": ["N", "Z"],
                "2": ["D", "C", "M"],
                "3": ["P"],
            },
            "MCD",
        ),
        (
            "input.txt",
            {
                "1": ["D", "H", "R", "Z", "S", "P", "W", "Q"],
                "2": ["F", "H", "Q", "W", "R", "B", "V"],
                "3": ["H", "S", "V", "C"],
                "4": ["G", "F", "H"],
                "5": ["Z", "B", "J", "G", "P"],
                "6": ["L", "F", "W", "H", "J", "T", "Q"],
                "7": ["N", "J", "V", "L", "D", "W", "T", "Z"],
                "8": ["F", "H", "G", "J", "C", "Z", "T", "D"],
                "9": ["H", "B", "M", "V", "P", "W"],
            },
            "HZFZCCWWV",
        ),
    ],
)
def test_part_2(
    filename: str,
    stacks: dict[str, list[str]],
    message: str,
    test_client: TestClient,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        response = test_client.post(
            "2022/day-5/part-2",
            json={
                "document": file.read().splitlines(),
                "stacks": stacks,
            },
        )

        assert response.status_code == 200
        assert response.json() == message
