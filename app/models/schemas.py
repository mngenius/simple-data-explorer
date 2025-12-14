"""Data models for the application."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class QueryOperation(str, Enum):
    """Supported query operations."""
    SELECT = "select"
    FILTER = "filter"
    JOIN = "join"
    AGGREGATE = "aggregate"


class JoinType(str, Enum):
    """Supported join types."""
    INNER = "inner"
    LEFT = "left"
    RIGHT = "right"
    OUTER = "outer"


class AggregateFunction(str, Enum):
    """Supported aggregate functions."""
    COUNT = "count"
    SUM = "sum"
    AVG = "avg"
    MIN = "min"
    MAX = "max"


class FilterCondition(BaseModel):
    """Filter condition model."""
    column: str = Field(..., description="Column name to filter on")
    operator: str = Field(..., description="Operator: =, !=, >, <, >=, <=, in, like")
    value: Any = Field(..., description="Value to compare against")


class JoinCondition(BaseModel):
    """Join condition model."""
    left_column: str = Field(..., description="Column name from left table")
    right_column: str = Field(..., description="Column name from right table")
    join_type: JoinType = Field(default=JoinType.INNER, description="Type of join")


class AggregateOperation(BaseModel):
    """Aggregate operation model."""
    function: AggregateFunction = Field(..., description="Aggregate function")
    column: str = Field(..., description="Column to aggregate")
    alias: Optional[str] = Field(None, description="Alias for result column")


class QueryRequest(BaseModel):
    """Query request model."""
    dataset: str = Field(..., description="Name or path of the dataset (Parquet file)")
    columns: Optional[List[str]] = Field(None, description="Columns to select (None = all)")
    filters: Optional[List[FilterCondition]] = Field(None, description="Filter conditions")
    joins: Optional[List[Dict[str, Any]]] = Field(None, description="Join operations")
    aggregates: Optional[List[AggregateOperation]] = Field(None, description="Aggregate operations")
    group_by: Optional[List[str]] = Field(None, description="Columns to group by")
    order_by: Optional[List[Dict[str, str]]] = Field(None, description="Order by columns")
    limit: Optional[int] = Field(None, description="Maximum number of rows to return")
    offset: Optional[int] = Field(0, description="Number of rows to skip")


class QueryResponse(BaseModel):
    """Query response model."""
    success: bool = Field(..., description="Whether query was successful")
    data: List[Dict[str, Any]] = Field(..., description="Query results")
    row_count: int = Field(..., description="Number of rows returned")
    total_count: Optional[int] = Field(None, description="Total rows available")
    execution_time: float = Field(..., description="Query execution time in seconds")
    cached: bool = Field(default=False, description="Whether result was cached")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class DatasetInfo(BaseModel):
    """Dataset information model."""
    name: str = Field(..., description="Dataset name")
    path: str = Field(..., description="Dataset path")
    size_bytes: int = Field(..., description="File size in bytes")
    row_count: Optional[int] = Field(None, description="Number of rows")
    column_count: int = Field(..., description="Number of columns")
    columns: List[Dict[str, str]] = Field(..., description="Column names and types")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    modified_at: Optional[datetime] = Field(None, description="Last modified timestamp")


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error type")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    uptime: float = Field(..., description="Uptime in seconds")
    cache_connected: bool = Field(..., description="Redis cache connection status")
    query_engine: str = Field(..., description="Active query engine")
