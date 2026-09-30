"""
Detection Session Model — Tracks active scanning sessions.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.types import Uuid as UUID, JSON as JSONB
from sqlalchemy.orm import relationship

from core.database import Base


class DetectionSession(Base):
    __tablename__ = "detection_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=True)

    # ── Session Info ──
    status = Column(String(16), nullable=False, default="active")  # active|paused|completed
    runtime_mode = Column(String(16), nullable=False, default="edge")  # edge|server
    module_id = Column(String(64), nullable=True)  # Which module is active

    # ── Metadata ──
    metadata_ = Column("metadata", JSONB, nullable=True, default=dict)

    # ── Timestamps ──
    started_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # ── Relationships ──
    device = relationship("Device", back_populates="sessions")
    incidents = relationship("Incident", back_populates="session", lazy="dynamic")

    def __repr__(self):
        return f"<DetectionSession {self.id} status={self.status}>"
