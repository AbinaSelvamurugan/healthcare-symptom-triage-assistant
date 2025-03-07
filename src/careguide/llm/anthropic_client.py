"""Official Anthropic SDK adapter. Loaded lazily so all offline tests need no SDK/key."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from time import perf_counter

from careguide.llm.prompt_builder import SYSTEM, user_content


class ProviderUnavailable(RuntimeError):
    """Sanitized provider failure, with no raw API exception or narrative."""


@dataclass(frozen=True)
class ProviderReply:
    text: str
    latency_ms: int


class AnthropicProvider:
    def __init__(self, *, model: str | None = None, timeout: float = 12,
                 max_retries: int = 1, client: object | None = None):
        self.model = model or os.getenv("ANTHROPIC_MODEL")
        self.timeout = timeout
        self.max_retries = max_retries
        if not self.model:
            raise ProviderUnavailable("model_not_configured")
        if client is not None:
            self.client = client
            return
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ProviderUnavailable("credentials_missing")
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"],
                                    timeout=timeout, max_retries=max_retries)
        except Exception as exc:  # sanitized at boundary
            raise ProviderUnavailable("client_initialization_failed") from exc

    def verify_model(self) -> bool:
        """Query active account's model access, not merely a published model catalogue."""
        try:
            info = self.client.models.retrieve(self.model)
            return getattr(info, "id", None) == self.model and getattr(info, "lifecycle", "active") != "retired"
        except Exception as exc:
            raise ProviderUnavailable("model_verification_failed") from exc

    def generate(self, *, narrative: str, rule_ids: list[str], instruction: str) -> ProviderReply:
        start = perf_counter()
        try:
            response = self.client.messages.create(
                model=self.model, max_tokens=450, temperature=0,
                system=SYSTEM,
                messages=[{"role": "user", "content": user_content(narrative, rule_ids, instruction)}],
            )
            blocks = getattr(response, "content", [])
            chunks = [b.text for b in blocks if getattr(b, "type", None) == "text"]
            if len(chunks) != 1:
                raise ValueError("unexpected blocks")
            # JSON decoding is also enforced by Pydantic after transport.
            json.loads(chunks[0])
            return ProviderReply(chunks[0], round((perf_counter() - start) * 1000))
        except Exception as exc:
            raise ProviderUnavailable("generation_failed") from exc
