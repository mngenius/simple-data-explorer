"""Test models and schemas."""
from app.models.schemas import QueryRequest, FilterCondition, AggregateOperation
import pytest


def test_query_request_basic():
    """Test basic query request creation."""
    query = QueryRequest(
        dataset="test_data",
        columns=["col1", "col2"],
        limit=100
    )
    
    assert query.dataset == "test_data"
    assert query.columns == ["col1", "col2"]
    assert query.limit == 100


def test_query_request_with_filters():
    """Test query request with filters."""
    query = QueryRequest(
        dataset="test_data",
        filters=[
            FilterCondition(column="col1", operator="=", value="test")
        ]
    )
    
    assert len(query.filters) == 1
    assert query.filters[0].column == "col1"


def test_query_request_with_aggregates():
    """Test query request with aggregates."""
    query = QueryRequest(
        dataset="test_data",
        aggregates=[
            AggregateOperation(function="sum", column="revenue", alias="total")
        ],
        group_by=["region"]
    )
    
    assert len(query.aggregates) == 1
    assert query.aggregates[0].function == "sum"
    assert query.group_by == ["region"]
