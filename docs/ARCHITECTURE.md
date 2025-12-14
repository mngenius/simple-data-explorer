# Architecture Documentation

## Overview

Simple Data Explorer is built with a multi-layered architecture designed for high performance, scalability, and maintainability when querying Parquet data.

## Architecture Layers

### 1. API Layer (Presentation)

**Technology**: FastAPI

**Responsibilities**:
- Expose REST endpoints
- Request/response validation with Pydantic
- API documentation (OpenAPI/Swagger)
- Authentication and authorization
- Error handling and logging

**Components**:
- `app/api/endpoints/`: API endpoint handlers
- `app/api/dependencies/`: Dependency injection for auth, etc.
- `app/api/router.py`: Route configuration

### 2. Service Layer (Business Logic)

**Responsibilities**:
- Implement business logic
- Coordinate between API and core layers
- Handle caching logic
- Validate business rules

**Components**:
- `app/services/query_service.py`: Query orchestration
- `app/services/cache.py`: Cache management

### 3. Core Layer (Query Engine)

**Technology**: DuckDB (with support for Spark/Trino)

**Responsibilities**:
- Execute SQL queries on Parquet files
- Query optimization
- Data type handling
- Join operations
- Aggregations

**Components**:
- `app/core/query_engine.py`: Abstract base class
- `app/core/duckdb_engine.py`: DuckDB implementation

### 4. Data Layer

**Technology**: Apache Parquet

**Responsibilities**:
- Store data in columnar format
- Efficient compression
- Schema management
- Metadata storage

**Storage Options**:
- Local filesystem
- HDFS (Hadoop Distributed File System)
- S3/Azure Data Lake/GCS (cloud storage)

## Data Flow

```
Client Request
     │
     ├──> [API Layer] FastAPI Endpoint
     │         │
     │         ├──> Request Validation (Pydantic)
     │         │
     │         └──> [Service Layer] Query Service
     │                   │
     │                   ├──> Cache Check (Redis)
     │                   │         │
     │                   │         ├──> Cache Hit → Return Cached Result
     │                   │         │
     │                   │         └──> Cache Miss ↓
     │                   │
     │                   └──> [Core Layer] Query Engine
     │                             │
     │                             ├──> Build SQL Query
     │                             │
     │                             ├──> Execute on Parquet
     │                             │
     │                             └──> Return Results
     │                                   │
     │                                   ├──> Cache Results
     │                                   │
     │                                   └──> Format Response
     │
     └──> JSON Response to Client
```

## Component Interactions

### Query Execution Flow

1. **Request Reception**
   - FastAPI receives HTTP POST request
   - Pydantic validates request schema
   - Converts to QueryRequest model

2. **Service Processing**
   - QueryService receives validated request
   - Generates cache key from query parameters
   - Checks Redis cache for existing results

3. **Cache Hit Path**
   - If cached result found, return immediately
   - Update execution_time and cached flag
   - Skip query engine

4. **Cache Miss Path**
   - Forward to appropriate query engine
   - Execute query on Parquet files
   - Process results
   - Store in cache for future requests

5. **Response Formation**
   - Convert DataFrame to JSON-serializable format
   - Add metadata (execution time, row counts, etc.)
   - Return QueryResponse to client

## Technology Choices

### Why FastAPI?

- **Performance**: Built on Starlette and Pydantic
- **Async Support**: Native async/await
- **Documentation**: Automatic OpenAPI docs
- **Type Safety**: Full type hints support
- **Modern**: Python 3.9+ features

### Why DuckDB?

- **Performance**: Columnar storage engine optimized for analytics
- **Zero Setup**: Embedded database, no separate server
- **Parquet Native**: First-class Parquet support
- **SQL Compliant**: Standard SQL interface
- **Lightweight**: Minimal dependencies

### Why Redis?

- **Speed**: In-memory data structure store
- **Flexibility**: Multiple data structures
- **TTL Support**: Automatic expiration
- **Pub/Sub**: For future real-time features
- **Clustering**: Horizontal scalability

### Why Parquet?

- **Columnar**: Efficient for analytical queries
- **Compression**: Excellent compression ratios
- **Schema**: Self-describing with embedded metadata
- **Ecosystem**: Wide tool support (Spark, Hive, etc.)
- **Performance**: Predicate pushdown support

## Scalability Considerations

### Horizontal Scaling

```
                    Load Balancer
                          │
           ┌──────────────┼──────────────┐
           │              │              │
      API Instance   API Instance   API Instance
           │              │              │
           └──────────────┼──────────────┘
                          │
                   Redis Cluster
                          │
                   Shared Storage
                  (HDFS/S3/NFS)
```

### Vertical Scaling

- Increase memory for larger datasets
- More CPU cores for parallel query execution
- SSD storage for faster I/O

### Caching Strategy

- **L1 Cache**: Application memory (future)
- **L2 Cache**: Redis (current)
- **L3 Cache**: Materialized views (future)

## Performance Optimizations

### Query Optimization

1. **Predicate Pushdown**
   - Filters applied at Parquet level
   - Reduces data read from disk

2. **Column Pruning**
   - Only requested columns loaded
   - Leverages Parquet columnar format

3. **Partition Pruning**
   - Skip irrelevant partitions
   - Based on partition columns

4. **Query Result Caching**
   - Identical queries return cached results
   - Configurable TTL

### Data Layout Optimization

1. **Partitioning**
   - Partition by frequently filtered columns
   - Example: partition by date, region

2. **Sorting**
   - Sort by commonly filtered columns
   - Enables early termination

3. **Compression**
   - Use appropriate codec (Snappy, Gzip, etc.)
   - Balance compression ratio vs. speed

## Security Architecture

### Current Implementation

- Configuration-based security settings
- JWT token infrastructure (ready for use)
- Environment-based secrets

### Future Enhancements

- OAuth2 authentication
- Role-based access control (RBAC)
- Row-level security
- Column-level security
- Audit logging
- Rate limiting
- API key management

## Monitoring and Observability

### Metrics (Prometheus)

- Query execution time
- Cache hit rate
- Error rates
- Request throughput
- Resource utilization

### Logging

- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error stack traces

### Health Checks

- API availability
- Redis connectivity
- Query engine status
- Disk space monitoring

## Deployment Architecture

### Development

```
Developer Workstation
├── Python Application
├── Local Redis (optional)
└── Local Parquet Files
```

### Production (Docker)

```
Docker Host
├── API Container
│   ├── FastAPI Application
│   └── Gunicorn/Uvicorn
├── Redis Container
└── Data Volume
    └── Parquet Files
```

### Production (Kubernetes)

```
Kubernetes Cluster
├── Ingress Controller
├── API Deployment (3 replicas)
│   └── Pod
│       └── API Container
├── Redis StatefulSet
│   └── Persistent Volume
└── Parquet Data
    └── Persistent Volume / S3
```

## Future Enhancements

### Short Term

- [ ] Join operations
- [ ] Upload API for Parquet files
- [ ] Query history
- [ ] Saved queries

### Medium Term

- [ ] Apache Spark integration
- [ ] Trino/Presto integration
- [ ] GraphQL API
- [ ] Web UI for query building

### Long Term

- [ ] Real-time streaming queries
- [ ] Materialized views
- [ ] Data lineage tracking
- [ ] Advanced analytics functions
- [ ] ML model integration

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DuckDB Documentation](https://duckdb.org/)
- [Apache Parquet Format](https://parquet.apache.org/)
- [Redis Documentation](https://redis.io/docs/)
