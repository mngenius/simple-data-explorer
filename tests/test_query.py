"""Test query endpoints."""
from fastapi.testclient import TestClient
import pytest


def test_list_datasets(client: TestClient):
    """Test listing datasets."""
    response = client.get("/api/v1/query/datasets")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_query_execution_validation(client: TestClient):
    """Test query execution with invalid dataset."""
    query = {
        "dataset": "nonexistent_dataset",
        "columns": ["col1"],
        "limit": 10
    }
    
    response = client.post("/api/v1/query/execute", json=query)
    assert response.status_code == 400  # Validation error for dataset not found


def test_query_request_validation(client: TestClient):
    """Test query request validation."""
    # Missing required field
    query = {
        "columns": ["col1"],
        "limit": 10
    }
    
    response = client.post("/api/v1/query/execute", json=query)
    assert response.status_code == 422  # Validation error
