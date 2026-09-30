from typing import Dict, Any

def calculate_severity(
    confidence: float, 
    bbox: Dict[str, float] = None, 
    thresholds: Dict[str, Any] = None
) -> str:
    """
    Classify incident severity based on confidence and bounding box area.
    
    Uses module-specific configuration thresholds if provided.
    """
    if not thresholds:
        # Default thresholds
        thresholds = {
            "low": {"confidence_min": 0.5, "area_max": 5000},
            "medium": {"confidence_min": 0.65, "area_max": 15000},
            "high": {"confidence_min": 0.75, "area_max": 30000},
            "critical": {"confidence_min": 0.85},
        }

    area = 0
    if bbox and all(k in bbox for k in ["x1", "y1", "x2", "y2"]):
        width = abs(bbox["x2"] - bbox["x1"])
        height = abs(bbox["y2"] - bbox["y1"])
        area = width * height

    # Determine severity based on criteria
    # We check from highest to lowest severity
    
    crit = thresholds.get("critical", {})
    if confidence >= crit.get("confidence_min", 0.85) and area > crit.get("area_min", 30000):
        return "critical"
        
    high = thresholds.get("high", {})
    if confidence >= high.get("confidence_min", 0.75) and area > high.get("area_min", 15000):
        return "high"
        
    med = thresholds.get("medium", {})
    if confidence >= med.get("confidence_min", 0.65) and area > med.get("area_min", 5000):
        return "medium"
        
    low = thresholds.get("low", {})
    if confidence >= low.get("confidence_min", 0.5):
        return "low"
        
    return "low"
