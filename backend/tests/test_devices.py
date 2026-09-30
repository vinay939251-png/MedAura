"""
Tests for Devices API.

Validates:
- Device retrieval
- Device listing
"""

import pytest
import uuid

@pytest.mark.asyncio
async def test_list_devices_empty(client):
    """Listing devices when none exist should return empty list."""
    response = await client.get("/api/v1/devices/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

@pytest.mark.asyncio
async def test_get_device_not_found(client):
    """Getting a non-existent device should return 404."""
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/devices/{fake_id}")
    assert response.status_code == 404
