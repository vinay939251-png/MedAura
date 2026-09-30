"""
Tests for Deduplication Engine.

Validates:
- Haversine distance calculation
- Same location within threshold is duplicate
- Different locations are not duplicate
"""

import pytest
from core.services.deduplication import calculate_distance, check_duplicate_incident
from core.models.incident import Incident
from datetime import datetime, timezone, timedelta

def test_calculate_distance():
    # New York to London
    dist = calculate_distance(40.7128, -74.0060, 51.5074, -0.1278)
    assert 5500000 < dist < 5600000  # ~5,570 km

    # Hyderabad points, a few meters apart
    dist2 = calculate_distance(17.385044, 78.486671, 17.385100, 78.486700)
    assert 0 < dist2 < 20
    
    # Same point
    dist3 = calculate_distance(10.0, 10.0, 10.0, 10.0)
    assert dist3 == 0.0

@pytest.mark.asyncio
async def test_check_duplicate_incident_empty_db(db_session):
    is_dup, _ = await check_duplicate_incident(
        db_session, "roadscan_ai", "pothole", 17.0, 78.0
    )
    assert is_dup is False

@pytest.mark.asyncio
async def test_check_duplicate_incident_true(db_session, sample_incident_data):
    # Add an incident
    now = datetime.now(timezone.utc)
    inc = Incident(**sample_incident_data(detected_at=now, latitude=17.0, longitude=78.0))
    db_session.add(inc)
    await db_session.commit()
    
    # Check slightly offset location (within 15m)
    # 0.00001 deg is ~1.11m
    is_dup, dup_id = await check_duplicate_incident(
        db_session, "roadscan_ai", "pothole", 17.00001, 78.00001, 15.0, 60
    )
    assert is_dup is True
    assert dup_id == inc.id

@pytest.mark.asyncio
async def test_check_duplicate_incident_spatial_diff(db_session, sample_incident_data):
    now = datetime.now(timezone.utc)
    inc = Incident(**sample_incident_data(detected_at=now, latitude=17.0, longitude=78.0))
    db_session.add(inc)
    await db_session.commit()
    
    # Check far location (100m+ away)
    is_dup, _ = await check_duplicate_incident(
        db_session, "roadscan_ai", "pothole", 17.001, 78.001, 15.0, 60
    )
    assert is_dup is False

@pytest.mark.asyncio
async def test_check_duplicate_incident_temporal_diff(db_session, sample_incident_data):
    # Old incident
    old_time = datetime.now(timezone.utc) - timedelta(seconds=120)
    inc = Incident(**sample_incident_data(detected_at=old_time, latitude=17.0, longitude=78.0))
    db_session.add(inc)
    await db_session.commit()
    
    # Same location, but older than threshold (60s)
    is_dup, _ = await check_duplicate_incident(
        db_session, "roadscan_ai", "pothole", 17.0, 78.0, 15.0, 60
    )
    assert is_dup is False
