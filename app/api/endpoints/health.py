"""Health check and monitoring endpoints."""
from fastapi import APIRouter
import time
from app.models.schemas import HealthResponse
from app.services.cache import cache_service
from config.settings import settings


router = APIRouter(tags=["health"])

# Track application start time
START_TIME = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the application and its dependencies.
    """
    uptime = time.time() - START_TIME
    
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        uptime=uptime,
        cache_connected=cache_service.is_connected(),
        query_engine=settings.QUERY_ENGINE
    )


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }
