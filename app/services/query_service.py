"""Query service for executing data queries."""
import time
from typing import Dict, Any, List
import pandas as pd
from app.models.schemas import QueryRequest, QueryResponse
from app.core.duckdb_engine import DuckDBQueryEngine
from app.services.cache import cache_service
from config.settings import settings


class QueryService:
    """Service for executing queries against datasets."""
    
    def __init__(self):
        """Initialize query service."""
        # Initialize query engine based on configuration
        if settings.QUERY_ENGINE == "duckdb":
            self.engine = DuckDBQueryEngine(data_dir=settings.DATA_DIR)
        else:
            # Fallback to DuckDB
            self.engine = DuckDBQueryEngine(data_dir=settings.DATA_DIR)
    
    async def execute_query(self, query_request: QueryRequest) -> QueryResponse:
        """
        Execute a query with caching support.
        
        Args:
            query_request: Query request object
            
        Returns:
            Query response with results
        """
        start_time = time.time()
        
        # Validate query
        self.engine.validate_query(query_request)
        
        # Check cache
        query_dict = query_request.model_dump()
        cached_result = cache_service.get(query_dict)
        
        if cached_result:
            cached_result['cached'] = True
            cached_result['execution_time'] = time.time() - start_time
            return QueryResponse(**cached_result)
        
        # Execute query
        try:
            df = self.engine.execute_query(query_request)
            
            # Convert to response format
            data = df.to_dict(orient='records')
            row_count = len(data)
            
            # Apply max result limit
            if row_count > settings.MAX_RESULT_ROWS:
                data = data[:settings.MAX_RESULT_ROWS]
                metadata = {
                    "warning": f"Results truncated to {settings.MAX_RESULT_ROWS} rows",
                    "total_rows": row_count
                }
            else:
                metadata = None
            
            execution_time = time.time() - start_time
            
            response_data = {
                'success': True,
                'data': data,
                'row_count': len(data),
                'total_count': row_count,
                'execution_time': execution_time,
                'cached': False,
                'metadata': metadata
            }
            
            # Cache the result
            cache_service.set(query_dict, response_data)
            
            return QueryResponse(**response_data)
            
        except Exception as e:
            execution_time = time.time() - start_time
            raise Exception(f"Query execution failed: {str(e)}")
    
    async def get_dataset_info(self, dataset: str) -> Dict[str, Any]:
        """Get information about a dataset."""
        return self.engine.get_dataset_info(dataset)
    
    async def list_datasets(self) -> List[Dict[str, str]]:
        """List available datasets."""
        import os
        from pathlib import Path
        
        datasets = []
        data_dir = Path(settings.DATA_DIR)
        
        # Search for parquet files
        for path in data_dir.rglob("*.parquet"):
            datasets.append({
                "name": path.stem,
                "path": str(path.relative_to(data_dir)),
                "full_path": str(path)
            })
        
        return datasets


# Global query service instance
query_service = QueryService()
