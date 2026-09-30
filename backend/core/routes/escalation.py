"""
Escalation Routes — Handles incident routing and accountability.
"""

from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from typing import List

from core.models.escalation import EscalationRecord, EscalationCreate

router = APIRouter()

# In-memory store for demo/hackathon purposes to avoid complex DB migrations mid-hackathon
# In a real app this would use the database session
MOCK_ESCALATIONS = {}

@router.post("/")
async def escalate_incident(escalation: EscalationCreate):
    """Escalate an incident to a specific road authority."""
    record = EscalationRecord(**escalation.model_dump())
    MOCK_ESCALATIONS[record.id] = record
    return {"message": "Incident escalated successfully", "record": record}

@router.get("/{incident_id}", response_model=List[EscalationRecord])
async def get_incident_escalations(incident_id: UUID):
    """Get the escalation history for a specific incident."""
    records = [r for r in MOCK_ESCALATIONS.values() if r.incident_id == incident_id]
    return records

@router.patch("/{escalation_id}/status")
async def update_escalation_status(escalation_id: UUID, status: str):
    """Update the status of an active escalation (e.g., to 'in_progress' or 'resolved')."""
    if escalation_id not in MOCK_ESCALATIONS:
        raise HTTPException(status_code=404, detail="Escalation record not found")
    
    valid_statuses = ["reported", "acknowledged", "in_progress", "resolved"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    import datetime
    record = MOCK_ESCALATIONS[escalation_id]
    record.status = status
    record.updated_at = datetime.datetime.now(datetime.timezone.utc)
    return {"message": "Status updated", "record": record}
