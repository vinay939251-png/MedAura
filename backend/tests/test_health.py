"""
Tests for the platform health check endpoint.

Validates:
- Health endpoint returns correct structure
- Platform name and environment are reported
- Module health is aggregated
"""

import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_health_endpoint_returns_200(client):
    """Health endpoint should return 200 with platform status."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_response_structure(client):
    """Health response should contain required fields."""
    response = await client.get("/api/v1/health")
    data = response.json()

    assert "status" in data
    assert "platform" in data
    assert "environment" in data
    assert "modules" in data
    assert "database" in data


@pytest.mark.asyncio
async def test_health_status_is_healthy(client):
    """Health status should be 'healthy' when server is running."""
    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_environment_is_testing(client):
    """Environment should reflect the test configuration."""
    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["environment"] == "testing"


@pytest.mark.asyncio
async def test_health_modules_is_dict(client):
    """Modules health should be a dictionary."""
    response = await client.get("/api/v1/health")
    data = response.json()
    assert isinstance(data["modules"], dict)
