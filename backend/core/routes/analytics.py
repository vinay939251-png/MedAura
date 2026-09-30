"""
Analytics Routes — Platform-wide analytics and summaries.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def platform_summary():
    """Get platform-wide analytics summary."""
    # TODO: Query actual DB aggregates
    return {
        "total_incidents": 0,
        "active_sessions": 0,
        "active_devices": 0,
        "incidents_by_module": {},
        "incidents_by_severity": {},
    }
