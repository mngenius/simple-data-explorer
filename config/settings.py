"""Configuration management for the data explorer application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "Simple Data Explorer"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Data Storage
    DATA_DIR: str = "./data"
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    ENABLE_CACHE: bool = True
    
    # Query Engine
    QUERY_ENGINE: str = "duckdb"  # Options: duckdb, spark, trino
    MAX_QUERY_TIME: int = 300  # 5 minutes
    MAX_RESULT_ROWS: int = 10000
    
    # Spark Configuration (if using Spark)
    SPARK_MASTER: Optional[str] = None
    SPARK_APP_NAME: str = "DataExplorer"
    
    # Trino Configuration (if using Trino)
    TRINO_HOST: Optional[str] = None
    TRINO_PORT: int = 8080
    TRINO_CATALOG: str = "hive"
    TRINO_SCHEMA: str = "default"
    
    # CDH/HDFS Configuration
    HDFS_URL: Optional[str] = None
    HIVE_METASTORE_URI: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
