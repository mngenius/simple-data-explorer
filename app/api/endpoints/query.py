"""Query API endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any
from app.models.schemas import QueryRequest, QueryResponse, DatasetInfo
from app.services.query_service import query_service
from app.utils.logging import logger


router = APIRouter(prefix="/query", tags=["query"])


@router.post("/execute", response_model=QueryResponse)
async def execute_query(query_request: QueryRequest):
    """
    Execute a query against a dataset.
    
    This endpoint allows you to query Parquet datasets with filtering,
    joining, aggregation, and sorting capabilities.
    
    **Features:**
    - Column selection
    - Filtering with various operators
    - Aggregation (COUNT, SUM, AVG, MIN, MAX)
    - Grouping and sorting
    - Result pagination
    - Automatic caching for performance
    
    **Example:**
    ```json
    {
        "dataset": "sales_data",
        "columns": ["product", "revenue"],
        "filters": [
            {
                "column": "region",
                "operator": "=",
                "value": "North"
            }
        ],
        "limit": 100
    }
    ```
    """
    try:
        logger.info(f"Executing query on dataset: {query_request.dataset}")
        response = await query_service.execute_query(query_request)
        return response
    except FileNotFoundError as e:
        logger.error(f"Dataset not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        logger.error(f"Invalid query: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query execution failed: {str(e)}"
        )


@router.get("/datasets", response_model=List[Dict[str, str]])
async def list_datasets():
    """
    List all available datasets.
    
    Returns a list of datasets available for querying.
    """
    try:
        datasets = await query_service.list_datasets()
        return datasets
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list datasets: {str(e)}"
        )


@router.get("/datasets/{dataset}", response_model=DatasetInfo)
async def get_dataset_info(dataset: str):
    """
    Get detailed information about a dataset.
    
    Returns schema, row count, and other metadata about the dataset.
    
    **Parameters:**
    - **dataset**: Name or path of the dataset
    """
    try:
        info = await query_service.get_dataset_info(dataset)
        return DatasetInfo(
            name=dataset,
            path=info['path'],
            size_bytes=info['size_bytes'],
            row_count=info['row_count'],
            column_count=info['column_count'],
            columns=info['columns']
        )
    except FileNotFoundError as e:
        logger.error(f"Dataset not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting dataset info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dataset info: {str(e)}"
        )
