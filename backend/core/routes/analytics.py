"""
Analytics Routes — Platform-wide analytics and summaries.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.database import get_db
from core.models.incident import Incident
from core.models.session import DetectionSession
from core.models.device import Device

router = APIRouter()


@router.get("/summary")
async def platform_summary(db: AsyncSession = Depends(get_db)):
    """Get platform-wide analytics summary from DB."""
    # Total incidents
    total_incidents = (await db.execute(select(func.count(Incident.id)))).scalar()
    
    # Active sessions
    active_sessions = (await db.execute(
        select(func.count(DetectionSession.id)).where(DetectionSession.status == "active")
    )).scalar()
    
    # Active devices
    active_devices = (await db.execute(
        select(func.count(Device.id)).where(Device.is_active == True)
    )).scalar()
    
    # Incidents by module
    module_res = await db.execute(
        select(Incident.module_id, func.count(Incident.id)).group_by(Incident.module_id)
    )
    incidents_by_module = {row[0]: row[1] for row in module_res.all()}
    
    # Incidents by severity
    severity_res = await db.execute(
        select(Incident.severity, func.count(Incident.id)).group_by(Incident.severity)
    )
    incidents_by_severity = {row[0]: row[1] for row in severity_res.all()}

    return {
        "total_incidents": total_incidents,
        "active_sessions": active_sessions,
        "active_devices": active_devices,
        "incidents_by_module": incidents_by_module,
        "incidents_by_severity": incidents_by_severity,
    }

