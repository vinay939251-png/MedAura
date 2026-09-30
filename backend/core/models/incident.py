"""
Incident Model — The shared incident table.

All detection modules write to this single table using `module_id` as
a discriminator and `module_data` (JSONB) for module-specific fields.
This avoids table-per-module sprawl while keeping cross-module queries simple.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.types import Uuid as UUID, JSON as JSONB
from sqlalchemy.orm import relationship

from core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("detection_sessions.id"), nullable=True)

    # ── Module Identification ──
    module_id = Column(String(64), nullable=False, index=True)  # e.g., 'roadscan_ai'
    incident_type = Column(String(64), nullable=False, index=True)  # e.g., 'pothole'

    # ── Detection Data ──
    confidence = Column(Float, nullable=False)
    severity = Column(String(16), nullable=False, default="medium")  # low|medium|high|critical
    tracking_id = Column(Integer, nullable=True)

    # ── Location ──
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    gps_accuracy = Column(Float, nullable=True)
    # PostGIS geometry column can be added when PostGIS is enabled:
    # location = Column(Geometry("POINT", srid=4326), nullable=True)

    # ── Bounding Box ──
    bounding_box = Column(JSONB, nullable=True)  # {"x": .., "y": .., "w": .., "h": ..}

    # ── Model Info ──
    model_version = Column(String(64), nullable=True)
    runtime_mode = Column(String(16), nullable=True)  # edge | server

    # ── Status ──
    status = Column(String(32), nullable=False, default="detected")
    # detected | confirmed | resolved | false_positive

    # ── Module-Specific Data ──
    # This JSONB column stores any extra fields specific to the module.
    # For ROADSCAN AI: pothole_area_px, road_surface_type, etc.
    module_data = Column(JSONB, nullable=True, default=dict)

    # ── Timestamps ──
    detected_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    # ── Relationships ──
    session = relationship("DetectionSession", back_populates="incidents")

    # ── Indexes for common queries ──
    __table_args__ = (
        Index("ix_incidents_module_type", "module_id", "incident_type"),
        Index("ix_incidents_location", "latitude", "longitude"),
        Index("ix_incidents_detected_at", "detected_at"),
        Index("ix_incidents_status", "status"),
    )

    def __repr__(self):
        return f"<Incident {self.id} [{self.module_id}:{self.incident_type}] conf={self.confidence:.2f}>"
