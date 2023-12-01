import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "filename,total",
    [
        ("0.txt", 142),
        ("1.txt", 54338),
    ],
)
def test_day_1(filename: str, total: int, test_client: TestClient) -> None:
    with open(f"tests/day_1/{filename}", "rb") as file:
        response = test_client.post(
            "day-1",
            files={"calibration_document": file},
        )

        assert response.status_code == 200
        assert response.json() == total
