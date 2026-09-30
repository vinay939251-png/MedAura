"""
ROADSCAN AI — Module-Specific Configuration

All thresholds, model settings, and detection parameters live here.
These can be overridden via environment variables or the admin API.
"""

# ── Default Configuration ──
ROADSCAN_CONFIG = {
    "runtime_mode": "edge",  # edge | server
    "confidence_threshold": 0.5,
    "iou_threshold": 0.45,
    "inference_resolution": 640,
    "max_inference_fps": 15,

    # Tracking
    "tracker_confirm_frames": 5,
    "tracker_max_lost": 30,

    # Incident generation
    "incident_min_confidence": 0.6,
    "incident_spatial_dedup_meters": 10,
    "incident_temporal_dedup_seconds": 30,
    "incident_cooldown_seconds": 60,

    # GPS
    "gps_accuracy_threshold_m": 15.0,

    # Severity classification
    "severity_thresholds": {
        "low": {"confidence_min": 0.5, "area_max": 5000},
        "medium": {"confidence_min": 0.65, "area_max": 15000},
        "high": {"confidence_min": 0.75, "area_max": 30000},
        "critical": {"confidence_min": 0.85},
    },
}

# ── Config Schema (for admin UI form generation) ──
ROADSCAN_CONFIG_SCHEMA = {
    "confidence_threshold": {
        "type": "float",
        "label": "Confidence Threshold",
        "description": "Minimum confidence for a detection to be considered",
        "default": 0.5,
        "min": 0.1,
        "max": 1.0,
        "step": 0.05,
    },
    "iou_threshold": {
        "type": "float",
        "label": "IoU Threshold",
        "description": "Intersection-over-Union threshold for NMS",
        "default": 0.45,
        "min": 0.1,
        "max": 1.0,
        "step": 0.05,
    },
    "inference_resolution": {
        "type": "integer",
        "label": "Inference Resolution",
        "description": "Input image size for YOLO model",
        "default": 640,
        "options": [320, 416, 512, 640, 736, 832],
    },
    "max_inference_fps": {
        "type": "integer",
        "label": "Max Inference FPS",
        "description": "Maximum frames per second to process",
        "default": 15,
        "min": 1,
        "max": 30,
    },
    "gps_accuracy_threshold_m": {
        "type": "float",
        "label": "GPS Accuracy Threshold (m)",
        "description": "Maximum acceptable GPS accuracy for incident creation",
        "default": 15.0,
        "min": 1.0,
        "max": 100.0,
    },
    "incident_spatial_dedup_meters": {
        "type": "float",
        "label": "Spatial Dedup Distance (m)",
        "description": "Incidents within this distance are considered duplicates",
        "default": 10.0,
        "min": 1.0,
        "max": 100.0,
    },
}
