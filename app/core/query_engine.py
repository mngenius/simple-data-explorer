"""Base query engine interface."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
from app.models.schemas import QueryRequest


class BaseQueryEngine(ABC):
    """Abstract base class for query engines."""
    
    @abstractmethod
    def execute_query(self, query_request: QueryRequest) -> pd.DataFrame:
        """
        Execute a query and return results as a DataFrame.
        
        Args:
            query_request: Query request object
            
        Returns:
            DataFrame with query results
        """
        pass
    
    @abstractmethod
    def get_dataset_info(self, dataset_path: str) -> Dict[str, Any]:
        """
        Get information about a dataset.
        
        Args:
            dataset_path: Path to the dataset
            
        Returns:
            Dictionary with dataset information
        """
        pass
    
    @abstractmethod
    def validate_query(self, query_request: QueryRequest) -> bool:
        """
        Validate a query request.
        
        Args:
            query_request: Query request to validate
            
        Returns:
            True if valid, raises exception otherwise
        """
        pass
