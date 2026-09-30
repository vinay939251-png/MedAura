"""
Module Registration Model — Tracks registered detection modules in the DB.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy.types import JSON as JSONB

from core.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(String(64), primary_key=True)  # e.g., 'roadscan_ai'
    name = Column(String(128), nullable=False)
    version = Column(String(32), nullable=False)
    status = Column(String(16), nullable=False, default="active")  # active|disabled|error
    config = Column(JSONB, nullable=True, default=dict)
    registered_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Module {self.id} v{self.version} [{self.status}]>"
