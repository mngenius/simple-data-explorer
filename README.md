# Simple Data Explorer

A multi-layered application architecture for querying Parquet data with high-performance, caching, and scalable design.

## 🚀 Features

- **Fast Query Execution**: Powered by DuckDB for high-performance SQL queries on Parquet files
- **Flexible Querying**: Support for filtering, aggregation, sorting, and pagination
- **Caching Layer**: Redis-based caching for improved query performance
- **REST API**: Well-documented FastAPI endpoints with automatic OpenAPI documentation
- **Scalable Architecture**: Designed for horizontal scaling with Docker/Kubernetes
- **Security**: JWT-based authentication (ready for implementation)
- **Monitoring**: Prometheus metrics support
- **Production Ready**: Docker and Docker Compose support

## 📋 Architecture

### Multi-Layered Design

```
┌─────────────────────────────────────────────┐
│           API Layer (FastAPI)               │
│  - REST Endpoints                           │
│  - Request Validation                       │
│  - Authentication/Authorization             │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         Service Layer                       │
│  - Query Service                            │
│  - Cache Service                            │
│  - Business Logic                           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│      Query Engine Layer (DuckDB)            │
│  - SQL Query Execution                      │
│  - Parquet File Reading                     │
│  - Query Optimization                       │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│          Data Layer                         │
│  - Parquet Files                            │
│  - HDFS/S3 (Configurable)                   │
│  - Metadata Management                      │
└─────────────────────────────────────────────┘
```

### Technology Stack

- **API Framework**: FastAPI
- **Query Engine**: DuckDB (with support for Spark/Trino)
- **Caching**: Redis
- **Data Format**: Apache Parquet
- **Containerization**: Docker, Docker Compose
- **Monitoring**: Prometheus
- **Documentation**: OpenAPI/Swagger

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- Redis (optional, for caching)
- Docker and Docker Compose (optional)

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/mngenius/simple-data-explorer.git
cd simple-data-explorer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment configuration:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Create sample data:
```bash
python scripts/create_sample_data.py
```

6. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

### Docker Installation

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

This will start:
- API service on port 8000
- Redis cache on port 6379

## 📖 Usage

### API Documentation

Once the application is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Quick Start Examples

#### 1. Check Health
```bash
curl http://localhost:8000/health
```

#### 2. List Available Datasets
```bash
curl http://localhost:8000/api/v1/query/datasets
```

#### 3. Get Dataset Information
```bash
curl http://localhost:8000/api/v1/query/datasets/sales_data
```

#### 4. Execute a Simple Query
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "columns": ["product", "region", "revenue"],
    "limit": 10
  }'
```

#### 5. Query with Filters
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "columns": ["product", "region", "revenue"],
    "filters": [
      {"column": "region", "operator": "=", "value": "North"},
      {"column": "revenue", "operator": ">", "value": 1000}
    ],
    "order_by": [{"column": "revenue", "direction": "DESC"}],
    "limit": 10
  }'
```

#### 6. Aggregated Query
```bash
curl -X POST http://localhost:8000/api/v1/query/execute \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "sales_data",
    "columns": ["region"],
    "aggregates": [
      {"function": "sum", "column": "revenue", "alias": "total_revenue"},
      {"function": "avg", "column": "quantity", "alias": "avg_quantity"}
    ],
    "group_by": ["region"],
    "order_by": [{"column": "total_revenue", "direction": "DESC"}]
  }'
```

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Execute a query
query = {
    "dataset": "sales_data",
    "columns": ["product", "region", "revenue"],
    "filters": [
        {"column": "region", "operator": "=", "value": "North"}
    ],
    "limit": 100
}

response = requests.post(f"{BASE_URL}/query/execute", json=query)
result = response.json()

print(f"Found {result['row_count']} rows")
print(f"Execution time: {result['execution_time']:.3f}s")
print(f"Cached: {result['cached']}")
```

Run the example script:
```bash
python scripts/example_usage.py
```

## 🔧 Configuration

Configuration is managed through environment variables. See `.env.example` for all options:

### Key Configuration Options

- `QUERY_ENGINE`: Query engine to use (duckdb, spark, trino)
- `ENABLE_CACHE`: Enable Redis caching (true/false)
- `REDIS_HOST`: Redis server hostname
- `DATA_DIR`: Directory for Parquet files
- `MAX_RESULT_ROWS`: Maximum rows per query result
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_query.py
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build image
docker build -t data-explorer:latest .

# Run container
docker run -p 8000:8000 \
  -e REDIS_HOST=redis \
  -e ENABLE_CACHE=true \
  -v $(pwd)/data:/app/data \
  data-explorer:latest
```

### Kubernetes Deployment

Example Kubernetes manifests are available in the `docs/kubernetes/` directory (to be added).

### CDH/HDFS Integration

To integrate with Cloudera Data Hub:

1. Update configuration:
```bash
HDFS_URL=hdfs://your-hdfs-cluster:9000
HIVE_METASTORE_URI=thrift://your-metastore:9083
```

2. Configure Kerberos authentication if required
3. Mount Hadoop configuration files

## 📊 Query Features

### Supported Operations

- **Selection**: Choose specific columns
- **Filtering**: Apply conditions with operators: =, !=, >, <, >=, <=, IN, LIKE
- **Aggregation**: COUNT, SUM, AVG, MIN, MAX
- **Grouping**: GROUP BY multiple columns
- **Sorting**: ORDER BY with ASC/DESC
- **Pagination**: LIMIT and OFFSET

### Filter Examples

```json
// Equality
{"column": "region", "operator": "=", "value": "North"}

// Comparison
{"column": "revenue", "operator": ">", "value": 1000}

// IN clause
{"column": "product", "operator": "IN", "value": ["Laptop", "Phone"]}

// LIKE clause
{"column": "customer_name", "operator": "LIKE", "value": "John%"}
```

## 🔐 Security

### Authentication (Planned)

JWT-based authentication is supported. To enable:

1. Set `SECRET_KEY` in environment
2. Implement token generation endpoint
3. Use `Authorization: Bearer <token>` header

### Best Practices

- Use HTTPS in production
- Implement rate limiting
- Use Kerberos for HDFS access
- Enable Apache Ranger for authorization
- Validate all user inputs
- Implement API keys or OAuth2

## 📈 Performance Optimization

### Caching Strategy

- Query results are cached in Redis
- Cache key is generated from query parameters
- Default TTL: 1 hour (configurable)
- Automatic cache invalidation on data updates

### Query Optimization

- Use columnar format advantages of Parquet
- Partition data by frequently queried fields
- Use predicate pushdown
- Limit result sizes
- Use indexes when available

### Scaling

- Horizontal scaling with load balancer
- Separate read replicas for queries
- Use Kubernetes for auto-scaling
- Implement query queue for resource management

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: http://localhost:8000/docs
- **Issues**: https://github.com/mngenius/simple-data-explorer/issues
- **Discussions**: https://github.com/mngenius/simple-data-explorer/discussions

## 🗺️ Roadmap

- [ ] Join operations between datasets
- [ ] Real-time streaming query support
- [ ] Apache Spark integration
- [ ] Trino/Presto integration
- [ ] GraphQL API support
- [ ] Advanced security features
- [ ] Query builder UI
- [ ] Data visualization dashboard
- [ ] Query history and saved queries
- [ ] Materialized views
- [ ] Data lineage tracking

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DuckDB Documentation](https://duckdb.org/)
- [Apache Parquet Documentation](https://parquet.apache.org/)
- [Redis Documentation](https://redis.io/docs/)

---

Built with ❤️ for efficient data exploration