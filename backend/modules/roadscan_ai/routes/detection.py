"""
ROADSCAN AI — Detection Routes

Endpoints for:
- Submitting detection results from edge inference
- Getting detection configuration
- Model information
"""

from fastapi import APIRouter
from modules.roadscan_ai.config import ROADSCAN_CONFIG, ROADSCAN_CONFIG_SCHEMA

router = APIRouter()


@router.get("/config")
async def get_config():
    """Get current ROADSCAN AI detection configuration."""
    return {
        "module": "roadscan_ai",
        "config": ROADSCAN_CONFIG,
    }


@router.put("/config")
async def update_config(updates: dict):
    """Update ROADSCAN AI detection configuration."""
    # TODO: Validate against schema and persist
    valid_keys = set(ROADSCAN_CONFIG.keys())
    applied = {}
    for key, value in updates.items():
        if key in valid_keys:
            ROADSCAN_CONFIG[key] = value
            applied[key] = value

    return {
        "message": "Configuration updated",
        "applied": applied,
    }


@router.get("/model/info")
async def model_info():
    """Get information about the currently loaded model."""
    # TODO: Connect to actual runtime in Phase 2
    return {
        "module": "roadscan_ai",
        "model": {
            "status": "not_loaded",
            "message": "Model loading will be implemented in Phase 2. Place best.pt in /models/ directory.",
        },
    }


@router.get("/schema")
async def get_config_schema():
    """Get the configuration schema (for admin UI form generation)."""
    return {
        "module": "roadscan_ai",
        "schema": ROADSCAN_CONFIG_SCHEMA,
    }
