"""
Smart City Infrastructure Monitoring Platform — Application Entrypoint

This is the main FastAPI application. It:
1. Initializes the platform core services
2. Discovers and registers all detection modules via the Module Registry
3. Mounts shared routes (auth, incidents, health, etc.)
4. Mounts module-specific routes under /api/v1/{module_id}/
5. Sets up middleware (CORS, error handling, rate limiting)
6. Manages startup/shutdown lifecycle
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from core.database import init_db, close_db
from core.module_registry import module_registry
from core.routes import health, modules, incidents, sessions, devices, analytics, escalation, heatmap
from core.websocket.hub import websocket_router
from core.middleware.error_handler import global_exception_handler
from core.middleware.rate_limiter import RateLimiterMiddleware
from core.logging_config import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    - Startup: Initialize DB, discover & initialize all modules
    - Shutdown: Gracefully shut down all modules, close DB
    """
    # ── Startup ──
    logger = setup_logging()
    logger.info(f"Starting {settings.app_name} ({settings.app_env})")
    await init_db()
    logger.info("Database initialized")

    # Discover and initialize all detection modules
    await module_registry.discover_and_register()
    print(f"{len(module_registry.modules)} module(s) registered")

    for module_id, module in module_registry.modules.items():
        print(f"   - {module.get_name()} v{module.get_version()} [{module_id}]")

    yield

    # ── Shutdown ──
    print(f"Shutting down {settings.app_name}")
    await module_registry.shutdown_all()
    await close_db()
    print("Shutdown complete")


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        description="Smart City Infrastructure Monitoring Platform — Modular AI Detection System",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    # ── Middleware ──
    app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    # ── Core Platform Routes ──
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])
    app.include_router(modules.router, prefix="/api/v1/modules", tags=["Modules"])
    app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])
    app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["Sessions"])
    app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])
    app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
    app.include_router(escalation.router, prefix="/api/v1/escalations", tags=["Escalations"])
    app.include_router(heatmap.router, prefix="/api/v1/heatmap", tags=["Heatmap"])
    # ── WebSocket Hub ──
    app.include_router(websocket_router)

    # ── Module Routes (dynamically mounted) ──
    # Module routers are mounted by the registry during startup via lifespan.
    # They are added via: app.include_router(module.get_router(), prefix=f"/api/v1/{module_id}")
    # This happens in module_registry.discover_and_register()
    # We store the app reference in the registry so it can mount routers.
    module_registry.set_app(app)

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.app_port,
        reload=settings.is_development,
    )
