"""
Session Routes — Detection session management.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def create_session():
    """Create a new detection session."""
    # TODO: Implement with DB integration
    return {"message": "Session creation — to be implemented in Phase 2"}


@router.get("/")
async def list_sessions():
    """List all detection sessions."""
    return {"sessions": [], "total": 0}


@router.patch("/{session_id}")
async def update_session(session_id: str):
    """Update session status (pause/end)."""
    return {"message": f"Session {session_id} update — to be implemented in Phase 2"}
