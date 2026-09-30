"""
Device Routes — Fleet / device management.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def list_devices():
    """List all registered devices."""
    return {"items": [], "total": 0}


@router.get("/{device_id}")
async def get_device(device_id: str):
    """Get a device."""
    raise HTTPException(status_code=404, detail="Device not found")


@router.post("/")
async def register_device():
    """Register a new device."""
    return {"message": "Device registration — to be implemented in Phase 2"}
