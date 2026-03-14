import logging
import time

from fastapi import APIRouter

from app.models.analysis_models import ApiResponse
from app.models.chat_models import ChatMessage, ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ApiResponse[ChatResponse])
async def chat(body: ChatRequest) -> ApiResponse[ChatResponse]:
    """Accept a user chat message and return an AI response."""
    logger.info("Chat message received, length=%d", len(body.message))
    echo_message = ChatMessage(
        role="assistant",
        content=f"Echo: {body.message}",
        timestamp=time.time(),
    )
    user_message = ChatMessage(
        role="user",
        content=body.message,
        timestamp=time.time(),
    )
    updated_history = [*body.conversation_history, user_message, echo_message]
    response = ChatResponse(
        message=echo_message.content,
        conversation_history=updated_history,
    )
    return ApiResponse(success=True, data=response)
