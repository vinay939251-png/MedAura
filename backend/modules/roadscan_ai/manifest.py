"""
ROADSCAN AI — Module Manifest

This is the module's entry point. The Module Registry discovers this class,
validates the interface, and registers the module during platform startup.

This file implements ModuleInterface and wires together:
- Module-specific API routes
- AI runtime initialization
- Health monitoring
- Frontend manifest for dashboard integration
"""

from typing import List, Dict, Any
from fastapi import APIRouter

from core.module_interface import ModuleInterface
from modules.roadscan_ai.routes import detection, incidents as roadscan_incidents
from modules.roadscan_ai.config import ROADSCAN_CONFIG, ROADSCAN_CONFIG_SCHEMA


class RoadscanAIModule(ModuleInterface):
    """
    ROADSCAN AI — Real-time Pothole Detection Module

    Detects potholes using YOLO inference (edge or server-side),
    tracks them with ByteTrack, and generates geo-located incidents.
    """

    def __init__(self):
        self._runtime = None
        self._is_initialized = False
        self._config = ROADSCAN_CONFIG.copy()

    def get_id(self) -> str:
        return "roadscan_ai"

    def get_name(self) -> str:
        return "RoadScan AI"

    def get_version(self) -> str:
        return "1.0.0"

    def get_description(self) -> str:
        return "Real-time pothole detection using YOLO object detection with edge-first inference and GPS-based incident mapping."

    def get_router(self) -> APIRouter:
        """Combine all ROADSCAN AI routes into a single router."""
        router = APIRouter()
        router.include_router(detection.router, tags=["RoadScan - Detection"])
        router.include_router(roadscan_incidents.router, tags=["RoadScan - Incidents"])
        return router

    def get_incident_types(self) -> List[str]:
        return ["pothole"]

    def get_config_schema(self) -> Dict[str, Any]:
        return ROADSCAN_CONFIG_SCHEMA

    async def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize ROADSCAN AI:
        1. Load AI model (if in server mode)
        2. Validate configuration
        3. Mark as ready
        """
        # Merge provided config with defaults
        self._config.update(config)

        # In edge mode, the browser handles inference — we just need the API
        # In server mode, we'd load the model here
        # For now, mark as initialized (model loading happens in Phase 2)
        self._is_initialized = True

    async def shutdown(self) -> None:
        """Release ROADSCAN AI resources."""
        if self._runtime:
            await self._runtime.unload()
        self._is_initialized = False

    async def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy" if self._is_initialized else "not_initialized",
            "module": self.get_id(),
            "version": self.get_version(),
            "model_loaded": self._runtime is not None and self._runtime.is_loaded() if self._runtime else False,
            "runtime_mode": self._config.get("runtime_mode", "edge"),
            "incident_types": self.get_incident_types(),
        }

    def get_frontend_manifest(self) -> Dict[str, Any]:
        return {
            "icon": "🛣️",
            "color": "#FF6B35",
            "nav_items": [
                {"path": "/roadscan/scan", "label": "Live Scan", "icon": "Camera"},
                {"path": "/roadscan/map", "label": "Pothole Map", "icon": "Map"},
                {"path": "/roadscan/reports", "label": "Reports", "icon": "BarChart"},
            ],
            "dashboard_widget": True,
            "incident_renderers": ["pothole"],
        }
