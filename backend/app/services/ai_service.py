import logging
import json
import anthropic

from app.core.config import settings
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_client: anthropic.AsyncAnthropic | None = None

_AE_SYSTEM_PROMPT = (
    "You are an AI assistant supporting a clinical trial management system (CTMS) "
    "for adverse event (AE) triage. This is a demonstration tool — your output is "
    "NOT a final medical determination and must always be reviewed by a qualified "
    "clinician before any action is taken.\n\n"
    "When given an adverse event description, respond ONLY with a JSON object — "
    "no extra text, no markdown fences — in exactly this format:\n"
    '{"risk_level": "Low" | "Monitor" | "Serious", "reasoning": "<one or two sentences>"}\n\n'
    "Guidelines:\n"
    "- Low: mild, expected, self-limiting events with no action required\n"
    "- Monitor: moderate or unexpected events that need closer observation\n"
    "- Serious: severe, life-threatening, or events meeting SAE criteria"
)


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        if not settings.ANTHROPIC_API_KEY:
            raise RuntimeError("ANTHROPIC_API_KEY is not set — add it to .env")
        _client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client


async def ask_claude(prompt: str, system_prompt: str | None = None) -> str:
    """Call Claude and return the text response.

    Raises RuntimeError on API failure so callers can handle it gracefully.
    """
    kwargs: dict = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    try:
        response = await _get_client().messages.create(**kwargs)
        return response.content[0].text
    except anthropic.AuthenticationError as exc:
        logger.error("Anthropic auth error — check ANTHROPIC_API_KEY: %s", exc)
        raise RuntimeError("AI service unavailable (auth)") from exc
    except anthropic.RateLimitError as exc:
        logger.error("Anthropic rate limit hit: %s", exc)
        raise RuntimeError("AI service unavailable (rate limit)") from exc
    except Exception as exc:
        logger.error("Anthropic API error: %s", exc)
        raise RuntimeError(f"AI service unavailable: {exc}") from exc


async def _assess_ae_risk_standalone(ae_data: dict) -> dict | None:
    """Build an AE risk prompt, call Claude, parse the JSON response.

    Args:
        ae_data: dict with keys matching AdverseEvent fields
                 (event_term, severity, seriousness, causality,
                  expectedness, outcome, description, action_taken)

    Returns:
        {"risk_level": str, "reasoning": str, "flagged_at": datetime} or None on failure.
    """
    prompt_parts = [
        f"Adverse event term: {ae_data.get('event_term', 'unknown')}",
        f"Severity reported: {ae_data.get('severity', 'unknown')}",
        f"Seriousness: {ae_data.get('seriousness', 'unknown')}",
        f"Causality assessment: {ae_data.get('causality', 'unknown')}",
        f"Expectedness: {ae_data.get('expectedness', 'unknown')}",
        f"Outcome: {ae_data.get('outcome', 'unknown')}",
    ]
    if ae_data.get("description"):
        prompt_parts.append(f"Description: {ae_data['description']}")
    if ae_data.get("action_taken"):
        prompt_parts.append(f"Action taken: {ae_data['action_taken']}")

    prompt = (
        "Please assess the risk level of the following adverse event and return JSON:\n\n"
        + "\n".join(prompt_parts)
    )

    raw = ""
    try:
        raw = await ask_claude(prompt, system_prompt=_AE_SYSTEM_PROMPT)
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        assessment = json.loads(cleaned)
        risk_level = assessment.get("risk_level", "").strip()
        reasoning = assessment.get("reasoning", "").strip()

        if risk_level not in ("Low", "Monitor", "Serious"):
            logger.warning("AI returned unexpected risk_level %r — ignoring", risk_level)
            return None

        return {
            "risk_level": risk_level,
            "reasoning": reasoning,
            "flagged_at": datetime.now(timezone.utc),
        }
    except json.JSONDecodeError:
        logger.warning("AI response was not valid JSON. Response: %r", raw[:200])
        return None
    except RuntimeError as exc:
        logger.warning("AI service unavailable: %s", exc)
        return None
    except Exception as exc:
        logger.warning("Unexpected error during AE risk assessment: %s", exc)
        return None

