from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RoadAuthority(BaseModel):
    """
    Represents a municipal or regional road management authority.
    """
    id: str
    name: str
    region: str
    contact_email: str
    contact_phone: Optional[str] = None
    level: int = 1 # 1: local, 2: county, 3: state

    model_config = ConfigDict(from_attributes=True)

class RoadAuthorityCreate(BaseModel):
    name: str
    region: str
    contact_email: str
    contact_phone: Optional[str] = None
    level: int = 1
