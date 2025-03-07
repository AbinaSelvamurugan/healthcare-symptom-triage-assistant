"""Operational records contain event codes, no raw text, identities, key, or prompt."""
import logging

LOG = logging.getLogger("careguide")
EVENTS = {"validation_error", "rule_evaluated", "escalation", "fallback", "provider_failure",
          "session_started", "session_expired", "proposal_rejected"}


def log_event(event: str, *, category: str = "none") -> None:
    if event not in EVENTS or not category.replace("_", "").isalnum():
        raise ValueError("unsafe log event metadata")
    LOG.info("event=%s category=%s", event, category)
