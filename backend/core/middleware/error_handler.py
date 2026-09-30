"""
Global Exception Handler — Prevents unhandled exceptions from crashing the server.

Critical for demo stability: an inference crash should never take down FastAPI.
"""

import traceback
from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler.
    Logs the error and returns a structured JSON error response
    instead of crashing the entire server.
    """
    error_detail = str(exc)
    error_traceback = traceback.format_exc()

    # Log the error (replace with proper logging in production)
    print(f"❌ Unhandled exception on {request.method} {request.url}")
    print(f"   Error: {error_detail}")
    print(f"   Traceback:\n{error_traceback}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": error_detail if request.app.extra.get("debug") else None,
        },
    )
