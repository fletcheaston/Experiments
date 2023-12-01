import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,total",
    [
        ("part-1.txt", 142),
        ("input.txt", 54338),
    ],
)
def test_day_1_part_1(filename: str, total: int, test_client: TestClient) -> None:
    with open(f"tests/day_1/{filename}", "rb") as file:
        response = test_client.post(
            "day-1/part-1",
            files={"calibration_document": file},
        )

        assert response.status_code == 200
        assert response.json() == total


@pytest.mark.parametrize(
    "filename,total",
    [
        ("part-2.txt", 281),
        ("input.txt", 53389),
    ],
)
def test_day_1_part_2(filename: str, total: int, test_client: TestClient) -> None:
    with open(f"tests/day_1/{filename}", "rb") as file:
        response = test_client.post(
            "day-1/part-2",
            files={"calibration_document": file},
        )

        assert response.status_code == 200
        assert response.json() == total
