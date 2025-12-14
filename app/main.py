"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from config.settings import settings
from app.api.router import api_router
from app.utils.logging import logger


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="""
        Multi-layered Data Explorer API for querying Parquet datasets.
        
        ## Features
        
        * **Query Execution**: Execute SQL-like queries on Parquet files
        * **Filtering**: Apply complex filter conditions
        * **Aggregation**: Perform aggregations (COUNT, SUM, AVG, MIN, MAX)
        * **Joins**: Join multiple datasets (planned)
        * **Caching**: Automatic result caching with Redis
        * **Performance**: Optimized for fast query execution
        
        ## Architecture
        
        - **API Layer**: FastAPI-based REST endpoints
        - **Query Engine**: DuckDB for high-performance querying
        - **Caching Layer**: Redis for result caching
        - **Data Layer**: Parquet file storage with HDFS support (planned)
        
        ## Usage
        
        1. Upload or configure Parquet datasets
        2. Use `/api/v1/query/execute` to run queries
        3. Check `/api/v1/query/datasets` for available datasets
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include health check at root level
    from app.api.endpoints import health
    app.include_router(health.router)
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    # Prometheus metrics endpoint (if enabled)
    if settings.ENABLE_METRICS:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)
    
    @app.on_event("startup")
    async def startup_event():
        """Application startup event."""
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"Query Engine: {settings.QUERY_ENGINE}")
        logger.info(f"Cache Enabled: {settings.ENABLE_CACHE}")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Application shutdown event."""
        logger.info("Shutting down application")
        # Close connections
        from app.services.cache import cache_service
        cache_service.close()
    
    return app


app = create_application()
