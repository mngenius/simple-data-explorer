"""API router configuration."""
from fastapi import APIRouter
from app.api.endpoints import query

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(query.router)
