"""
Shared test fixtures for the RoadScan AI test suite.

Provides:
- Async test database (in-memory SQLite)
- FastAPI test client
- Sample data factories
- Mock AI runtime
"""

import os
import sys
import uuid
import pytest
import pytest_asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

# Ensure backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Override database URL BEFORE importing app modules
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["APP_ENV"] = "testing"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.database import Base, get_db
from main import app


# ── Async Database Fixtures ──

@pytest_asyncio.fixture
async def async_engine():
    """Create an in-memory SQLite engine for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(async_engine):
    """Provide a transactional database session for each test."""
    session_factory = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_modules():
    """Ensure modules are discovered and registered for all tests."""
    from core.module_registry import module_registry
    from main import app
    
    module_registry.set_app(app)
    # We must ensure discovery happens before tests run
    # If already populated, skip to avoid duplicate routes
    if not module_registry.modules:
        await module_registry.discover_and_register()

@pytest_asyncio.fixture
async def client(async_engine, initialize_modules):
    """Provide an async HTTP test client with a test database."""
    session_factory = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_db():
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Sample Data Factories ──

@pytest.fixture
def sample_incident_data():
    """Factory for valid incident creation payloads."""
    def _make(**overrides):
        base = {
            "module_id": "roadscan_ai",
            "incident_type": "pothole",
            "confidence": 0.85,
            "severity": "high",
            "tracking_id": 42,
            "latitude": 17.385044,
            "longitude": 78.486671,
            "gps_accuracy": 5.2,
            "bounding_box": {"x1": 100.0, "y1": 200.0, "x2": 300.0, "y2": 400.0},
            "model_version": "roadscan-v1.0",
            "runtime_mode": "edge",
            "module_data": {
                "pothole_area_px": 12450,
                "road_surface_type": "asphalt",
                "detection_frame_count": 8,
                "inference_latency_ms": 45.2,
            },
        }
        base.update(overrides)
        return base
    return _make


@pytest.fixture
def sample_device_data():
    """Factory for valid device registration payloads."""
    def _make(**overrides):
        base = {
            "device_name": "Bus-HYD-001",
            "device_type": "bus",
            "identifier": f"TS09-{uuid.uuid4().hex[:6].upper()}",
            "is_active": True,
        }
        base.update(overrides)
        return base
    return _make


@pytest.fixture
def sample_session_data():
    """Factory for valid detection session payloads."""
    def _make(**overrides):
        base = {
            "runtime_mode": "edge",
            "module_id": "roadscan_ai",
            "status": "active",
        }
        base.update(overrides)
        return base
    return _make


# ── Mock AI Runtime ──

@pytest.fixture
def mock_runtime():
    """Create a mock AI runtime for testing without a real model."""
    runtime = MagicMock()
    runtime.is_loaded.return_value = True
    runtime.load_model = AsyncMock()
    runtime.unload = AsyncMock()
    runtime.infer = AsyncMock(return_value=[])
    runtime.get_model_info.return_value = MagicMock(
        architecture="yolov8",
        num_classes=1,
        class_names={0: "pothole"},
        input_resolution=640,
        framework="ultralytics/pytorch",
    )
    runtime.benchmark = AsyncMock()
    return runtime
