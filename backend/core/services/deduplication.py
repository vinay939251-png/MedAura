import math
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
import uuid

from core.models.incident import Incident


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees) using Haversine formula.
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in meters is 6371000
    meters = 6371000 * c
    return meters


async def check_duplicate_incident(
    db: AsyncSession,
    module_id: str,
    incident_type: str,
    latitude: float,
    longitude: float,
    spatial_threshold_m: float = 15.0,
    temporal_threshold_s: int = 60
) -> Tuple[bool, Optional[uuid.UUID]]:
    """
    Check if a similar incident was recently reported near this location.
    
    Returns:
        (is_duplicate, duplicate_incident_id)
    """
    # For a real spatial query, we would use PostGIS ST_DWithin.
    # Since we might be using SQLite, we can approximate a bounding box 
    # to filter first, then calculate exact distances.
    
    # 1 degree of latitude is ~111,320 meters
    lat_offset = spatial_threshold_m / 111320.0
    # 1 degree of longitude is ~111,320 * cos(latitude) meters
    lon_offset = spatial_threshold_m / (111320.0 * math.cos(math.radians(latitude)))
    
    # Filter candidates within the rough bounding box, limited to recent ones
    # To keep it simple and DB-agnostic, we just fetch recent incidents of the same type
    # and calculate distance in Python.
    
    # Let's get the 10 most recent incidents of this type
    query = (
        select(Incident)
        .where(
            and_(
                Incident.module_id == module_id,
                Incident.incident_type == incident_type
            )
        )
        .order_by(Incident.detected_at.desc())
        .limit(20)
    )
    
    result = await db.execute(query)
    recent_incidents = result.scalars().all()
    
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for inc in recent_incidents:
        # Check temporal distance
        # Ensure detected_at has tzinfo
        dt = inc.detected_at
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            
        time_diff = (now - dt).total_seconds()
        
        if time_diff <= temporal_threshold_s:
            # Check spatial distance
            dist = calculate_distance(latitude, longitude, inc.latitude, inc.longitude)
            if dist <= spatial_threshold_m:
                return True, inc.id
                
    return False, None
