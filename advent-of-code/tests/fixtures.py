import pytest
from app import PREFIX, app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(
        app=app,
        base_url=f"http://testserver/{PREFIX}",
    )
