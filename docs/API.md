# API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### Health Check

#### GET /health

Check the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime": 123.45,
  "cache_connected": true,
  "query_engine": "duckdb"
}
```

---

### Query Endpoints

#### POST /api/v1/query/execute

Execute a query on a Parquet dataset.

**Request Body:**
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
  "aggregates": [
    {
      "function": "sum",
      "column": "revenue",
      "alias": "total_revenue"
    }
  ],
  "group_by": ["product"],
  "order_by": [
    {
      "column": "total_revenue",
      "direction": "DESC"
    }
  ],
  "limit": 100,
  "offset": 0
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "product": "Laptop",
      "total_revenue": 150000.50
    },
    {
      "product": "Phone",
      "total_revenue": 125000.75
    }
  ],
  "row_count": 2,
  "total_count": 2,
  "execution_time": 0.123,
  "cached": false,
  "metadata": null
}
```

#### GET /api/v1/query/datasets

List all available datasets.

**Response:**
```json
[
  {
    "name": "sales_data",
    "path": "sample/sales_data.parquet",
    "full_path": "/app/data/sample/sales_data.parquet"
  },
  {
    "name": "customer_data",
    "path": "sample/customer_data.parquet",
    "full_path": "/app/data/sample/customer_data.parquet"
  }
]
```

#### GET /api/v1/query/datasets/{dataset}

Get detailed information about a specific dataset.

**Parameters:**
- `dataset` (path): Name of the dataset

**Response:**
```json
{
  "name": "sales_data",
  "path": "/app/data/sample/sales_data.parquet",
  "size_bytes": 12345678,
  "row_count": 1000,
  "column_count": 7,
  "columns": [
    {"name": "order_id", "type": "int64"},
    {"name": "product", "type": "object"},
    {"name": "region", "type": "object"},
    {"name": "revenue", "type": "float64"},
    {"name": "quantity", "type": "int64"},
    {"name": "customer_id", "type": "int64"},
    {"name": "order_date", "type": "datetime64[ns]"}
  ]
}
```

---

## Query Request Schema

### QueryRequest

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| dataset | string | Yes | Name or path of the dataset |
| columns | array[string] | No | Columns to select (null = all) |
| filters | array[FilterCondition] | No | Filter conditions |
| aggregates | array[AggregateOperation] | No | Aggregate operations |
| group_by | array[string] | No | Columns to group by |
| order_by | array[OrderBy] | No | Sorting specification |
| limit | integer | No | Maximum rows to return |
| offset | integer | No | Number of rows to skip |

### FilterCondition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| column | string | Yes | Column name |
| operator | string | Yes | Operator: =, !=, >, <, >=, <=, IN, LIKE |
| value | any | Yes | Value to compare |

### AggregateOperation

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| function | string | Yes | Function: count, sum, avg, min, max |
| column | string | Yes | Column to aggregate |
| alias | string | No | Alias for result column |

### OrderBy

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| column | string | Yes | Column name |
| direction | string | No | ASC or DESC (default: ASC) |

---

## Response Schema

### QueryResponse

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether query succeeded |
| data | array[object] | Query results |
| row_count | integer | Number of rows returned |
| total_count | integer | Total rows available |
| execution_time | float | Query time in seconds |
| cached | boolean | Whether from cache |
| metadata | object | Additional metadata |

---

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid query: operator 'INVALID' not supported"
}
```

### 404 Not Found
```json
{
  "detail": "Dataset not found: unknown_dataset"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Query execution failed: [error details]"
}
```

---

## Examples

### Simple Query
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "limit": 10
  }'
```

### Filtered Query
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "columns": ["product", "revenue"],
    "filters": [
      {"column": "region", "operator": "=", "value": "North"}
    ]
  }'
```

### Aggregated Query
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "columns": ["region"],
    "aggregates": [
      {"function": "sum", "column": "revenue", "alias": "total"}
    ],
    "group_by": ["region"]
  }'
```
