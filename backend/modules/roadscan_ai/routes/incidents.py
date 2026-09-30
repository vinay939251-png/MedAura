"""
ROADSCAN AI — Incident Routes

Module-specific incident endpoints for pothole incidents.
These supplement the cross-module /api/v1/incidents/ routes.
"""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.database import get_db
from core.models.incident import Incident
from core.schemas.incident import IncidentCreate, IncidentResponse
from core.websocket.hub import ws_manager

router = APIRouter()


@router.post("/incidents")
async def create_pothole_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new pothole incident.

    Called by the edge client after a detection is confirmed
    (tracked for N frames with sufficient confidence).
    """
    # Force module_id and incident_type for this module
    incident_data = incident.model_dump()
    incident_data["module_id"] = "roadscan_ai"
    incident_data["incident_type"] = incident_data.get("incident_type", "pothole")

    # TODO: Spatial + temporal deduplication (Phase 2)
    # Check if there's already an incident within X meters and Y seconds

    # Create the incident
    db_incident = Incident(**incident_data)
    db.add(db_incident)
    await db.flush()
    await db.refresh(db_incident)

    # Broadcast via WebSocket
    await ws_manager.broadcast_to_channel(
        "incidents:roadscan_ai",
        {
            "event": "incident.created",
            "module": "roadscan_ai",
            "data": IncidentResponse.model_validate(db_incident).model_dump(mode="json"),
        },
    )

    return IncidentResponse.model_validate(db_incident)


@router.get("/incidents")
async def list_pothole_incidents(
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List pothole incidents with filtering."""
    query = select(Incident).where(Incident.module_id == "roadscan_ai")

    if severity:
        query = query.where(Incident.severity == severity)
    if status:
        query = query.where(Incident.status == status)
    if min_confidence is not None:
        query = query.where(Incident.confidence >= min_confidence)

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Paginate
    query = query.order_by(Incident.detected_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    incidents = result.scalars().all()

    return {
        "items": [IncidentResponse.model_validate(i) for i in incidents],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/incidents/stats")
async def pothole_stats(db: AsyncSession = Depends(get_db)):
    """Get ROADSCAN AI incident statistics."""
    base = select(Incident).where(Incident.module_id == "roadscan_ai")

    total = (await db.execute(
        select(func.count()).select_from(base.subquery())
    )).scalar()

    # Severity breakdown
    severity_query = (
        select(Incident.severity, func.count())
        .where(Incident.module_id == "roadscan_ai")
        .group_by(Incident.severity)
    )
    severity_result = await db.execute(severity_query)
    severity_breakdown = {row[0]: row[1] for row in severity_result.all()}

    return {
        "module": "roadscan_ai",
        "total_incidents": total,
        "by_severity": severity_breakdown,
    }
