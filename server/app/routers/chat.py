import logging
import time

from fastapi import APIRouter

from app.models.analysis_models import ApiResponse
from app.models.chat_models import ChatMessage, ChatRequest, ChatResponse
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

_ai_service = AIService()


@router.post("/", response_model=ApiResponse[ChatResponse])
async def chat(body: ChatRequest) -> ApiResponse[ChatResponse]:
    """Accept a user chat message and return an AI response."""
    logger.info("Chat message received, length=%d", len(body.message))

    if not body.api_key:
        return ApiResponse(
            success=False,
            error="API key is required for chat",
            error_code="MISSING_API_KEY",
        )

    ai_reply = await _ai_service.chat(body)

    user_msg = ChatMessage(role="user", content=body.message, timestamp=time.time())
    assistant_msg = ChatMessage(role="assistant", content=ai_reply, timestamp=time.time())
    updated_history = [*body.conversation_history, user_msg, assistant_msg]

    response = ChatResponse(message=ai_reply, conversation_history=updated_history)
    return ApiResponse(success=True, data=response)
