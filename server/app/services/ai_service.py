"""AI service — all LLM interactions via the Anthropic Claude API (BYOK)."""

from __future__ import annotations

import logging

from anthropic import APIError, Anthropic, AuthenticationError

from app.models.analysis_models import AnalysisResult
from app.models.chat_models import ChatRequest
from app.prompts import (
    build_chat_messages,
    build_graph_explanation_prompt,
    build_report_prompt,
    get_system_prompt,
    serialize_analysis_context,
)

logger = logging.getLogger(__name__)

_FALLBACK_REPORT: str = "Analysis complete. See graphs for details."
_FALLBACK_CHAT: str = "I can only help with video accessibility analysis."
_FALLBACK_EXPLANATION: str = "Graph data is available. See the waveform for details."

_METRIC_THRESHOLDS: dict[str, str] = {
    "flash": "WCAG 2.1 SC 2.3.1 limit: 3 flashes/sec maximum",
    "red_flash": "W3C red flash rule: saturated red transitions above 0.2 intensity are hazardous",
    "luminance": "W3C threshold: luminance delta >0.2 between frames in the flash area",
    "motion": "High motion (>0.7 normalised intensity) may compound flash hazards",
    "scene_cut": "Rapid scene cuts (confidence >0.8) can mask flash accumulation",
    "color_cycle": "Hue cycling >180 deg/sec indicates rapid colour alternation hazard",
    "pattern": "Spatial pattern score >0.5 indicates >8 cycles per visual angle degree",
}


def _build_metric_summary(metric_name: str, analysis: AnalysisResult) -> str:
    """Extract a brief summary string for a single metric from the full analysis."""
    context = serialize_analysis_context(analysis)
    marker = f"--- {metric_name.upper().replace('_', ' ')} "
    start = context.find(marker)
    if start == -1:
        return "No data available for this metric."
    end = context.find("\n---", start + 1)
    section = context[start:end] if end != -1 else context[start:]
    return section.strip()


class AIServiceError(Exception):
    """Raised when an LLM call fails after all retries and fallbacks."""


class AIService:
    """Handles all LLM interactions using the Anthropic Claude API (BYOK)."""

    REPORT_MODEL: str = "claude-haiku-4-5-20251001"
    CHAT_MODEL: str = "claude-sonnet-4-5-20241022"
    MAX_REPORT_TOKENS: int = 2048
    MAX_CHAT_TOKENS: int = 1024
    MAX_EXPLANATION_TOKENS: int = 256

    def _make_client(self, api_key: str) -> Anthropic:
        """Create a new Anthropic client per request — key never stored."""
        return Anthropic(api_key=api_key)

    def _call_api(
        self,
        client: Anthropic,
        model: str,
        max_tokens: int,
        system: str,
        messages: list[dict[str, str]],
    ) -> str:
        """Perform a single synchronous Anthropic messages.create call."""
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text

    async def generate_report(
        self, analysis: AnalysisResult, api_key: str
    ) -> str:
        """Generate a narrative safety report from analysis results."""
        client = self._make_client(api_key)
        prompt = build_report_prompt(analysis)
        messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]

        try:
            return self._call_api(
                client,
                self.REPORT_MODEL,
                self.MAX_REPORT_TOKENS,
                get_system_prompt(),
                messages,
            )
        except AuthenticationError:
            logger.error("generate_report: Anthropic authentication failed")
            return _FALLBACK_REPORT
        except APIError as exc:
            logger.error("generate_report: Anthropic API error — %s", exc.status_code)
            return _FALLBACK_REPORT

    async def _explain_single_metric(
        self,
        client: Anthropic,
        metric_name: str,
        analysis: AnalysisResult,
    ) -> str:
        """Generate an explanation for one metric graph. Returns fallback on failure."""
        summary = _build_metric_summary(metric_name, analysis)
        threshold = _METRIC_THRESHOLDS.get(metric_name, "No specific threshold defined.")
        prompt = build_graph_explanation_prompt(metric_name, summary, threshold)
        messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]

        try:
            return self._call_api(
                client,
                self.REPORT_MODEL,
                self.MAX_EXPLANATION_TOKENS,
                get_system_prompt(),
                messages,
            )
        except AuthenticationError:
            logger.error("explain_metric '%s': authentication failed", metric_name)
            return _FALLBACK_EXPLANATION
        except APIError as exc:
            logger.error(
                "explain_metric '%s': API error — %s", metric_name, exc.status_code
            )
            return _FALLBACK_EXPLANATION

    async def generate_graph_explanations(
        self, analysis: AnalysisResult, api_key: str
    ) -> dict[str, str]:
        """Generate per-graph explanations for all metric types."""
        client = self._make_client(api_key)
        metric_names = list(_METRIC_THRESHOLDS.keys())
        explanations: dict[str, str] = {}

        for name in metric_names:
            explanations[name] = await self._explain_single_metric(
                client, name, analysis
            )

        return explanations

    async def chat(self, request: ChatRequest) -> str:
        """Process a chat turn and return the assistant reply."""
        client = self._make_client(request.api_key)
        messages = build_chat_messages(request)

        try:
            return self._call_api(
                client,
                self.CHAT_MODEL,
                self.MAX_CHAT_TOKENS,
                get_system_prompt(),
                messages,
            )
        except AuthenticationError:
            logger.error("chat: Anthropic authentication failed")
            return _FALLBACK_CHAT
        except APIError as exc:
            logger.error("chat: Anthropic API error — %s", exc.status_code)
            return _FALLBACK_CHAT
