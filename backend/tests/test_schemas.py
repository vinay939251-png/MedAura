"""
Tests for Pydantic schema validation — boundary values and edge cases.

Validates:
- Confidence must be between 0.0 and 1.0
- GPS coordinates must be in valid ranges
- Severity must be one of: low, medium, high, critical
- Runtime mode must be edge or server
- Bounding box structure validation
- Required field enforcement
"""

import pytest
from pydantic import ValidationError

from core.schemas.incident import IncidentCreate, IncidentUpdate, IncidentFilter


class TestIncidentCreateSchema:
    """Tests for IncidentCreate Pydantic schema."""

    def test_valid_incident_create(self):
        """Valid incident data should pass validation."""
        incident = IncidentCreate(
            module_id="roadscan_ai",
            incident_type="pothole",
            confidence=0.85,
            severity="high",
            latitude=17.385044,
            longitude=78.486671,
        )
        assert incident.module_id == "roadscan_ai"
        assert incident.confidence == 0.85

    def test_confidence_below_zero_rejected(self):
        """Confidence below 0.0 should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=-0.1,
                latitude=17.0,
                longitude=78.0,
            )
        assert "confidence" in str(exc_info.value).lower()

    def test_confidence_above_one_rejected(self):
        """Confidence above 1.0 should be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=1.5,
                latitude=17.0,
                longitude=78.0,
            )
        assert "confidence" in str(exc_info.value).lower()

    def test_confidence_boundary_zero(self):
        """Confidence of exactly 0.0 should be accepted."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.0,
            latitude=17.0,
            longitude=78.0,
        )
        assert incident.confidence == 0.0

    def test_confidence_boundary_one(self):
        """Confidence of exactly 1.0 should be accepted."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=1.0,
            latitude=17.0,
            longitude=78.0,
        )
        assert incident.confidence == 1.0

    def test_latitude_out_of_range_rejected(self):
        """Latitude outside [-90, 90] should be rejected."""
        with pytest.raises(ValidationError):
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                latitude=91.0,
                longitude=78.0,
            )

    def test_latitude_negative_boundary(self):
        """Latitude of -90 should be accepted."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.5,
            latitude=-90.0,
            longitude=0.0,
        )
        assert incident.latitude == -90.0

    def test_longitude_out_of_range_rejected(self):
        """Longitude outside [-180, 180] should be rejected."""
        with pytest.raises(ValidationError):
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                latitude=17.0,
                longitude=200.0,
            )

    def test_longitude_negative_boundary(self):
        """Longitude of -180 should be accepted."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.5,
            latitude=0.0,
            longitude=-180.0,
        )
        assert incident.longitude == -180.0

    def test_invalid_severity_rejected(self):
        """Invalid severity value should be rejected."""
        with pytest.raises(ValidationError):
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                severity="extreme",  # Not a valid severity
                latitude=17.0,
                longitude=78.0,
            )

    def test_valid_severity_values(self):
        """All valid severity values should be accepted."""
        for severity in ["low", "medium", "high", "critical"]:
            incident = IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                severity=severity,
                latitude=17.0,
                longitude=78.0,
            )
            assert incident.severity == severity

    def test_invalid_runtime_mode_rejected(self):
        """Invalid runtime_mode should be rejected."""
        with pytest.raises(ValidationError):
            IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                runtime_mode="cloud",  # Not valid
                latitude=17.0,
                longitude=78.0,
            )

    def test_valid_runtime_modes(self):
        """Both 'edge' and 'server' should be accepted."""
        for mode in ["edge", "server"]:
            incident = IncidentCreate(
                module_id="test",
                incident_type="pothole",
                confidence=0.5,
                runtime_mode=mode,
                latitude=17.0,
                longitude=78.0,
            )
            assert incident.runtime_mode == mode

    def test_missing_required_fields_rejected(self):
        """Missing required fields should raise validation error."""
        with pytest.raises(ValidationError):
            IncidentCreate()  # Missing all required fields

    def test_missing_module_id_rejected(self):
        """Missing module_id should raise validation error."""
        with pytest.raises(ValidationError):
            IncidentCreate(
                incident_type="pothole",
                confidence=0.5,
                latitude=17.0,
                longitude=78.0,
            )

    def test_bounding_box_optional(self):
        """Bounding box should be optional."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.5,
            latitude=17.0,
            longitude=78.0,
        )
        assert incident.bounding_box is None

    def test_bounding_box_with_valid_data(self):
        """Bounding box with valid coordinates should be accepted."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.5,
            latitude=17.0,
            longitude=78.0,
            bounding_box={"x1": 10.0, "y1": 20.0, "x2": 100.0, "y2": 200.0},
        )
        assert incident.bounding_box["x1"] == 10.0

    def test_module_data_optional(self):
        """Module data should be optional."""
        incident = IncidentCreate(
            module_id="test",
            incident_type="pothole",
            confidence=0.5,
            latitude=17.0,
            longitude=78.0,
        )
        assert incident.module_data is None


class TestIncidentUpdateSchema:
    """Tests for IncidentUpdate Pydantic schema."""

    def test_valid_status_update(self):
        """Valid status update should pass."""
        update = IncidentUpdate(status="resolved")
        assert update.status == "resolved"

    def test_invalid_status_rejected(self):
        """Invalid status value should be rejected."""
        with pytest.raises(ValidationError):
            IncidentUpdate(status="pending")  # Not a valid status

    def test_all_valid_statuses(self):
        """All valid status values should be accepted."""
        for status in ["detected", "confirmed", "resolved", "false_positive"]:
            update = IncidentUpdate(status=status)
            assert update.status == status

    def test_partial_update_allowed(self):
        """Partial updates (only some fields) should be allowed."""
        update = IncidentUpdate(severity="critical")
        assert update.severity == "critical"
        assert update.status is None


class TestIncidentFilterSchema:
    """Tests for IncidentFilter Pydantic schema."""

    def test_empty_filter_valid(self):
        """Empty filter (no constraints) should be valid."""
        f = IncidentFilter()
        assert f.module_id is None
        assert f.min_confidence is None

    def test_filter_with_all_fields(self):
        """Filter with all fields populated should be valid."""
        f = IncidentFilter(
            module_id="roadscan_ai",
            incident_type="pothole",
            severity="high",
            status="detected",
            min_confidence=0.7,
            lat_min=17.0,
            lat_max=18.0,
            lng_min=78.0,
            lng_max=79.0,
        )
        assert f.module_id == "roadscan_ai"
        assert f.min_confidence == 0.7

    def test_filter_min_confidence_boundary(self):
        """Filter confidence must be between 0 and 1."""
        with pytest.raises(ValidationError):
            IncidentFilter(min_confidence=1.5)
