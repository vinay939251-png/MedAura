<![CDATA[# 🛣️ ROADSCAN AI — Smart City Infrastructure Monitoring Platform

> **Real-time AI-powered road hazard detection using edge computing, computer vision, and geospatial analytics**

[![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/Frontend-React%20(Vite)-61DAFB?style=flat-square&logo=react)](https://vitejs.dev)
[![AI](https://img.shields.io/badge/AI-YOLO%20%2B%20ByteTrack-FF6F00?style=flat-square)](https://docs.ultralytics.com)
[![Database](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20PostGIS-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)]()

**GitHub**: [github.com/vinay939251-png/MedAura](https://github.com/vinay939251-png/MedAura)

---

## 📋 Table of Contents

1. [Problem Statement](#-problem-statement)
2. [Our Solution](#-our-solution)
3. [Innovation & Unique Selling Points](#-innovation--unique-selling-points)
4. [System Architecture](#-system-architecture)
5. [Modular Plugin System](#-modular-plugin-system)
6. [Technical Architecture Deep Dive](#-technical-architecture-deep-dive)
7. [AI & Computer Vision Pipeline](#-ai--computer-vision-pipeline)
8. [Database Design](#-database-design)
9. [API Design](#-api-design)
10. [Real-Time Communication](#-real-time-communication)
11. [Security Architecture](#-security-architecture)
12. [Scalability & Performance](#-scalability--performance)
13. [Deployment Strategy](#-deployment-strategy)
14. [Feasibility & Risk Assessment](#-feasibility--risk-assessment)
15. [Social Impact & Sustainability](#-social-impact--sustainability)
16. [Tech Stack Justification](#-tech-stack-justification)
17. [Project Structure](#-project-structure)
18. [Configuration Architecture](#-configuration-architecture)
19. [Implementation Roadmap](#-implementation-roadmap)
20. [Architecture Decision Records](#-architecture-decision-records)
21. [Adding Future Modules — Developer Guide](#-adding-future-modules--developer-guide)
22. [Detailed Technical Specification](#-detailed-technical-specification)
23. [Development Journal](#-development-journal)

---

## 🎯 Problem Statement

### The Crisis

India has over **6.2 million kilometers of roads**, and road surface deterioration — particularly **potholes** — is one of the leading causes of:

- **~13,000 deaths annually** due to pothole-related accidents (MoRTH data)
- **₹1.5 lakh crore in annual vehicle damage** across the country
- **Chronic delays in detection and repair** — municipalities rely on manual complaints and infrequent surveys
- **No real-time monitoring** — by the time a pothole is reported, it has often already caused damage

### The Gap

Current approaches fail because:

| Current Method | Limitation |
|---|---|
| Manual inspection | Slow, expensive, infrequent, covers <5% of road network |
| Citizen complaints | Reactive, unverified, location-imprecise, delayed |
| Periodic surveys | Months between checks, no real-time data |
| Existing AI systems | Cloud-dependent, high bandwidth, high latency, no edge capability |

### What's Needed

A system that can:
1. **Detect potholes in real-time** from moving vehicles
2. **Work on ordinary smartphones** — no special hardware
3. **Operate with minimal bandwidth** — edge-first, not cloud-dependent
4. **Geolocate incidents precisely** using GPS
5. **Scale to city-wide deployment** across fleets of buses, patrol vehicles, and citizen devices
6. **Extend to other infrastructure hazards** — cracks, flooding, debris, damaged signage

---

## 💡 Our Solution

**ROADSCAN AI** is a **modular smart city infrastructure monitoring platform** that transforms any Android smartphone into a real-time road hazard detection device using **edge AI**.

```
📱 Android Smartphone Camera
    ↓
🧠 On-Device YOLO Inference (Edge AI)
    ↓
🔍 ByteTrack Multi-Object Tracking
    ↓
📍 GPS-Correlated Incident Generation
    ↓
⚡ Lightweight API (metadata only — no video upload)
    ↓
🗺️ Real-Time GIS Dashboard & Alerts
```

### How It Works

1. **Mount any Android phone** on a bus windshield or patrol vehicle dashboard
2. **Open the web app** in Chrome — the camera activates and AI begins running locally
3. **YOLO detects potholes** in real-time directly on the phone (no cloud needed)
4. **ByteTrack confirms** detections across multiple frames (reduces false positives)
5. **GPS coordinates** are captured and matched to each confirmed detection
6. **Only metadata** (coordinates, confidence, severity) is sent to the backend — **not video**
7. **The dashboard** updates in real-time with mapped incidents, severity heatmaps, and analytics
8. **Alerts** are sent to maintenance teams for critical detections

### Key Differentiator

> **Traditional systems upload entire video streams to cloud servers for processing. ROADSCAN AI runs inference directly on the phone's browser, sending only tiny metadata payloads (~200 bytes per incident vs ~5 MB/s for video). This reduces bandwidth by 99.99% and enables operation even with intermittent connectivity.**

---

## 🚀 Innovation & Unique Selling Points

### 1. Edge-First AI Architecture
- AI inference runs **directly in the browser** using ONNX Runtime Web
- No cloud GPU required for real-time detection
- Works offline — detections continue even without internet
- Automatic fallback to server-side inference if device can't handle edge AI

### 2. Modular Plugin System
- **Not a single-purpose pothole detector** — it's an extensible platform
- New detection modules (traffic violations, flood zones, waste accumulation, damaged signage) can be added by implementing a single `ModuleInterface` contract
- Each module gets auto-discovered, auto-routed, and auto-integrated into the dashboard
- **~8-12 new files** to add a module; **zero changes** to core platform code

### 3. Adaptive Inference Scheduling
- Camera runs at 30 FPS for smooth video
- AI processes only 5-15 frames/second depending on device capability
- **Latest-frame strategy** — stale frames are discarded, not queued
- Prevents memory buildup and ensures detections are always current

### 4. Multi-Runtime AI Abstraction
- Single `RuntimeInterface` supports: PyTorch, ONNX Runtime, TensorRT, and Browser Edge
- **Benchmark-driven runtime selection** — not assumptions
- Model can be swapped without changing any application code

### 5. Intelligent Incident Deduplication
- Spatial deduplication: same pothole from different frames = 1 incident
- Temporal deduplication: same location within cooldown window = 1 incident
- Tracker-independent: works even if ByteTrack resets tracking IDs

### 6. Graceful Degradation
- GPS unavailable → detection continues, incident queued for location
- Network down → metadata queued locally, synced when online
- AI model fails → dashboard and database remain accessible
- Device overheating → inference FPS automatically reduces

### 7. Privacy by Design
- **Raw camera footage never leaves the device** in edge mode
- Only structured metadata (coordinates, confidence scores) is transmitted
- No personal data collected — detects road conditions, not people

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                             │
│  📱 Android Chrome / PWA        🖥️ Admin Dashboard (React)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  API GATEWAY LAYER                            │
│     🔀 FastAPI Gateway — Auth · Routing · Rate Limiting      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌───────────────┐ ┌──────────┐ ┌──────────────┐
│ SHARED CORE   │ │ MODULE   │ │ REAL-TIME    │
│ SERVICES      │ │ REGISTRY │ │ LAYER        │
│               │ │          │ │              │
│ 🔐 Auth       │ │ 📦 Plugin │ │ 🔌 WebSocket │
│ 📍 GPS        │ │   Loader │ │    Hub       │
│ 🚨 Incident   │ │          │ │ 📡 SSE       │
│ 📊 Analytics  │ │          │ │   Fallback   │
│ 🔔 Alerts     │ │          │ │              │
│ 💾 Sessions   │ │          │ │              │
└───────────────┘ └─────┬────┘ └──────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 🛣️ ROADSCAN │ │ 🚦 FUTURE:  │ │ 🌊 FUTURE:  │
│    AI       │ │   Traffic   │ │   Flood     │
│ (Pothole    │ │   Monitor   │ │   Detection │
│  Detection) │ │             │ │             │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
         ┌─────────────────────────┐
         │  🧠 AI RUNTIME LAYER    │
         │  PyTorch · ONNX ·       │
         │  TensorRT · Edge        │
         └────────────┬────────────┘
                      ▼
         ┌─────────────────────────┐
         │     DATA LAYER          │
         │  🐘 PostgreSQL + PostGIS │
         │  🗺️ GIS Engine           │
         │  📁 Model Storage        │
         └─────────────────────────┘
```

### Architecture Style: Modular Monolith → Microservices-Ready

The platform uses a **modular monolith** pattern — all modules run in a single deployment but are fully isolated through interfaces. This provides:

- **Simplicity** of a monolith for MVP/hackathon
- **Isolation** of a microservice architecture through interface contracts
- **Migration path** — modules can be extracted to separate services later with zero interface changes

---

## 🔌 Modular Plugin System

This is the **most critical design element** — it's what makes the platform extensible.

### The ModuleInterface Contract

Every detection module (ROADSCAN AI, future traffic monitor, flood detection, etc.) must implement:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from fastapi import APIRouter

class ModuleInterface(ABC):
    """Every detection module must implement this interface."""

    def get_id(self) -> str: ...          # 'roadscan_ai'
    def get_name(self) -> str: ...        # 'RoadScan AI'
    def get_version(self) -> str: ...     # '1.0.0'
    def get_description(self) -> str: ... # Module description
    def get_router(self) -> APIRouter: ...         # API routes
    def get_incident_types(self) -> List[str]: ... # ['pothole']
    def get_config_schema(self) -> Dict[str, Any]: ...  # Config schema
    async def initialize(self, config) -> None: ...     # Startup
    async def shutdown(self) -> None: ...               # Cleanup
    async def health_check(self) -> Dict[str, Any]: ... # Health status
    def get_frontend_manifest(self) -> Dict[str, Any]: ... # UI registration
```

### How Module Discovery Works

```
Platform Startup
    │
    ▼
Module Registry scans /modules/ directory
    │
    ▼
For Each Module Found:
    ├── Import manifest.py
    ├── Validate ModuleInterface implementation
    ├── Call initialize(config)
    ├── Load AI model / start workers
    ├── Mount APIRouter → /api/v1/{module_id}/
    └── Register module metadata in DB
    │
    ▼
All modules ready — Platform online
```

### Extensibility Metrics

| Metric | Value |
|--------|-------|
| Files to create for a new module | ~8-12 |
| Existing files to modify | 2 (registry imports) |
| Core platform files changed | 0 |
| Time to add a basic module | < 2 hours |
| Supported module types | Detection, Monitoring, Analytics |

### Frontend Module Registration

Each module exports a registration object that auto-configures sidebar navigation, dashboard widgets, and incident renderers:

```javascript
export const RoadscanModule = {
  id: 'roadscan_ai',
  name: 'RoadScan AI',
  icon: '🛣️',
  navItems: [
    { path: '/roadscan/scan', label: 'Live Scan', icon: 'Camera' },
    { path: '/roadscan/map', label: 'Pothole Map', icon: 'Map' },
    { path: '/roadscan/reports', label: 'Reports', icon: 'BarChart' },
  ],
  dashboardWidget: RoadscanWidget,
  incidentRenderers: { pothole: PotholeIncidentCard },
};
```

---

## 🔬 Technical Architecture Deep Dive

### Data Flow — Edge Mode (Primary)

```
📷 Camera (30 FPS)
    │
    ▼
🌐 Browser (React)
    ├── Display video on <canvas>
    │
    └── Adaptive Inference Loop (5-15 FPS)
         │
         ▼
    🧠 ONNX Runtime Web
         │  YOLO inference on latest frame
         │  (stale frames discarded — bounded queue of 1)
         │
         ▼
    🔍 ByteTrack (JavaScript)
         │  Assign tracking IDs
         │  Confirm detection over N frames
         │
         ▼
    🎨 Canvas Overlay — draw bounding boxes
         │
         ▼
    📍 GPS API (independent, continuous)
         │  Match latest GPS fix to detection
         │
         ▼
    ✅ Confirmed? → POST /api/v1/roadscan_ai/incidents
         │
         │  Payload (~200 bytes):
         │  { tracking_id, confidence, severity,
         │    lat, lng, gps_accuracy, timestamp,
         │    model_version, runtime_mode }
         │
         ▼
    ⚡ FastAPI → Dedup → PostgreSQL → WebSocket → 📊 Dashboard
```

### Data Flow — Server Mode (Fallback)

```
📷 Camera → 🌐 Browser → WebSocket frames → ⚡ FastAPI
    → 🧠 Inference Worker (isolated) → ByteTrack
    → WebSocket overlay data → 🌐 Browser renders boxes
    → Incident → PostgreSQL → 📊 Dashboard
```

### Why Edge Mode is Primary

| Factor | Edge Mode | Server Mode |
|--------|-----------|-------------|
| **Bandwidth** | ~200 bytes/incident | ~5 MB/s continuous video |
| **Latency** | <100ms (local) | 200-500ms (network round-trip) |
| **Offline capable** | ✅ Yes | ❌ No |
| **Backend load** | Minimal (metadata only) | Heavy (YOLO per frame) |
| **Privacy** | Video stays on device | Video transmitted to server |
| **Scalability** | 1000s of devices, same backend | Limited by GPU resources |
| **Demo resilience** | Works if server goes down | Fails if server goes down |

### Adaptive Inference Scheduling

The system **never processes every camera frame**. This prevents memory overflow and stale detections:

```
Camera: 30 FPS → Frame Buffer (size=1, latest only)

Inference Loop:
  ┌─ Grab latest frame (discard older)
  ├─ Run YOLO → 50-200ms
  ├─ Run ByteTrack → <5ms
  ├─ Update canvas overlay
  └─ Repeat

Adaptive FPS:
  Device capable     → 10-15 inference FPS
  Device overloaded  → 5-8 inference FPS
  Device struggling  → 3-5 inference FPS + resolution reduction
  Device incapable   → Switch to SERVER mode
```

---

## 🧠 AI & Computer Vision Pipeline

### Model Strategy

**Source of truth**: `models/best.pt` — the custom-trained pothole detection model.

> ⚠️ **The system never substitutes this with a generic YOLO model.** Any runtime optimization (ONNX export, quantization, resolution reduction) must be benchmarked against the actual model to verify detection quality is preserved.

### AI Runtime Abstraction Layer

```
RuntimeInterface (Abstract Base)
    │
    ├── load_model(path, config)
    ├── infer(frame) → List[Detection]
    ├── get_model_info() → ModelInfo
    ├── benchmark(video_path) → BenchmarkResult
    ├── unload()
    └── is_loaded()
    │
    ▼ Implementations:
    │
    ├── PyTorchRuntime
    │   Input: best.pt
    │   Use: Development, model validation
    │   Advantage: Simplest, full Ultralytics compatibility
    │
    ├── ONNXRuntime
    │   Input: best.onnx (exported from best.pt)
    │   Use: Production server inference
    │   Advantage: Lower overhead, cross-platform
    │
    ├── TensorRTRuntime
    │   Input: best.engine
    │   Use: High-perf NVIDIA environments (optional)
    │   Advantage: Maximum GPU throughput
    │
    └── EdgeRuntimeConfig
        Output: Browser config for ONNX Runtime Web
        Use: On-device inference in Android Chrome
        Advantage: Zero backend load, privacy-preserving
```

### Runtime Selection: Benchmark-Driven, Not Assumed

Before production deployment, each runtime is benchmarked with the **same model, input, and hardware**:

| Metric | Measured |
|--------|----------|
| Model load time (ms) | ✅ |
| First inference latency (ms) | ✅ |
| Average inference latency (ms) | ✅ |
| P50 / P95 latency (ms) | ✅ |
| Sustained FPS | ✅ |
| RAM usage (MB) | ✅ |
| CPU / GPU utilization (%) | ✅ |
| Device temperature (°C) | ✅ |
| Detection consistency vs PyTorch baseline | ✅ |

### Edge Model Optimization Pipeline

```
best.pt (PyTorch)
    ↓ Export
best.onnx (ONNX)
    ↓ Optimize
    ├── ONNX Graph Optimization
    ├── FP16 quantization (where GPU supports)
    ├── INT8 quantization (where practical)
    └── Operator compatibility validation
    ↓ Deploy
Browser downloads model once → ONNX Runtime Web
    ↓ Runtime selection
    ├── WebGPU (preferred)
    ├── WebGL (fallback)
    └── CPU/WASM (last resort)
```

### ByteTrack Object Tracking

ByteTrack runs **on-device** alongside YOLO to:
- Assign consistent IDs to potholes across frames
- Confirm detections over N frames (reducing false positives)
- Generate incident candidates only after sufficient tracking confidence

```
Frame 1: YOLO detects → bbox (0.45 conf) → Track ID #1 assigned
Frame 2: YOLO detects → bbox (0.62 conf) → Track ID #1 matched
Frame 3: YOLO detects → bbox (0.78 conf) → Track ID #1 confirmed
Frame 4: YOLO detects → bbox (0.81 conf) → Track ID #1 → CONFIRMED
Frame 5: GPS matched → INCIDENT CREATED
```

---

## 🗄️ Database Design

### Schema: Shared Incident Table + JSONB Module Data

A single `incidents` table serves **all modules** — using `module_id` as discriminator and `module_data` (JSONB) for module-specific fields:

```
┌──────────────────────────────────────────────────┐
│ DEVICES                                          │
├──────────────────────────────────────────────────┤
│ id            UUID PK                            │
│ device_name   VARCHAR(128)                       │
│ device_type   VARCHAR(32)  "bus|patrol|drone"    │
│ identifier    VARCHAR(64)  UNIQUE                │
│ is_active     BOOLEAN                            │
│ metadata      JSONB                              │
│ created_at    TIMESTAMP                          │
└──────────────────────┬───────────────────────────┘
                       │ 1:N
┌──────────────────────▼───────────────────────────┐
│ DETECTION_SESSIONS                                │
├──────────────────────────────────────────────────┤
│ id            UUID PK                            │
│ device_id     UUID FK → devices                  │
│ status        VARCHAR(16)  "active|paused|done"  │
│ runtime_mode  VARCHAR(16)  "edge|server"         │
│ module_id     VARCHAR(64)                        │
│ metadata      JSONB                              │
│ started_at    TIMESTAMP                          │
│ ended_at      TIMESTAMP                          │
└──────────────────────┬───────────────────────────┘
                       │ 1:N
┌──────────────────────▼───────────────────────────┐
│ INCIDENTS  (shared across ALL modules)            │
├──────────────────────────────────────────────────┤
│ id              UUID PK                          │
│ session_id      UUID FK → detection_sessions     │
│ module_id       VARCHAR(64) INDEX                │
│ incident_type   VARCHAR(64) INDEX                │
│ confidence      FLOAT                            │
│ severity        VARCHAR(16) "low|med|high|crit"  │
│ tracking_id     INTEGER                          │
│ latitude        FLOAT                            │
│ longitude       FLOAT                            │
│ gps_accuracy    FLOAT                            │
│ bounding_box    JSONB                            │
│ model_version   VARCHAR(64)                      │
│ runtime_mode    VARCHAR(16)                      │
│ status          VARCHAR(32) INDEX                │
│ module_data     JSONB  ◄── per-module extension  │
│ detected_at     TIMESTAMP INDEX                  │
│ created_at      TIMESTAMP                        │
│ updated_at      TIMESTAMP                        │
├──────────────────────────────────────────────────┤
│ INDEXES:                                         │
│   ix_incidents_module_type (module_id, type)     │
│   ix_incidents_location (lat, lng)               │
│   ix_incidents_detected_at (detected_at)         │
│   ix_incidents_status (status)                   │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│ MODULES                                          │
├──────────────────────────────────────────────────┤
│ id VARCHAR(64) PK │ name │ version │ status │    │
│ config JSONB │ registered_at │ updated_at        │
└──────────────────────────────────────────────────┘
```

### Why This Design

| Design Decision | Rationale |
|---|---|
| Single shared `incidents` table | Cross-module analytics, unified dashboard, simpler queries |
| JSONB `module_data` column | Module-specific fields without schema-per-module table sprawl |
| PostGIS `geometry` column (optional) | Efficient spatial queries, radius-based deduplication |
| Composite indexes | Fast filtering by module + type, location, time |

### Module-Specific JSONB Example (ROADSCAN AI)

```json
{
  "pothole_area_px": 12450,
  "road_surface_type": "asphalt",
  "detection_frame_count": 8,
  "inference_latency_ms": 45.2,
  "frame_dimensions": [640, 480]
}
```

---

## 🌐 API Design

### Core Platform APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/login` | JWT authentication |
| `POST` | `/api/v1/auth/register` | User registration |
| `GET` | `/api/v1/modules` | List registered modules + health |
| `GET` | `/api/v1/modules/{id}/health` | Module health check |
| `GET` | `/api/v1/incidents` | Query incidents cross-module (filterable) |
| `GET` | `/api/v1/incidents/{id}` | Get specific incident |
| `PATCH` | `/api/v1/incidents/{id}` | Update incident status |
| `POST` | `/api/v1/sessions` | Create detection session |
| `GET` | `/api/v1/devices` | List fleet devices |
| `GET` | `/api/v1/analytics/summary` | Platform-wide analytics |
| `GET` | `/api/v1/health` | Platform health check |
| `WS` | `/ws/incidents` | Real-time incident stream |
| `WS` | `/ws/status` | System status stream |

### Module APIs (auto-mounted under `/api/v1/{module_id}/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/roadscan_ai/incidents` | Create pothole incident (from edge) |
| `GET` | `/api/v1/roadscan_ai/incidents` | Query pothole incidents |
| `GET` | `/api/v1/roadscan_ai/incidents/stats` | Statistics |
| `GET` | `/api/v1/roadscan_ai/config` | Detection configuration |
| `PUT` | `/api/v1/roadscan_ai/config` | Update thresholds |
| `GET` | `/api/v1/roadscan_ai/model/info` | Model metadata |

> Future modules get the same pattern: `/api/v1/traffic_monitor/...`, `/api/v1/flood_detection/...`

---

## 🔌 Real-Time Communication

### WebSocket Channel Architecture

```
WebSocket Hub (Connection Manager)
    │
    ├── incidents:*             → All incidents (cross-module)
    ├── incidents:roadscan_ai   → Pothole incidents only
    ├── incidents:traffic       → Future traffic module
    │
    ├── status:platform         → Platform-wide health
    ├── status:roadscan_ai      → Module-specific status
    │
    └── detection:roadscan_ai   → Live detection feed (high-freq)
```

**Wildcard propagation**: Broadcasting to `incidents:roadscan_ai` automatically also notifies subscribers on `incidents:*`.

### Event Types

| Event | Trigger | Channel |
|-------|---------|---------|
| `incident.created` | New confirmed detection | `incidents:{module}` |
| `incident.updated` | Status change | `incidents:{module}` |
| `module.status_changed` | Module online/offline | `status:{module}` |
| `session.started` | New scan session | `status:platform` |
| `detection.frame` | Each inference result | `detection:{module}` |

---

## 🔐 Security Architecture

| Layer | Mechanism |
|-------|-----------|
| **Authentication** | JWT tokens with refresh rotation |
| **Authorization** | Role-based (admin, operator, viewer) |
| **API Security** | Rate limiting per endpoint, CORS whitelist |
| **Data Privacy** | Raw video never leaves device (edge mode). Only structured metadata transmitted |
| **Input Validation** | Pydantic schemas validate all API inputs |
| **SQL Injection** | SQLAlchemy ORM with parameterized queries |
| **WebSocket** | Authenticated connections, max connection limits |
| **Configuration** | Secrets via environment variables, never in code |
| **Crash Isolation** | Inference exceptions caught — never crash the API server |
| **Resource Limits** | Max sessions, max connections, max queue size, max resolution |

---

## 📈 Scalability & Performance

### Horizontal Scaling Path

```
Phase 1 (MVP):      Single server, all modules
Phase 2 (City):     Load-balanced API, separate DB
Phase 3 (National): Modules as microservices, message queue, CDN for models
```

### Performance Targets

| Metric | Target |
|--------|--------|
| Video display | 20-30 FPS (device-dependent) |
| Inference FPS | 5-15 FPS (adaptive) |
| Detection latency | < 1 second end-to-end |
| Incident creation | < 2 seconds after confirmation |
| API response time | < 100ms for queries |
| WebSocket latency | < 50ms for broadcasts |
| Concurrent devices | 10-50 (MVP), 1000+ (production) |

### Why Edge AI Enables Scale

| Devices | Server Mode Cost | Edge Mode Cost |
|---------|-----------------|----------------|
| 10 | 1 GPU server | 1 small API server |
| 100 | 10 GPU servers | 1 medium API server |
| 1,000 | 100 GPU servers (💰💰💰) | 2-3 API servers |

Edge mode shifts compute to the phones — the backend only handles metadata, making the system **orders of magnitude cheaper to scale**.

---

## 🚀 Deployment Strategy

### Development

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

### Production (Docker)

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [db]
    env_file: .env

  frontend:
    build: ./frontend
    ports: ["5173:80"]

  db:
    image: postgis/postgis:16-3.4
    volumes: [pgdata:/var/lib/postgresql/data]
    environment:
      POSTGRES_DB: smartcity
```

### CI/CD Pipeline

```
Push to GitHub
    → GitHub Actions: Lint + Test
    → Build Docker images
    → Deploy to cloud (Railway / Render / AWS)
```

---

## ⚠️ Feasibility & Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Edge inference too slow on target Android | HIGH | Medium | Server-mode fallback; adaptive FPS; model quantization |
| ONNX export breaks `best.pt` | HIGH | Low | Validate early; keep PyTorch runtime as backup |
| WebGPU not available on target device | MEDIUM | Medium | WebGL → WASM fallback chain |
| Browser memory crash with model | HIGH | Medium | Size validation; INT8 quantization; auto-fallback |
| GPS accuracy insufficient for dedup | MEDIUM | Low | Configurable thresholds; manual merge UI |
| Tracker ID reset → duplicate incidents | MEDIUM | High | Spatial+temporal dedup independent of tracker |
| FastAPI crash from inference exception | HIGH | Medium | Process isolation; global exception handler |
| Database write storms | MEDIUM | Low | Rate limiting; batch inserts; queue buffering |

### Technical Feasibility Decision Gate

Before final architecture lock, these questions must be answered by benchmarking:

1. Can `best.pt` export to ONNX successfully?
2. Does ONNX Runtime Web work on target Android Chrome?
3. What FPS is achieved on the actual target device?
4. Does the browser remain stable during sustained operation?
5. Can video remain smooth while inference runs?
6. Does the device remain thermally stable?

---

## 🌍 Social Impact & Sustainability

### Direct Impact

| Beneficiary | Impact |
|-------------|--------|
| **Citizens** | Safer roads, fewer pothole accidents, faster repairs |
| **Municipalities** | Real-time infrastructure monitoring at 1/100th the cost of manual surveys |
| **Public Transit** | Bus fleets become automatic road scanners — no extra cost |
| **Emergency Services** | Automated alerts for critical road damage |

### SDG Alignment

| UN SDG | Contribution |
|--------|-------------|
| **SDG 9** — Industry, Innovation, Infrastructure | AI-powered infrastructure monitoring |
| **SDG 11** — Sustainable Cities | Real-time urban road health data |
| **SDG 3** — Good Health | Reduction in pothole-related accidents |
| **SDG 13** — Climate Action | Edge computing reduces cloud energy consumption |

### Cost Comparison

| Approach | Cost per 100 km surveyed |
|----------|--------------------------|
| Manual inspection team | ₹50,000 - ₹1,00,000 |
| Dedicated survey vehicle | ₹2,00,000 - ₹5,00,000 |
| **ROADSCAN AI (bus fleet)** | **₹0 (marginal)** — uses existing phones and buses |

### Sustainability

- **No special hardware** — works on existing Android phones
- **No continuous cloud costs** — edge inference eliminates GPU cloud bills
- **Crowdsourceable** — any citizen can contribute via the web app
- **Extensible** — same platform monitors flood zones, traffic violations, etc.

---

## 🛠️ Tech Stack Justification

| Component | Technology | Why This Choice |
|-----------|------------|-----------------|
| **Backend** | FastAPI (Python) | Async, ML ecosystem compatibility, auto-generated docs, WebSocket support |
| **Frontend** | React + Vite | Component ecosystem, fast HMR, large community, PWA capable |
| **Database** | PostgreSQL + PostGIS | Spatial queries for geo-incident dedup, JSONB for module-specific data, battle-tested |
| **AI Framework** | YOLO (Ultralytics) | State-of-the-art real-time detection, export to ONNX/TensorRT |
| **Edge Runtime** | ONNX Runtime Web | Browser-native ML inference, WebGPU/WebGL/WASM backends |
| **Tracking** | ByteTrack | Lightweight, works with YOLO outputs, suitable for JS port |
| **Maps** | Leaflet | Open-source, mobile-friendly, GeoJSON native |
| **Real-Time** | WebSocket (native) | Bi-directional, low-latency, FastAPI-native |
| **Auth** | JWT (python-jose) | Stateless, scalable, standard |
| **ORM** | SQLAlchemy (async) | Type-safe queries, Alembic migrations, async support |

---

## 📁 Project Structure

```
MedAura/
├── Readme.md                          # This file — architecture + journal
├── .env.example                       # Environment configuration template
├── .gitignore                         # Git exclusions
│
├── backend/                           # ═══ FastAPI Backend ═══
│   ├── main.py                        # Application entrypoint + lifecycle
│   ├── config.py                      # Global configuration (pydantic-settings)
│   ├── requirements.txt               # Python dependencies
│   ├── core/                          # Shared platform core
│   │   ├── module_interface.py        # ★ Module contract (ABC)
│   │   ├── module_registry.py         # ★ Auto-discovery & lifecycle
│   │   ├── database.py                # Async SQLAlchemy setup
│   │   ├── models/                    # DB models (incident, session, device, module)
│   │   ├── schemas/                   # Pydantic validation schemas
│   │   ├── routes/                    # Core API routes (health, incidents, modules)
│   │   ├── middleware/                # Error handler, auth, rate limiting
│   │   └── websocket/                 # WebSocket hub + channels
│   ├── ai/                            # AI runtime abstraction layer
│   │   ├── runtime_interface.py       # ★ Abstract runtime contract
│   │   └── pytorch_runtime.py         # PyTorch/Ultralytics implementation
│   └── modules/                       # Detection modules
│       └── roadscan_ai/               # ★ First module: pothole detection
│           ├── manifest.py            # Implements ModuleInterface
│           ├── config.py              # Module-specific thresholds
│           └── routes/                # Module API endpoints
│
├── frontend/                          # ═══ React (Vite) Frontend ═══
│   ├── src/
│   │   ├── main.jsx                   # App entrypoint
│   │   ├── App.jsx                    # Router + module routes
│   │   └── index.css                  # Design system (dark mode, glass UI)
│   ├── package.json
│   └── vite.config.js
│
├── models/                            # AI models (gitignored)
│   └── best.pt                        # Source of truth YOLO model
│
└── frontend/public/models/            # Edge inference models (gitignored)
```

> **★** = Core extensibility files. These are the contracts that make adding new modules trivial.

---

## ⚙️ Configuration Architecture

All thresholds, model paths, and runtime parameters are **environment-driven, not hardcoded**.

### Platform Configuration (.env)

```env
# Platform
APP_NAME=SmartCity-Platform
APP_ENV=development
SECRET_KEY=...
CORS_ORIGINS=http://localhost:5173

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/smartcity

# AI Runtime
AI_RUNTIME=pytorch           # pytorch | onnx | tensorrt | edge
AI_MODEL_PATH=models/best.pt
AI_CONFIDENCE_THRESHOLD=0.5
AI_IOU_THRESHOLD=0.45
AI_INFERENCE_RESOLUTION=640
AI_MAX_INFERENCE_FPS=15

# Incident Deduplication
INCIDENT_SPATIAL_DEDUP_METERS=10
INCIDENT_TEMPORAL_DEDUP_SECONDS=30
INCIDENT_COOLDOWN_SECONDS=60

# Resource Limits
MAX_CONCURRENT_SESSIONS=10
MAX_WEBSOCKET_CONNECTIONS=50
MAX_FRAME_QUEUE_SIZE=3
```

### Module-Specific Config (ROADSCAN AI)

```json
{
  "confidence_threshold": 0.5,
  "severity_thresholds": {
    "low":      { "confidence_min": 0.5,  "area_max": 5000 },
    "medium":   { "confidence_min": 0.65, "area_max": 15000 },
    "high":     { "confidence_min": 0.75, "area_max": 30000 },
    "critical": { "confidence_min": 0.85 }
  },
  "gps_accuracy_threshold_m": 15.0
}
```

---

## 📅 Implementation Roadmap

### Phase 1 — Planning & Design ✅ COMPLETE
- [x] Workspace inspection & requirements analysis
- [x] Modular architecture design (plugin system)
- [x] Data flow design (edge + server modes)
- [x] Database schema design
- [x] API boundary design
- [x] AI runtime abstraction design
- [x] Frontend module system design
- [x] Risk assessment (8 risks with mitigations)
- [x] Implementation roadmap

### Phase 2 — Foundation (Week 1-2)
- [ ] Core backend: FastAPI app, database, Alembic migrations
- [ ] Module interface & registry (working auto-discovery)
- [ ] Core frontend: Vite React, design system, layout shell
- [ ] Health check endpoints
- [ ] JWT authentication

### Phase 3 — ROADSCAN AI Module (Week 3-5)
- [ ] `best.pt` model inspection & ONNX export
- [ ] PyTorch + ONNX runtime implementations
- [ ] ByteTrack integration
- [ ] Incident engine (creation, dedup, persistence)
- [ ] Camera feed + canvas overlay (React)
- [ ] GPS integration
- [ ] WebSocket real-time updates

### Phase 4 — Edge AI & Dashboard (Week 5-7)
- [ ] ONNX Runtime Web + browser capability detection
- [ ] JS ByteTrack implementation
- [ ] Adaptive frame scheduling
- [ ] Edge ↔ Server mode switching
- [ ] Leaflet map with incident visualization
- [ ] Analytics dashboard
- [ ] Alert system

### Phase 5 — Polish & Demo (Week 7-8)
- [ ] Performance optimization & benchmarking
- [ ] Crash resilience testing
- [ ] Offline queue (optional)
- [ ] UI/UX polish
- [ ] Video file test mode
- [ ] SIH demonstration preparation

---

## 📝 Architecture Decision Records

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | **Modular monolith with plugin interface** | Extensible without complexity of microservices. Modules isolated via contracts. |
| ADR-002 | **Shared incident table + JSONB** | Cross-module analytics. No per-module table sprawl. PostgreSQL JSONB is indexable. |
| ADR-003 | **Edge inference primary, server fallback** | 99.99% bandwidth reduction. Privacy. Scalability. Offline capability. |
| ADR-004 | **FastAPI + React (Vite)** | Async Python for ML. React ecosystem for UI. Vite for fast dev. |
| ADR-005 | **PostgreSQL + PostGIS** | Spatial queries for geo-dedup. Production-grade. Open source. |
| ADR-006 | **AI runtime abstraction** | Swap PyTorch/ONNX/TensorRT without code changes. Benchmark-driven. |
| ADR-007 | **WebSocket hub with channels** | Real-time dashboard. Per-module subscriptions. Wildcard propagation. |
| ADR-008 | **Adaptive frame scheduling** | Latest-frame-only. No infinite queues. Device-responsive. |
| ADR-009 | **Config-driven thresholds** | Every threshold configurable via env/API. No hardcoding. |
| ADR-010 | **No fake detections** | Real model, real inference, real GPS. System credibility. |

---

## 🧩 Adding Future Modules — Developer Guide

### To add a new module (e.g., `traffic_monitor`):

**Backend (~6 files):**
```
backend/modules/traffic_monitor/
├── __init__.py
├── manifest.py        ← Implement ModuleInterface
├── config.py          ← Module-specific thresholds
└── routes/
    ├── __init__.py
    ├── detection.py   ← Config/model endpoints
    └── incidents.py   ← Module incident CRUD
```

**Frontend (~4 files):**
```
frontend/src/modules/traffic_monitor/
├── index.js           ← Registration object
├── pages/
│   ├── MonitorView.jsx
│   └── TrafficMap.jsx
```

**Modify 2 existing files:**
- `backend/modules/__init__.py` (or auto-discovered)
- `frontend/src/App.jsx` (add routes)

**Core platform files changed: 0**

---

## 📖 Detailed Technical Specification

<details>
<summary><strong>Click to expand the full 35-section technical specification</strong></summary>

### 1. Architectural Objective

The ROADSCAN AI system must prioritize:

1. Real-time detection
2. Low latency
3. Stable continuous video
4. Low bandwidth consumption
5. Low backend CPU/GPU load
6. Resistance to backend crashes during demonstrations
7. Reliable operation on Android
8. Real YOLO inference
9. Accurate incident generation
10. Graceful degradation when hardware or network conditions are poor

### Architecture Options Evaluated

**Option A — Backend inference**: Android camera → video stream → FastAPI → YOLO → ByteTrack → metadata → overlay

**Option B — Edge/browser inference** (selected as primary): Android camera → browser → local YOLO → ByteTrack → Canvas overlay. Only metadata sent to FastAPI.

**Option C — Hybrid inference**: Local video + lightweight inference on Android, FastAPI handles incident processing + database + GIS + alerts.

**Option D — Native Android edge inference**: Future option using TFLite/ONNX Runtime mobile. Only if browser-based proves inadequate.

### 2. Model Integrity

The actual model is `models/best.pt`. Never auto-replace with YOLOv8n, YOLO11n, etc. The architecture must first inspect: model architecture, parameter count, input resolution, class names, confidence behavior, inference speed, training framework compatibility, supported export formats.

### 3-5. Runtime Evaluation

**PyTorch/Ultralytics**: Simplest, development use. **ONNX Runtime**: Benchmark CPU and GPU vs PyTorch. **TensorRT**: Optional for NVIDIA environments.

### 6-7. Browser Edge AI

Evaluate ONNX Runtime Web with WebGPU → WebGL → CPU/WASM fallback chain. Browser downloads model once, phone performs inference locally.

### 8. Edge Advantages

Bandwidth (metadata vs video), latency (local vs round-trip), resilience (offline capable), scalability (compute on phones), privacy (video stays on device).

### 9. Edge Limitations

Must test: Android GPU performance, WebGPU support, model loading time, browser memory, thermal throttling, battery consumption, inference FPS, tab stability.

### 10. Edge Model Optimization

Reduced resolution, FP16, INT8 quantization, ONNX graph optimization, batch=1, async inference, frame skipping, adaptive FPS. Balance accuracy vs speed vs stability.

### 11-12. Adaptive Inference & Frame Queue

Camera 30 FPS, inference 5-15 FPS. Latest-frame strategy — discard stale frames. Bounded queue prevents infinite growth. Low latency over process-every-frame.

### 13. Tracking on Edge

Prefer YOLO + ByteTrack on phone where performance permits. Avoids transmitting per-frame detections. Fallback: tracker on backend if mobile CPU cost too high.

### 14. Video Overlay Architecture

Camera → HTML video, simultaneously Camera frame → inference → detection → Canvas. Video never travels to FastAPI. Frontend owns: video, camera, canvas, detection, tracking, visualization. Backend owns: sessions, incidents, persistence, GIS, alerts.

### 15. GPS + Edge AI

GPS independent from inference. Continuous GPS updates. Never wait for GPS before processing video. GPS unavailable → detection continues → incident pending until location available.

### 16. Backend Role in Edge Architecture

FastAPI provides: session management, incident API, database, real-time dashboard, alerts, configuration, health checks. Not a video-processing bottleneck.

### 17. Fallback Backend-Inference Mode

Retained for unsupported devices, low-end phones, incompatible WebGPU, large models, browser memory constraints. UI indicates active mode (EDGE vs SERVER).

### 18. Video File Test Mode

Shares code with actual AI pipeline: Video Source (camera or file) → Frame Provider → Preprocessing → YOLO → ByteTrack → Incident Engine.

### 19. Model Benchmarking

Fixed validation video. Same model, resolution, hardware, thresholds. Measure: FPS, latency, RAM, CPU, GPU, temperature, detection consistency.

### 20. Target Performance

Video: 20-30 FPS. AI: 5-15 FPS. Detection latency: sub-second. Backend: responsive even when inference unavailable.

### 21. Crash Prevention

YOLO exception must never crash FastAPI. Isolated inference worker. If inference fails: AI status ERROR, backend still alive, dashboard accessible, database accessible.

### 22. Resource Limits

Max video resolution, inference resolution, queue size, concurrent sessions, WebSocket connections, database write rate, email rate.

### 23. Incident Rate Limiting

Same tracking ID + same spatial region + short time window = same incident. Spatial distance threshold + temporal threshold as configuration values.

### 24. Network Failure

Edge mode: internet disconnected → camera/AI/GPS continue → incidents queued locally → sync when online. Use IndexedDB for metadata queues.

### 25. Offline-First Demo Mode

AI: LOCAL, GPS: LOCAL, Network: OPTIONAL, Backend: SYNC WHEN AVAILABLE. Minimum viable resilience: temporary metadata queue + retry.

### 26. Data Sent to Backend

In edge mode: incident ID, bus ID, tracking ID, confidence, severity, lat/lng, GPS accuracy, timestamp, device/session ID, model version, runtime mode. NOT raw video.

### 27. Model Versioning

Every incident records model version and runtime. Enables comparison when `best.pt` changes.

### 28. Configuration

All parameters configurable: confidence threshold, IoU threshold, inference resolution, inference FPS, tracking threshold, confirmation frames, dedup distance, cooldown, GPS accuracy threshold.

### 29. Recommended Architecture

Primary: Android Chrome → camera → local YOLO → ByteTrack → Canvas → GPS → FastAPI metadata → PostgreSQL/PostGIS → Leaflet dashboard.

Fallback: Camera → video/WebRTC → FastAPI → YOLO → ByteTrack → PostgreSQL.

### 30. Decision Gate

12-point feasibility test before architecture lock (export, browser compatibility, FPS, latency, memory, stability, thermal).

### 31. Architectural Principle

Optimize for REAL-TIME RESPONSIVENESS, not MAXIMUM MODEL COMPLEXITY.

### 32. SIH Demo Priority

Continuous camera → real detection → live boxes → stable tracking → GPS → incidents → map → low latency → stability → clear states.

### 33. UI System Status

Real values only: AI ENGINE (EDGE/SERVER/NOT CONFIGURED), MODEL, INFERENCE FPS, GPS accuracy, NETWORK status.

### 34. Architecture Decision Records

10 ADRs documented with context, decision, reasoning, alternatives, consequences.

### 35. Final Rule

Optimize based on REAL MODEL + REAL DEVICE + REAL VIDEO + REAL LATENCY + REAL FPS + REAL GPS + REAL NETWORK. Benchmark first, then select runtime. Architecture modular enough that YOLO runtime can be replaced without redesigning the application.

</details>

---

# 📓 DEVELOPMENT JOURNAL

> Maintained per README instructions. Every significant change is documented here for continuity.

---

## Journal Entry #1 — 2026-09-30 (Phase 1: Planning & Design)

**Author**: AI Assistant

### What was done:
1. **Inspected workspace** — Found only Readme.md with 35-section ROADSCAN AI spec
2. **Clarified project scope** — Smart City Infrastructure Monitoring Platform, ROADSCAN AI as first module, designed for future module expansion
3. **Confirmed tech stack** — FastAPI (Python) + React (Vite) + PostgreSQL/PostGIS
4. **Designed complete modular architecture**:
   - Module plugin interface (`ModuleInterface` ABC)
   - Module registry (auto-discovery, validation, lifecycle)
   - Directory structure (backend + frontend)
   - Data flow for Edge mode and Server mode
   - Database schema (shared incident table + JSONB)
   - Full API design (core + module-specific)
   - AI runtime abstraction (PyTorch, ONNX, TensorRT, Edge)
   - Frontend module registration system
   - Configuration architecture (env-driven)
   - WebSocket real-time hub
5. **Created initial scaffolding** (backend core, module contract, ROADSCAN AI module skeleton, Vite React app)
6. **Risk assessment** — 8 risks with mitigations
7. **5-phase implementation roadmap**
8. **10 Architecture Decision Records**

### Files created:
- `backend/main.py`, `config.py`, `requirements.txt`
- `backend/core/` — module_interface, module_registry, database, models, schemas, routes, websocket
- `backend/ai/` — runtime_interface, pytorch_runtime
- `backend/modules/roadscan_ai/` — manifest, config, routes
- `frontend/` — Vite React app with react-router-dom, axios, leaflet, lucide-react
- `.gitignore`, `.env.example`

**No fake detections, no simulated inference, no placeholder data.**

### Next steps (Phase 2):
- Complete backend foundation with working module discovery
- Frontend layout shell with design system
- JWT authentication
- Database migrations with Alembic

---

## 📅 Session Journal: Phase 2 Completed (Implementation MVP)

### What was achieved:
- **Backend Architecture Fully Operational:**
  - FastApi server fully functioning with `aiosqlite`.
  - Removed PostgreSQL-specific constraints (UUID/JSONB) to allow local edge execution via SQLite.
  - Resolved Windows Terminal Unicode encoding bugs to allow seamless startup.
  - Dynamic module loading (`module_registry.py`) is successfully injecting the ROADSCAN AI endpoints.
- **Frontend App Built and Deployed:**
  - Modern, responsive React/Vite dashboard deployed live on Vercel!
  - Fully integrated layout with dynamic routing (Dashboard, ScanView, Map, Reports).
  - OpenStreetMap integrated with CSS-based dark-mode filter (No API key needed).
  - `ScanView` connects to device camera `navigator.mediaDevices.getUserMedia` for Edge AI foundation.
- **Deployment Strategy:**
  - Frontend hosted on Vercel.
  - Backend prepared with `Procfile` for Railway/Render hosting to support persistent DB and WebSockets.

### Next steps (Phase 3):
- Deploy backend to Railway/Render.
- Proxy frontend API requests to live backend URL.
- Load `best.onnx` into `ScanView` using ONNX Runtime Web for true offline edge inference.

---

**⚠️ IMPORTANT FOR NEXT DEVELOPER:**
- Do NOT create fake/simulated pothole detections
- Do NOT substitute `best.pt` with a generic YOLO model without benchmarking
- All thresholds must remain configurable (see Configuration Architecture)
- The `ModuleInterface` contract must be respected when adding new modules
- Phase 2 should follow the directory structure defined above
]]>