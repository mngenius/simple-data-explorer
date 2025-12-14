"""Test configuration."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_query_request():
    """Sample query request for testing."""
    return {
        "dataset": "sales_data",
        "columns": ["product", "revenue"],
        "limit": 10
    }
