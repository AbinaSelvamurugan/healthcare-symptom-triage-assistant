"""Short-lived, per-user in-memory state; no persistent symptom conversation."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from careguide.conversation.state import State, check_transition
from careguide.schemas import Decision


@dataclass
class Session:
    id: str = field(default_factory=lambda: uuid4().hex)
    state: State = State.DISCLOSURE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    transitions: list[tuple[str, str]] = field(default_factory=list)
    # These contain no narrative: only rule identifiers, state, and synthetic-label metadata.
    decision_trace: list[dict[str, object]] = field(default_factory=list)
    question_index: int = 0
    sticky_decision: Decision | None = None
    signs: dict[str, set[str]] = field(default_factory=dict)  # transient, not logged

    def move(self, state: State) -> None:
        check_transition(self.state, state)
        self.transitions.append((self.state.value, state.value))
        self.state = state

    def consent(self) -> None:
        self.move(State.COLLECTION)

    def complete(self) -> None:
        """End a non-escalated fictional workflow; reset creates a fresh disclosure."""
        self.move(State.COMPLETE)

    def expired(self, ttl_minutes: int, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.created_at + timedelta(minutes=ttl_minutes)

    def reset(self) -> Session:
        self.signs.clear()
        self.decision_trace.clear()
        self.transitions.clear()
        self.sticky_decision = None
        return Session()

    def record(self, decision: Decision) -> None:
        self.decision_trace.append({"category": decision.category.value,
                                    "rule_ids": list(decision.rule_ids),
                                    "validation_status": decision.validation_status,
                                    "state": self.state.value})
