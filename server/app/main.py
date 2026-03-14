import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket

from app.config import settings
from app.exceptions import OpticShieldError
from app.routers import analysis, chat, video, youtube

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Optic Shield AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api")
app.include_router(youtube.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(video.router, prefix="/api")


@app.exception_handler(OpticShieldError)
async def optic_shield_error_handler(
    request: Request, exc: OpticShieldError
) -> JSONResponse:
    """Convert domain exceptions into structured JSON error responses."""
    logger.error("Domain error [%s]: %s", exc.error_code, exc.message)
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "data": None,
            "error": exc.message,
            "error_code": exc.error_code.value,
        },
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple liveness probe response."""
    return {"status": "ok"}


@app.websocket("/ws/{video_id}")
async def websocket_endpoint(websocket: WebSocket, video_id: str) -> None:
    """WebSocket endpoint for real-time analysis progress updates."""
    from app.services.ws_manager import ws_manager
    await ws_manager.connect(video_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(video_id, websocket)


@app.on_event("startup")
async def on_startup() -> None:
    """Create the temp directory on application startup if it does not exist."""
    os.makedirs(settings.temp_dir, exist_ok=True)
    logger.info("Temp directory ensured: %s", settings.temp_dir)
