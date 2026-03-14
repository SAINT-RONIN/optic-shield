"""Prompt builder that assembles full message arrays for the Anthropic chat API."""

from __future__ import annotations

from app.models.chat_models import ChatRequest
from app.prompts.analysis_prompt import serialize_analysis_context
from app.prompts.system_prompt import get_system_prompt

_CONTEXT_PREAMBLE: str = (
    "The user has completed a video safety analysis. "
    "The following data is the full analysis result. "
    "Use this as your factual reference for all answers in this conversation."
)


def _build_context_injection(request: ChatRequest) -> list[dict[str, str]]:
    """Return a user/assistant message pair that seeds analysis context."""
    if request.analysis_context is None:
        return []

    context_text = serialize_analysis_context(request.analysis_context)
    user_turn: dict[str, str] = {
        "role": "user",
        "content": f"{_CONTEXT_PREAMBLE}\n\n{context_text}",
    }
    assistant_ack: dict[str, str] = {
        "role": "assistant",
        "content": (
            "Understood. I have reviewed the analysis data and I am ready to answer "
            "questions about this video's safety profile."
        ),
    }
    return [user_turn, assistant_ack]


def _build_history_messages(request: ChatRequest) -> list[dict[str, str]]:
    """Convert ChatMessage history into Anthropic API message dicts."""
    return [
        {"role": msg.role, "content": msg.content}
        for msg in request.conversation_history
    ]


def build_chat_messages(request: ChatRequest) -> list[dict[str, str]]:
    """Build the full message array for an Anthropic API chat call.

    Message order:
    1. Analysis context injection (user + assistant pair) if context is present
    2. Prior conversation history
    3. Current user message
    """
    messages: list[dict[str, str]] = []
    messages.extend(_build_context_injection(request))
    messages.extend(_build_history_messages(request))
    messages.append({"role": "user", "content": request.message})
    return messages
