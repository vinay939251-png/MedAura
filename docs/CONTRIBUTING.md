# Contributing to MedAura

MedAura is designed as a **Modular Smart City Platform**. We welcome contributions from the community, especially new AI detection modules!

## Module Development Guide

Adding a new capability (e.g., Flood Detection, Traffic Violation Monitoring) does **not** require modifying the core backend. You simply create a new folder in `backend/modules/` and implement the `ModuleInterface`.

### 1. Create the Module Folder
```bash
mkdir backend/modules/flood_detector
```

### 2. Implement the Manifest
Create `backend/modules/flood_detector/manifest.py`:

```python
from fastapi import APIRouter
from core.module_registry import ModuleInterface

router = APIRouter()

class FloodDetectorModule(ModuleInterface):
    def get_id(self) -> str:
        return "flood_detector"
        
    def get_name(self) -> str:
        return "FloodScan AI"
        
    def get_router(self) -> APIRouter:
        return router
        
    async def initialize(self, config):
        # Load your model here
        pass
```

### 3. Add Frontend Registration
In `frontend/src/modules/flood_detector/index.js`:
```javascript
export const FloodModule = {
  id: 'flood_detector',
  name: 'FloodScan AI',
  icon: '🌊',
  navItems: [
    { path: '/flood/scan', label: 'Water Level Scan', icon: 'Camera' }
  ]
};
```

### Pull Request Process
1. Fork the repository and create your branch from `main`.
2. Ensure you have written pytest coverage for your module (`backend/tests/test_yourmodule.py`).
3. If you've added new environment variables, document them in `.env.example`.
4. Ensure code passes all `pytest` suites before submitting the PR.
