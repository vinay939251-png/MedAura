"""
Module Registry — Auto-discovery, validation, and lifecycle management.

Scans the /modules/ directory for classes implementing ModuleInterface,
validates them, calls their lifecycle hooks, and mounts their API routers.
"""

import importlib
import pkgutil
from typing import Dict, Optional
from fastapi import FastAPI

from core.module_interface import ModuleInterface


class ModuleRegistry:
    """
    Central registry that manages all detection modules.

    Responsibilities:
    - Discover module manifests in backend/modules/
    - Validate interface compliance
    - Initialize modules (model loading, worker startup)
    - Mount FastAPI routers under /api/v1/{module_id}/
    - Provide health checks across all modules
    - Graceful shutdown of all modules
    """

    def __init__(self):
        self.modules: Dict[str, ModuleInterface] = {}
        self._app: Optional[FastAPI] = None

    def set_app(self, app: FastAPI) -> None:
        """Store reference to the FastAPI app for dynamic router mounting."""
        self._app = app

    async def discover_and_register(self) -> None:
        """
        Scan backend/modules/ for module manifests and register them.

        Each module directory must contain a manifest.py with a class
        extending ModuleInterface. The registry discovers these via
        Python's pkgutil.
        """
        import modules as modules_package

        for importer, module_name, is_pkg in pkgutil.iter_modules(
            modules_package.__path__
        ):
            if not is_pkg:
                continue

            try:
                # Import the manifest from each module package
                manifest_module = importlib.import_module(
                    f"modules.{module_name}.manifest"
                )

                # Look for a class extending ModuleInterface
                module_class = None
                for attr_name in dir(manifest_module):
                    attr = getattr(manifest_module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, ModuleInterface)
                        and attr is not ModuleInterface
                    ):
                        module_class = attr
                        break

                if module_class is None:
                    print(
                        f"   [!] Module '{module_name}': No ModuleInterface implementation found in manifest.py"
                    )
                    continue

                # Instantiate and validate
                module_instance = module_class()
                module_id = module_instance.get_id()

                if module_id in self.modules:
                    print(
                        f"   [!] Module '{module_id}': Duplicate module ID, skipping"
                    )
                    continue

                # Initialize the module (load models, start workers, etc.)
                await module_instance.initialize(config={})

                # Mount the module's API router
                if self._app is not None:
                    router = module_instance.get_router()
                    self._app.include_router(
                        router,
                        prefix=f"/api/v1/{module_id}",
                        tags=[module_instance.get_name()],
                    )

                # Register
                self.modules[module_id] = module_instance
                print(f"   [+] Module '{module_id}' registered successfully")

            except Exception as e:
                print(f"   [x] Module '{module_name}' failed to register: {e}")

    async def shutdown_all(self) -> None:
        """Gracefully shut down all registered modules."""
        for module_id, module in self.modules.items():
            try:
                await module.shutdown()
                print(f"   [-] Module '{module_id}' shut down")
            except Exception as e:
                print(f"   [x] Module '{module_id}' shutdown error: {e}")

    def get_module(self, module_id: str) -> Optional[ModuleInterface]:
        """Get a specific module by ID."""
        return self.modules.get(module_id)

    async def get_all_health(self) -> Dict[str, Dict]:
        """Get health status of all registered modules."""
        health = {}
        for module_id, module in self.modules.items():
            try:
                health[module_id] = await module.health_check()
            except Exception as e:
                health[module_id] = {
                    "status": "unhealthy",
                    "error": str(e),
                }
        return health

    def get_all_manifests(self) -> Dict[str, Dict]:
        """Get frontend manifests for all modules (used by dashboard)."""
        manifests = {}
        for module_id, module in self.modules.items():
            manifests[module_id] = {
                "id": module.get_id(),
                "name": module.get_name(),
                "version": module.get_version(),
                "description": module.get_description(),
                "incident_types": module.get_incident_types(),
                "frontend": module.get_frontend_manifest(),
            }
        return manifests


# Singleton instance — used by main.py and route handlers
module_registry = ModuleRegistry()
