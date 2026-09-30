"""
Session Routes — Detection session management.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/")
async def create_session():
    """Create a new detection session."""
    # TODO: Implement with DB integration
    return {"message": "Session creation — to be implemented in Phase 2"}


@router.get("/")
async def list_sessions():
    """List all detection sessions."""
    return {"items": [], "total": 0}


@router.get("/{session_id}")
async def get_session(session_id: str):
    """Get a detection session."""
    raise HTTPException(status_code=404, detail="Session not found")


@router.patch("/{session_id}")
async def update_session(session_id: str):
    """Update session status (pause/end)."""
    return {"message": f"Session {session_id} update — to be implemented in Phase 2"}
