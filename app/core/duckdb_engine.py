"""DuckDB query engine implementation."""
import duckdb
import pandas as pd
from typing import Dict, Any, List, Optional
import os
from pathlib import Path
from app.core.query_engine import BaseQueryEngine
from app.models.schemas import QueryRequest, FilterCondition


class DuckDBQueryEngine(BaseQueryEngine):
    """Query engine implementation using DuckDB."""
    
    def __init__(self, data_dir: str = "./data"):
        """Initialize DuckDB query engine."""
        self.data_dir = Path(data_dir)
        self.conn = duckdb.connect(database=':memory:')
        
    def execute_query(self, query_request: QueryRequest) -> pd.DataFrame:
        """Execute a query using DuckDB."""
        dataset_path = self._resolve_dataset_path(query_request.dataset)
        
        # Build SQL query
        sql_query = self._build_sql_query(query_request, dataset_path)
        
        # Execute query
        result = self.conn.execute(sql_query).fetchdf()
        
        return result
    
    def _resolve_dataset_path(self, dataset: str) -> str:
        """Resolve dataset name to full path."""
        if os.path.isabs(dataset):
            return dataset
        
        # Try with .parquet extension
        dataset_path = self.data_dir / dataset
        if not dataset_path.suffix:
            dataset_path = dataset_path.with_suffix('.parquet')
        
        if not dataset_path.exists():
            # Try in sample directory
            dataset_path = self.data_dir / 'sample' / dataset_path.name
        
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {dataset}")
        
        return str(dataset_path)
    
    def _build_sql_query(self, query_request: QueryRequest, dataset_path: str) -> str:
        """Build SQL query from request."""
        # Validate column names to prevent SQL injection
        def sanitize_identifier(identifier: str) -> str:
            """Sanitize SQL identifier (column name, table name, etc.)."""
            # Only allow alphanumeric characters, underscores, and dots
            import re
            if not re.match(r'^[a-zA-Z0-9_\.]+$', identifier):
                raise ValueError(f"Invalid identifier: {identifier}")
            return identifier
        
        # SELECT clause
        if query_request.columns:
            sanitized_columns = [sanitize_identifier(col) for col in query_request.columns]
            select_clause = ", ".join(sanitized_columns)
        else:
            select_clause = "*"
        
        # Add aggregates if present
        if query_request.aggregates:
            agg_parts = []
            for agg in query_request.aggregates:
                col = sanitize_identifier(agg.column)
                alias = sanitize_identifier(agg.alias or f"{agg.function}_{agg.column}")
                agg_parts.append(f"{agg.function.upper()}({col}) as {alias}")
            if agg_parts:
                if query_request.columns:
                    select_clause = f"{select_clause}, {', '.join(agg_parts)}"
                else:
                    select_clause = ', '.join(agg_parts)
        
        # FROM clause - use parameterized path
        from_clause = f"FROM read_parquet('{dataset_path}')"
        
        # WHERE clause
        where_clause = ""
        if query_request.filters:
            conditions = []
            for filter_cond in query_request.filters:
                condition = self._build_filter_condition(filter_cond)
                conditions.append(condition)
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
        
        # GROUP BY clause
        group_by_clause = ""
        if query_request.group_by:
            sanitized_groups = [sanitize_identifier(col) for col in query_request.group_by]
            group_by_clause = f"GROUP BY {', '.join(sanitized_groups)}"
        
        # ORDER BY clause
        order_by_clause = ""
        if query_request.order_by:
            order_parts = []
            for order in query_request.order_by:
                col = sanitize_identifier(order.get('column'))
                direction = order.get('direction', 'ASC').upper()
                if direction not in ('ASC', 'DESC'):
                    raise ValueError(f"Invalid order direction: {direction}")
                order_parts.append(f"{col} {direction}")
            order_by_clause = f"ORDER BY {', '.join(order_parts)}"
        
        # LIMIT and OFFSET
        limit_clause = ""
        if query_request.limit:
            limit_clause = f"LIMIT {int(query_request.limit)}"
            if query_request.offset:
                limit_clause += f" OFFSET {int(query_request.offset)}"
        
        # Combine all parts
        query_parts = [
            f"SELECT {select_clause}",
            from_clause,
            where_clause,
            group_by_clause,
            order_by_clause,
            limit_clause,
        ]
        
        sql_query = " ".join(part for part in query_parts if part)
        return sql_query
    
    def _build_filter_condition(self, filter_cond: FilterCondition) -> str:
        """Build SQL filter condition with proper escaping."""
        # Validate column name
        import re
        column = filter_cond.column
        if not re.match(r'^[a-zA-Z0-9_\.]+$', column):
            raise ValueError(f"Invalid column name: {column}")
        
        operator = filter_cond.operator.upper()
        value = filter_cond.value
        
        if operator == "IN":
            if isinstance(value, list):
                # Escape each value in the list
                escaped_values = []
                for v in value:
                    if isinstance(v, str):
                        # Escape single quotes by doubling them
                        escaped = v.replace("'", "''")
                        escaped_values.append(f"'{escaped}'")
                    elif isinstance(v, (int, float)):
                        escaped_values.append(str(v))
                    else:
                        raise ValueError(f"Unsupported value type in IN clause: {type(v)}")
                return f"{column} IN ({', '.join(escaped_values)})"
            else:
                raise ValueError("IN operator requires a list value")
        elif operator == "LIKE":
            # Escape single quotes in LIKE pattern
            escaped_value = str(value).replace("'", "''")
            return f"{column} LIKE '{escaped_value}'"
        else:
            # Handle standard operators: =, !=, >, <, >=, <=
            if operator not in ('=', '!=', '>', '<', '>=', '<='):
                raise ValueError(f"Invalid operator: {operator}")
            
            if isinstance(value, str):
                # Escape single quotes
                escaped_value = value.replace("'", "''")
                return f"{column} {operator} '{escaped_value}'"
            elif isinstance(value, (int, float, bool)):
                return f"{column} {operator} {value}"
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
    
    def get_dataset_info(self, dataset_path: str) -> Dict[str, Any]:
        """Get information about a dataset."""
        dataset_path = self._resolve_dataset_path(dataset_path)
        
        # Read schema and sample data
        query = f"SELECT * FROM read_parquet('{dataset_path}') LIMIT 1"
        df = self.conn.execute(query).fetchdf()
        
        # Get row count
        count_query = f"SELECT COUNT(*) as count FROM read_parquet('{dataset_path}')"
        row_count = self.conn.execute(count_query).fetchdf()['count'].iloc[0]
        
        # Get file size
        file_size = os.path.getsize(dataset_path)
        
        # Get column information
        columns = []
        for col_name, col_type in df.dtypes.items():
            columns.append({
                "name": col_name,
                "type": str(col_type)
            })
        
        return {
            "path": dataset_path,
            "size_bytes": file_size,
            "row_count": int(row_count),
            "column_count": len(columns),
            "columns": columns,
        }
    
    def validate_query(self, query_request: QueryRequest) -> bool:
        """Validate a query request."""
        # Check if dataset exists
        try:
            self._resolve_dataset_path(query_request.dataset)
        except FileNotFoundError as e:
            raise ValueError(f"Invalid dataset: {e}")
        
        # Validate filter operators
        if query_request.filters:
            valid_operators = ["=", "!=", ">", "<", ">=", "<=", "IN", "LIKE"]
            for filter_cond in query_request.filters:
                if filter_cond.operator.upper() not in valid_operators:
                    raise ValueError(f"Invalid operator: {filter_cond.operator}")
        
        return True
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
