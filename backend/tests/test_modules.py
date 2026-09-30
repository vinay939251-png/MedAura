"""
Tests for Module Registry API.

Validates:
- Listing registered modules
- Fetching specific module health
"""

import pytest

@pytest.mark.asyncio
async def test_list_modules(client):
    """Listing modules should return at least the roadscan_ai module."""
    response = await client.get("/api/v1/modules")
    assert response.status_code == 200
    
    data = response.json()
    assert "modules" in data
    assert "roadscan_ai" in data["modules"]

    mod = data["modules"]["roadscan_ai"]
    assert mod["id"] == "roadscan_ai"
    assert mod["name"] == "RoadScan AI"
    assert "pothole" in mod["incident_types"]


@pytest.mark.asyncio
async def test_module_health(client):
    """Fetching module health should work for a registered module."""
    response = await client.get("/api/v1/modules/roadscan_ai/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["module"] == "roadscan_ai"
    assert "status" in data


@pytest.mark.asyncio
async def test_module_health_not_found(client):
    """Fetching module health for non-existent module should return 404."""
    response = await client.get("/api/v1/modules/non_existent/health")
    assert response.status_code == 404
