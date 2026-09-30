"""
Runtime Interface — Abstract base for all AI inference backends.

This abstraction allows swapping between PyTorch, ONNX, TensorRT,
and Edge runtimes without changing any module code.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Detection:
    """A single object detection result."""
    class_id: int
    class_name: str
    confidence: float
    x1: float  # top-left x
    y1: float  # top-left y
    x2: float  # bottom-right x
    y2: float  # bottom-right y

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1

    @property
    def center(self) -> tuple:
        return ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

    @property
    def area(self) -> float:
        return self.width * self.height

    def to_dict(self) -> dict:
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "confidence": round(self.confidence, 4),
            "bbox": {
                "x1": round(self.x1, 2),
                "y1": round(self.y1, 2),
                "x2": round(self.x2, 2),
                "y2": round(self.y2, 2),
            },
            "area": round(self.area, 2),
        }


@dataclass
class ModelInfo:
    """Metadata about a loaded model."""
    architecture: str = ""
    parameter_count: int = 0
    input_resolution: int = 640
    class_names: Dict[int, str] = field(default_factory=dict)
    num_classes: int = 0
    model_size_mb: float = 0.0
    framework: str = ""
    export_formats: List[str] = field(default_factory=list)


@dataclass
class BenchmarkResult:
    """Results from a runtime benchmark."""
    runtime_name: str = ""
    model_load_time_ms: float = 0.0
    first_inference_ms: float = 0.0
    avg_inference_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    fps: float = 0.0
    ram_usage_mb: float = 0.0
    cpu_utilization: float = 0.0
    detection_count: int = 0
    frames_processed: int = 0


class RuntimeInterface(ABC):
    """
    Abstract base class for all AI inference runtimes.

    Implementations:
    - PyTorchRuntime: Uses Ultralytics/PyTorch directly
    - ONNXRuntime: Uses ONNX Runtime (CPU/GPU)
    - TensorRTRuntime: Uses NVIDIA TensorRT (optional)
    - EdgeRuntimeConfig: Provides config for browser-side ONNX Runtime Web
    """

    @abstractmethod
    async def load_model(self, model_path: str, config: Dict[str, Any]) -> None:
        """
        Load a model from the given path.
        Config includes: confidence_threshold, iou_threshold, inference_resolution
        """

    @abstractmethod
    async def infer(self, frame) -> List[Detection]:
        """
        Run inference on a single frame (numpy array).
        Returns list of Detection objects.
        """

    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        """Return metadata about the currently loaded model."""

    @abstractmethod
    async def benchmark(self, video_path: str, num_frames: int = 100) -> BenchmarkResult:
        """
        Run a benchmark against a test video.
        Returns timing metrics, FPS, resource usage.
        """

    @abstractmethod
    async def unload(self) -> None:
        """Release model resources (GPU memory, etc.)."""

    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if a model is currently loaded and ready for inference."""
