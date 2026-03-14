"""WebSocket connection manager for broadcasting analysis progress."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections grouped by video_id."""

    def __init__(self) -> None:
        self._connections: dict[str, list[WebSocket]] = {}

    async def connect(self, video_id: str, websocket: WebSocket) -> None:
        """Register a WebSocket connection for a video analysis."""
        await websocket.accept()
        if video_id not in self._connections:
            self._connections[video_id] = []
        self._connections[video_id].append(websocket)
        logger.info("WebSocket connected for video_id=%s", video_id)

    def disconnect(self, video_id: str, websocket: WebSocket) -> None:
        """Remove a WebSocket connection."""
        if video_id in self._connections:
            self._connections[video_id] = [
                ws for ws in self._connections[video_id] if ws is not websocket
            ]
            if not self._connections[video_id]:
                del self._connections[video_id]

    async def send_progress(self, video_id: str, data: dict[str, Any]) -> None:
        """Broadcast a progress update to all connections for a video_id."""
        connections = self._connections.get(video_id, [])
        dead: list[WebSocket] = []
        for ws in connections:
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(video_id, ws)


ws_manager = ConnectionManager()
