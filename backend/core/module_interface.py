"""
Module Interface — The contract every detection module must implement.

This is the cornerstone of the plugin architecture. Any new module
(traffic monitoring, flood detection, waste management, etc.) simply
creates a class that extends ModuleInterface, and the platform
auto-discovers, validates, and registers it.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from fastapi import APIRouter


class ModuleInterface(ABC):
    """
    Abstract base class that every detection module must implement.

    The Module Registry will:
    1. Discover classes extending this interface in /modules/*/manifest.py
    2. Validate that all abstract methods are implemented
    3. Call initialize() during platform startup
    4. Mount get_router() under /api/v1/{module_id}/
    5. Call health_check() for status monitoring
    6. Call shutdown() during platform shutdown
    """

    @abstractmethod
    def get_id(self) -> str:
        """
        Unique module identifier used in URLs, DB records, and config.
        Convention: lowercase_snake_case, e.g., 'roadscan_ai'
        """

    @abstractmethod
    def get_name(self) -> str:
        """
        Human-readable display name.
        Example: 'RoadScan AI'
        """

    @abstractmethod
    def get_version(self) -> str:
        """
        Semantic version string.
        Example: '1.0.0'
        """

    @abstractmethod
    def get_description(self) -> str:
        """Module description for the admin dashboard."""

    @abstractmethod
    def get_router(self) -> APIRouter:
        """
        Return a FastAPI APIRouter with all module-specific endpoints.
        The registry will mount this under /api/v1/{module_id}/
        """

    @abstractmethod
    def get_incident_types(self) -> List[str]:
        """
        Return the list of incident types this module can produce.
        Example: ['pothole', 'road_crack']
        Used for filtering, analytics, and dashboard categorization.
        """

    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Return a JSON-Schema-like dict describing module-specific
        configuration options. Used by the admin UI to render
        configuration forms.
        """

    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> None:
        """
        Called once during platform startup.
        Use this to:
        - Load AI models
        - Validate configuration
        - Start background workers
        - Warm up inference pipelines
        """

    @abstractmethod
    async def shutdown(self) -> None:
        """
        Called during platform shutdown.
        Use this to:
        - Release GPU/model resources
        - Stop background workers
        - Flush pending data
        """

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Return module health status. Called periodically and on-demand.

        Expected return format:
        {
            "status": "healthy" | "degraded" | "unhealthy",
            "model_loaded": True/False,
            "inference_fps": 12.5,
            "details": { ... }
        }
        """

    @abstractmethod
    def get_frontend_manifest(self) -> Dict[str, Any]:
        """
        Return frontend component registration info.
        The dashboard uses this to render module navigation,
        widgets, and incident type renderers.

        Expected return format:
        {
            "icon": "🛣️",
            "nav_items": [
                {"path": "/roadscan/scan", "label": "Live Scan", "icon": "Camera"},
            ],
            "dashboard_widget": True,
            "incident_renderers": ["pothole"],
        }
        """
