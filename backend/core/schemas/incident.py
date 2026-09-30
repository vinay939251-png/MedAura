"""
Incident Pydantic Schemas — for API request/response validation.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    """Schema for creating a new incident (from edge or server inference)."""
    session_id: Optional[UUID] = None
    module_id: str = Field(..., max_length=64)
    incident_type: str = Field(..., max_length=64)
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: str = Field("medium", pattern="^(low|medium|high|critical)$")
    tracking_id: Optional[int] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    gps_accuracy: Optional[float] = None
    bounding_box: Optional[Dict[str, float]] = None
    model_version: Optional[str] = None
    runtime_mode: Optional[str] = Field(None, pattern="^(edge|server)$")
    module_data: Optional[Dict[str, Any]] = None
    detected_at: Optional[datetime] = None


class IncidentUpdate(BaseModel):
    """Schema for updating incident status."""
    status: Optional[str] = Field(None, pattern="^(detected|confirmed|resolved|false_positive)$")
    severity: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    module_data: Optional[Dict[str, Any]] = None


class IncidentResponse(BaseModel):
    """Schema for incident API responses."""
    id: UUID
    session_id: Optional[UUID]
    module_id: str
    incident_type: str
    confidence: float
    severity: str
    tracking_id: Optional[int]
    latitude: float
    longitude: float
    gps_accuracy: Optional[float]
    bounding_box: Optional[Dict[str, float]]
    model_version: Optional[str]
    runtime_mode: Optional[str]
    status: str
    module_data: Optional[Dict[str, Any]]
    detected_at: datetime
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class IncidentFilter(BaseModel):
    """Schema for filtering incidents."""
    module_id: Optional[str] = None
    incident_type: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    min_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    # Spatial bounding box filter
    lat_min: Optional[float] = None
    lat_max: Optional[float] = None
    lng_min: Optional[float] = None
    lng_max: Optional[float] = None
    # Temporal filter
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
