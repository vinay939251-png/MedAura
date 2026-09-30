# MedAura API Documentation

This platform provides a REST API for core infrastructure tasks and dynamic APIs mapped to specific AI modules (like `roadscan_ai`).

## Core Platform Endpoints

### 1. Health & Status
- **`GET /api/v1/health`**
  - Returns overall system health, DB connectivity, and active sessions count.

### 2. Modules
- **`GET /api/v1/modules`**
  - Lists all registered AI modules (e.g., `roadscan_ai`) and their configuration status.
- **`GET /api/v1/modules/{module_id}/health`**
  - Returns specific health checks for a module (e.g. if the ONNX model is loaded).

### 3. Incidents (Global)
- **`GET /api/v1/incidents`**
  - Query incidents across all modules. Supports filtering by `module_id`, `severity`, and temporal ranges.
- **`GET /api/v1/incidents/{incident_id}`**
  - Detailed view of a single incident, including spatial metadata.
- **`PATCH /api/v1/incidents/{incident_id}/status`**
  - Updates incident status (e.g., `reported` -> `resolved`).

### 4. Escalations
- **`POST /api/v1/escalations`**
  - Escalate an incident to a specific road authority level.
- **`GET /api/v1/escalations/{incident_id}`**
  - Get the escalation lifecycle history for an incident.

### 5. Geospatial & Analytics
- **`GET /api/v1/heatmap/geojson`**
  - Returns a `FeatureCollection` (GeoJSON format) of incident points for direct map rendering in Mapbox/Leaflet.
- **`GET /api/v1/analytics/summary`**
  - Dashboard statistics: counts grouped by severity, status, and module over time.

## Module-Specific Endpoints: RoadScan AI

- **`POST /api/v1/roadscan_ai/incidents`**
  - Creates a pothole incident. Triggers the deduplication and severity classification engines automatically.
- **`GET /api/v1/roadscan_ai/incidents/stats`**
  - Returns module-specific stats (e.g., total potholes detected today).
- **`GET /api/v1/roadscan_ai/config`**
  - Retrieves confidence thresholds and inference resolutions.

## WebSockets

- **`ws://<host>/ws/incidents`**
  - Subscribe to real-time incident creation events across the platform.

*For interactive Swagger UI documentation and live testing, start the backend and visit `/docs`.*
