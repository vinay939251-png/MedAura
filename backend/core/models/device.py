"""
Device Model — Tracks buses, patrol vehicles, drones, etc.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.types import Uuid as UUID, JSON as JSONB
from sqlalchemy.orm import relationship

from core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_name = Column(String(128), nullable=False)
    device_type = Column(String(32), nullable=False, default="bus")  # bus|patrol|drone
    identifier = Column(String(64), unique=True, nullable=False)  # License plate or serial
    is_active = Column(Boolean, nullable=False, default=True)
    metadata_ = Column("metadata", JSONB, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # ── Relationships ──
    sessions = relationship("DetectionSession", back_populates="device", lazy="dynamic")

    def __repr__(self):
        return f"<Device {self.device_name} [{self.identifier}]>"
