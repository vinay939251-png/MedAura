"""
Module Routes — List and inspect registered detection modules.
"""

from fastapi import APIRouter, HTTPException

from core.module_registry import module_registry

router = APIRouter()


@router.get("")
@router.get("/")
async def list_modules():
    """List all registered modules with their metadata."""
    return {
        "modules": module_registry.get_all_manifests(),
        "total": len(module_registry.modules),
    }


@router.get("/{module_id}")
async def get_module(module_id: str):
    """Get detailed info for a specific module."""
    module = module_registry.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")

    manifests = module_registry.get_all_manifests()
    return manifests.get(module_id)


@router.get("/{module_id}/health")
async def module_health(module_id: str):
    """Get health status of a specific module."""
    module = module_registry.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"Module '{module_id}' not found")

    return await module.health_check()
