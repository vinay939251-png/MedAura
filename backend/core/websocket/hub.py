"""
WebSocket Hub — Central real-time communication manager.

Manages WebSocket connections, channels, and event broadcasting.
Modules broadcast events (new incidents, status changes) through this hub.
Dashboard and mobile clients subscribe to relevant channels.
"""

import json
from typing import Dict, Set, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from config import settings

websocket_router = APIRouter()


class ConnectionManager:
    """
    Manages WebSocket connections organized by channels.

    Channels follow the pattern:
    - "incidents:*"           → All incidents across modules
    - "incidents:roadscan_ai" → ROADSCAN AI incidents only
    - "status:platform"       → Platform-wide status
    - "status:roadscan_ai"    → Module-specific status
    """

    def __init__(self):
        # channel_name → set of active WebSocket connections
        self.channels: Dict[str, Set[WebSocket]] = {}
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, channel: str = "incidents:*"):
        """Accept a WebSocket connection and subscribe to a channel."""
        if len(self.active_connections) >= settings.max_websocket_connections:
            await websocket.close(code=1013, reason="Max connections reached")
            return False

        await websocket.accept()
        self.active_connections.add(websocket)

        if channel not in self.channels:
            self.channels[channel] = set()
        self.channels[channel].add(websocket)

        return True

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from all channels."""
        self.active_connections.discard(websocket)
        for channel_connections in self.channels.values():
            channel_connections.discard(websocket)

    async def broadcast_to_channel(self, channel: str, event: dict):
        """Send an event to all connections subscribed to a channel."""
        message = json.dumps(event)
        dead_connections = set()

        # Broadcast to specific channel
        for ws in self.channels.get(channel, set()):
            try:
                await ws.send_text(message)
            except Exception:
                dead_connections.add(ws)

        # Also broadcast to wildcard channel if it's a specific channel
        # e.g., "incidents:roadscan_ai" → also notify "incidents:*"
        parts = channel.split(":")
        if len(parts) == 2 and parts[1] != "*":
            wildcard = f"{parts[0]}:*"
            for ws in self.channels.get(wildcard, set()):
                try:
                    await ws.send_text(message)
                except Exception:
                    dead_connections.add(ws)

        # Clean up dead connections
        for ws in dead_connections:
            self.disconnect(ws)

    async def broadcast_all(self, event: dict):
        """Send an event to ALL connected clients."""
        message = json.dumps(event)
        dead_connections = set()

        for ws in self.active_connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead_connections.add(ws)

        for ws in dead_connections:
            self.disconnect(ws)

    @property
    def connection_count(self) -> int:
        return len(self.active_connections)


# Singleton instance — modules import this to broadcast events
ws_manager = ConnectionManager()


# ── WebSocket Endpoints ──

@websocket_router.websocket("/ws/incidents")
async def incident_stream(websocket: WebSocket, channel: Optional[str] = "incidents:*"):
    """
    Real-time incident stream.
    Clients can subscribe to:
    - incidents:*           → all modules
    - incidents:roadscan_ai → specific module
    """
    connected = await ws_manager.connect(websocket, channel or "incidents:*")
    if not connected:
        return

    try:
        while True:
            # Keep connection alive, listen for client messages
            data = await websocket.receive_text()
            # Clients can send subscription changes
            try:
                msg = json.loads(data)
                if msg.get("action") == "subscribe":
                    new_channel = msg.get("channel", "incidents:*")
                    ws_manager.channels.setdefault(new_channel, set()).add(websocket)
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@websocket_router.websocket("/ws/status")
async def status_stream(websocket: WebSocket):
    """Real-time platform status stream."""
    connected = await ws_manager.connect(websocket, "status:platform")
    if not connected:
        return

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
