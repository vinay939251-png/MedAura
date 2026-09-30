import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter to prevent API abuse.
    Limits requests per IP per minute.
    """
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.ip_records = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        
        # Clean up old records for this IP
        self.ip_records[client_ip] = [
            timestamp for timestamp in self.ip_records[client_ip] 
            if now - timestamp < self.window_seconds
        ]
        
        # Check rate limit
        if len(self.ip_records[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please slow down."}
            )
            
        self.ip_records[client_ip].append(now)
        
        response = await call_next(request)
        return response
