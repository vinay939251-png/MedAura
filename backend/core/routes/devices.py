"""
Device Routes — Fleet / device management.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_devices():
    """List all registered devices."""
    return {"devices": [], "total": 0}


@router.post("/")
async def register_device():
    """Register a new device."""
    return {"message": "Device registration — to be implemented in Phase 2"}
