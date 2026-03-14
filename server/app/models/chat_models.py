from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.models.analysis_models import AnalysisResult


class ChatMessage(BaseModel):
    """A single turn in the conversation between the user and the AI assistant."""

    role: Literal["user", "assistant"] = Field(
        description="Author of the message — either the end user or the AI assistant"
    )
    content: str = Field(description="Text content of the message")
    timestamp: float | None = Field(
        default=None,
        description="Unix epoch time when the message was created",
    )


class ChatRequest(BaseModel):
    """Request payload for a chat turn submitted to the AI assistant."""

    message: str = Field(description="The user's latest message text")
    api_key: str = Field(description="Anthropic API key supplied by the user (BYOK)")
    conversation_history: list[ChatMessage] = Field(
        default_factory=list,
        description="All prior messages in the session, oldest first",
    )
    analysis_context: AnalysisResult | None = Field(
        default=None,
        description="Optional analysis result to provide as context to the AI",
    )


class ChatResponse(BaseModel):
    """Response payload returned after each AI chat turn."""

    message: str = Field(description="The AI assistant's reply text")
    conversation_history: list[ChatMessage] = Field(
        description="Updated conversation history including the new exchange"
    )
