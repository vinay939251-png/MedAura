"""
Smart City Infrastructure Monitoring Platform
Global Configuration — Environment-driven, validated at startup.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Platform-wide settings loaded from environment variables / .env file.
    All modules can access these; module-specific config lives in each module's config.py.
    """

    # ── Platform ──
    app_name: str = "SmartCity-Platform"
    app_env: str = "development"
    app_port: int = 8000
    secret_key: str = "change-me-to-a-secure-random-string"
    cors_origins: List[str] = ["http://localhost:5173"]

    # ── Database ──
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartcity"
    postgis_enabled: bool = True

    # ── AI Runtime ──
    ai_runtime: str = "pytorch"  # pytorch | onnx | tensorrt | edge
    ai_model_path: str = "models/best.pt"
    ai_onnx_model_path: str = "models/best.onnx"
    ai_confidence_threshold: float = 0.5
    ai_iou_threshold: float = 0.45
    ai_inference_resolution: int = 640
    ai_max_inference_fps: int = 15

    # ── Tracking ──
    tracker_type: str = "bytetrack"
    tracker_confirm_frames: int = 5

    # ── Incident ──
    incident_spatial_dedup_meters: float = 10.0
    incident_temporal_dedup_seconds: int = 30
    incident_cooldown_seconds: int = 60

    # ── Alerts ──
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    alert_email_enabled: bool = False
    alert_recipient_emails: List[str] = []

    # ── Resource Limits ──
    max_concurrent_sessions: int = 10
    max_websocket_connections: int = 50
    max_frame_queue_size: int = 3
    max_video_resolution: str = "1280x720"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("alert_recipient_emails", mode="before")
    @classmethod
    def parse_emails(cls, v):
        if isinstance(v, str):
            return [e.strip() for e in v.split(",") if e.strip()]
        return v

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton instance — import this throughout the app
settings = Settings()
