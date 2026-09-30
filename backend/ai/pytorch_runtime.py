"""
PyTorch Runtime — Ultralytics YOLO inference backend.

This is the primary runtime for development and initial model validation.
Uses the Ultralytics library directly with best.pt.
"""

from typing import List, Dict, Any
import time

from ai.runtime_interface import RuntimeInterface, Detection, ModelInfo, BenchmarkResult


class PyTorchRuntime(RuntimeInterface):
    """
    YOLO inference using Ultralytics/PyTorch.

    Advantages: simplest integration, direct compatibility, easiest debugging.
    Disadvantages: higher runtime overhead, more RAM usage.
    Recommended use: Development and initial model validation.
    """

    def __init__(self):
        self._model = None
        self._model_info = ModelInfo()
        self._config = {}

    async def load_model(self, model_path: str, config: Dict[str, Any]) -> None:
        """Load a YOLO model using Ultralytics."""
        try:
            from ultralytics import YOLO
        except ImportError:
            raise RuntimeError(
                "Ultralytics not installed. Run: pip install ultralytics"
            )

        self._config = config
        self._model = YOLO(model_path)

        # Extract model info
        model_info = self._model.info(verbose=False)
        self._model_info = ModelInfo(
            architecture=str(getattr(self._model, 'task', 'detect')),
            class_names=self._model.names or {},
            num_classes=len(self._model.names) if self._model.names else 0,
            input_resolution=config.get("inference_resolution", 640),
            framework="ultralytics/pytorch",
        )

    async def infer(self, frame) -> List[Detection]:
        """Run YOLO inference on a numpy frame."""
        if self._model is None:
            return []

        results = self._model(
            frame,
            conf=self._config.get("confidence_threshold", 0.5),
            iou=self._config.get("iou_threshold", 0.45),
            imgsz=self._config.get("inference_resolution", 640),
            verbose=False,
        )

        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append(
                    Detection(
                        class_id=int(box.cls[0].item()),
                        class_name=self._model.names.get(int(box.cls[0].item()), "unknown"),
                        confidence=float(box.conf[0].item()),
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                    )
                )

        return detections

    def get_model_info(self) -> ModelInfo:
        return self._model_info

    async def benchmark(self, video_path: str, num_frames: int = 100) -> BenchmarkResult:
        """Benchmark against a test video."""
        import cv2
        import numpy as np

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")

        latencies = []
        total_detections = 0
        frames_processed = 0

        for _ in range(num_frames):
            ret, frame = cap.read()
            if not ret:
                break

            start = time.perf_counter()
            detections = await self.infer(frame)
            elapsed = (time.perf_counter() - start) * 1000  # ms

            latencies.append(elapsed)
            total_detections += len(detections)
            frames_processed += 1

        cap.release()

        if not latencies:
            return BenchmarkResult(runtime_name="pytorch")

        latencies.sort()
        return BenchmarkResult(
            runtime_name="pytorch",
            first_inference_ms=latencies[0],
            avg_inference_ms=sum(latencies) / len(latencies),
            p50_latency_ms=latencies[len(latencies) // 2],
            p95_latency_ms=latencies[int(len(latencies) * 0.95)],
            fps=1000 / (sum(latencies) / len(latencies)),
            detection_count=total_detections,
            frames_processed=frames_processed,
        )

    async def unload(self) -> None:
        """Release model resources."""
        self._model = None

    def is_loaded(self) -> bool:
        return self._model is not None
