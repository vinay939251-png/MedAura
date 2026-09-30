"""
Tests for the Detection dataclass — width, height, center, area computations.

Validates:
- Property calculations (width, height, center, area)
- Serialization to dict
- Boundary conditions (zero-area, negative coords)
- ModelInfo and BenchmarkResult dataclasses
"""

import pytest
from ai.runtime_interface import Detection, ModelInfo, BenchmarkResult


class TestDetectionDataclass:
    """Tests for the Detection dataclass and its computed properties."""

    def test_width_calculation(self):
        """Width should be x2 - x1."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.9,
                      x1=100.0, y1=50.0, x2=300.0, y2=250.0)
        assert d.width == 200.0

    def test_height_calculation(self):
        """Height should be y2 - y1."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.9,
                      x1=100.0, y1=50.0, x2=300.0, y2=250.0)
        assert d.height == 200.0

    def test_center_calculation(self):
        """Center should be midpoint of bbox."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.9,
                      x1=100.0, y1=50.0, x2=300.0, y2=250.0)
        cx, cy = d.center
        assert cx == pytest.approx(200.0)
        assert cy == pytest.approx(150.0)

    def test_area_calculation(self):
        """Area should be width * height."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.9,
                      x1=0.0, y1=0.0, x2=100.0, y2=50.0)
        assert d.area == pytest.approx(5000.0)

    def test_zero_area_detection(self):
        """Zero-area bbox (point detection) should return area 0."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.5,
                      x1=100.0, y1=100.0, x2=100.0, y2=100.0)
        assert d.area == 0.0
        assert d.width == 0.0
        assert d.height == 0.0

    def test_to_dict_structure(self):
        """to_dict should return correct structure."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.8765,
                      x1=10.0, y1=20.0, x2=110.0, y2=120.0)
        result = d.to_dict()

        assert result["class_id"] == 0
        assert result["class_name"] == "pothole"
        assert result["confidence"] == 0.8765
        assert "bbox" in result
        assert result["bbox"]["x1"] == 10.0
        assert result["bbox"]["y1"] == 20.0
        assert result["bbox"]["x2"] == 110.0
        assert result["bbox"]["y2"] == 120.0
        assert "area" in result
        assert result["area"] == pytest.approx(10000.0)

    def test_confidence_rounding_in_dict(self):
        """Confidence should be rounded to 4 decimal places in dict."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.123456789,
                      x1=0, y1=0, x2=10, y2=10)
        result = d.to_dict()
        assert result["confidence"] == 0.1235

    def test_bbox_rounding_in_dict(self):
        """Bbox coordinates should be rounded to 2 decimal places."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.9,
                      x1=10.123456, y1=20.789012, x2=30.456789, y2=40.111111)
        result = d.to_dict()
        assert result["bbox"]["x1"] == 10.12
        assert result["bbox"]["y1"] == 20.79

    def test_large_detection_area(self):
        """Large bounding box area should compute correctly."""
        d = Detection(class_id=0, class_name="pothole", confidence=0.95,
                      x1=0, y1=0, x2=1920, y2=1080)
        assert d.area == pytest.approx(1920 * 1080)

    def test_different_class_ids(self):
        """Detections with different class IDs should be distinguishable."""
        d1 = Detection(class_id=0, class_name="pothole", confidence=0.9,
                       x1=0, y1=0, x2=10, y2=10)
        d2 = Detection(class_id=1, class_name="crack", confidence=0.8,
                       x1=0, y1=0, x2=10, y2=10)
        assert d1.class_id != d2.class_id
        assert d1.class_name != d2.class_name


class TestModelInfoDataclass:
    """Tests for ModelInfo dataclass."""

    def test_default_values(self):
        """ModelInfo should have sensible defaults."""
        info = ModelInfo()
        assert info.architecture == ""
        assert info.parameter_count == 0
        assert info.input_resolution == 640
        assert info.num_classes == 0
        assert info.class_names == {}

    def test_custom_values(self):
        """ModelInfo should accept custom values."""
        info = ModelInfo(
            architecture="yolov8n",
            parameter_count=3200000,
            input_resolution=640,
            class_names={0: "pothole"},
            num_classes=1,
            framework="ultralytics/pytorch",
        )
        assert info.architecture == "yolov8n"
        assert info.num_classes == 1
        assert info.class_names[0] == "pothole"


class TestBenchmarkResultDataclass:
    """Tests for BenchmarkResult dataclass."""

    def test_default_values(self):
        """BenchmarkResult should have zero defaults."""
        result = BenchmarkResult()
        assert result.runtime_name == ""
        assert result.avg_inference_ms == 0.0
        assert result.fps == 0.0
        assert result.frames_processed == 0

    def test_custom_benchmark(self):
        """BenchmarkResult should store benchmark data."""
        result = BenchmarkResult(
            runtime_name="pytorch",
            avg_inference_ms=45.2,
            fps=22.1,
            detection_count=150,
            frames_processed=100,
        )
        assert result.runtime_name == "pytorch"
        assert result.fps == pytest.approx(22.1)
        assert result.detection_count == 150
