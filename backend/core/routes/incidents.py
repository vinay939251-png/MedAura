"""
Incident Routes — Cross-module incident queries and management.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from core.database import get_db
from core.models.incident import Incident
from core.schemas.incident import IncidentResponse, IncidentUpdate

router = APIRouter()


@router.get("/")
async def list_incidents(
    module_id: Optional[str] = Query(None),
    incident_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    Query incidents across ALL modules with filtering.
    This is the platform-wide incident view.
    """
    query = select(Incident)

    if module_id:
        query = query.where(Incident.module_id == module_id)
    if incident_type:
        query = query.where(Incident.incident_type == incident_type)
    if severity:
        query = query.where(Incident.severity == severity)
    if status:
        query = query.where(Incident.status == status)
    if min_confidence is not None:
        query = query.where(Incident.confidence >= min_confidence)

    # Count total
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
        "total_pages": (total + page_size - 1) // page_size if total else 0,
    }


@router.get("/{incident_id}")
async def get_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific incident by ID."""
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalar_one_or_none()

    if not incident:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Incident not found")

    return IncidentResponse.model_validate(incident)


@router.patch("/{incident_id}")
async def update_incident(
    incident_id: UUID,
    update: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update incident status or metadata."""
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalar_one_or_none()

    if not incident:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Incident not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(incident, key, value)

    await db.flush()
    return IncidentResponse.model_validate(incident)
