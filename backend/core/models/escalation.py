from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID, uuid4

class EscalationRecord(BaseModel):
    """
    Tracks the lifecycle of an incident as it moves through authority levels.
    """
    id: UUID = Field(default_factory=uuid4)
    incident_id: UUID
    authority_id: str
    status: str = "reported" # reported, acknowledged, in_progress, resolved
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)

class EscalationCreate(BaseModel):
    incident_id: UUID
    authority_id: str
    notes: Optional[str] = None
