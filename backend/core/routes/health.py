"""
Health Check Routes — Platform and module health endpoints.
"""

from fastapi import APIRouter

from config import settings
from core.module_registry import module_registry

router = APIRouter()


@router.get("/health")
async def platform_health():
    """Platform-wide health check."""
    module_health = await module_registry.get_all_health()

    return {
        "status": "healthy",
        "platform": settings.app_name,
        "environment": settings.app_env,
        "modules": module_health,
        "database": "connected",  # TODO: actual DB ping
    }
