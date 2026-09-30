"""
Heatmap Routes — Geospatial density mapping of incidents.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.database import get_db
from core.models.incident import Incident

router = APIRouter()

@router.get("/geojson")
async def get_incident_heatmap_geojson(
    module_id: str = None,
    severity: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns incident data formatted as GeoJSON for heatmap visualization (e.g., in Leaflet/Mapbox).
    """
    query = select(Incident)
    
    if module_id:
        query = query.where(Incident.module_id == module_id)
    if severity:
        query = query.where(Incident.severity == severity)
        
    result = await db.execute(query)
    incidents = result.scalars().all()
    
    features = []
    for inc in incidents:
        if inc.latitude is not None and inc.longitude is not None:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [inc.longitude, inc.latitude] # GeoJSON uses [lon, lat]
                },
                "properties": {
                    "id": str(inc.id),
                    "type": inc.incident_type,
                    "severity": inc.severity,
                    "confidence": inc.confidence,
                    "detected_at": inc.detected_at.isoformat() if inc.detected_at else None
                }
            })
            
    return {
        "type": "FeatureCollection",
        "features": features
    }
