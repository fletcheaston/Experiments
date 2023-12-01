import pytest
from app import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(
        app=app,
        base_url="http://testserver/experiments/advent-of-code-2023",
    )
