"""
Tests for the global exception handler middleware.

Validates:
- Unhandled exceptions do not crash the server
- Exception details are hidden in non-debug mode
- 500 status code is correctly returned
- Structured JSON error is returned
"""

import pytest
from fastapi import APIRouter
from httpx import AsyncClient, ASGITransport

from main import app

# Create a temporary route that explicitly raises an exception for testing
test_router = APIRouter()

@test_router.get("/api/v1/test-crash")
async def trigger_crash():
    raise ValueError("This is an intentional crash for testing")

app.include_router(test_router)


@pytest.mark.asyncio
async def test_global_exception_handler_returns_500():
    """An unhandled exception should be caught and return a 500 status code."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/test-crash")

        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False
        assert data["error"] == "Internal server error"
        # We don't assert detail here because it depends on app.extra["debug"]

@pytest.mark.asyncio
async def test_global_exception_handler_hides_detail_in_production():
    """Exception details should be hidden if not in debug mode."""
    # Ensure debug is false
    app.extra["debug"] = False
    
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/test-crash")
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] is None

@pytest.mark.asyncio
async def test_global_exception_handler_shows_detail_in_debug():
    """Exception details should be shown if in debug mode."""
    # Ensure debug is true
    app.extra["debug"] = True
    
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/v1/test-crash")
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "This is an intentional crash for testing"
        
    # Reset debug state to avoid side effects
    app.extra["debug"] = False
