"""Deterministic orchestration. Each provider interaction follows core rule assessment."""
from __future__ import annotations

from typing import Protocol as Interface

from pydantic import ValidationError

from careguide.clinical_rules.engine import RuleEngine
from careguide.clinical_rules.escalation import locked_escalation
from careguide.config import AppConfig, Policy
from careguide.conversation.session import Session
from careguide.conversation.state import State
from careguide.llm.anthropic_client import ProviderReply
from careguide.llm.response_validator import validate_proposal
from careguide.logging.safe_log import log_event
from careguide.safety.guardrails import contradictory
from careguide.safety.policy import fail_closed
from careguide.safety.refusal import is_unsupported
from careguide.schemas import Category, Decision, Input, Protocol


class LanguageProvider(Interface):
    def generate(self, *, narrative: str, rule_ids: list[str], instruction: str) -> ProviderReply: ...


class TriageService:
    def __init__(self, *, app: AppConfig, policy: Policy, protocol: Protocol,
                 provider: LanguageProvider | None = None):
        self.app = app
        self.policy = policy
        self.engine = RuleEngine(protocol)
        self.protocol = protocol
        self.provider = provider

    def _finish(self, session: Session, decision: Decision, target: State) -> Decision:
        session.move(target)
        decision.state = session.state.value
        if target in (State.EMERGENCY, State.URGENT):
            session.sticky_decision = decision.model_copy(deep=True)
        session.record(decision)
        return decision

    def submit(self, session: Session, text: str) -> Decision:
        if session.expired(self.app.session_ttl_minutes):
            log_event("session_expired")
            raise ValueError("session expired: restart and accept disclosure")
        if session.state == State.DISCLOSURE:
            raise ValueError("disclosure must be accepted before use")
        if session.state == State.COMPLETE:
            raise ValueError("session is completed; restart")
        # An emergency latch is shown regardless of subsequent text (no model work).
        if session.state == State.EMERGENCY:
            assert session.sticky_decision is not None
            session.move(State.EMERGENCY)
            again = session.sticky_decision.model_copy(deep=True)
            session.record(again)
            return again
        # Check for higher-priority emergency even after urgent latch.
        try:
            narrative = Input(narrative=text).narrative
            if len(narrative) > self.app.max_input_chars:
                raise ValueError("input exceeds configured length")
        except (ValidationError, ValueError) as exc:
            log_event("validation_error")
            raise ValueError("Please enter a shorter, non-empty fictional scenario without control characters") from exc

        match = self.engine.evaluate(narrative)
        if match and match.category == Category.EMERGENCY:
            # Urgent -> emergency transition is permitted without EVALUATING.
            decision = locked_escalation(match, self.app.emergency_contact)
            if session.state == State.URGENT:
                return self._finish(session, decision, State.EMERGENCY)
            session.move(State.EVALUATING)
            return self._finish(session, decision, State.EMERGENCY)
        if session.state == State.URGENT:
            assert session.sticky_decision is not None
            session.move(State.URGENT)
            prior = session.sticky_decision.model_copy(deep=True)
            session.record(prior)
            return prior

        session.move(State.EVALUATING)
        log_event("rule_evaluated", category=(match.category.value if match else "none"))
        if match and match.category == Category.URGENT:
            return self._finish(session, locked_escalation(match, self.app.emergency_contact), State.URGENT)
        if contradictory(session, narrative):
            return self._finish(session, fail_closed(self.policy), State.CLINICIAN_REFERRAL)
        if is_unsupported(narrative):
            return self._finish(session, Decision(category=Category.UNSUPPORTED,
                                message=self.policy.unsupported_instruction), State.UNSUPPORTED)
        if match and match.category == Category.GENERAL_INFO:
            instruction = match.rules[0].user_instruction
            rule_ids = [r.id for r in match.rules]
            if self.app.mode == "offline_demo":
                return self._finish(session, Decision(category=Category.GENERAL_INFO,
                                    message=instruction, rule_ids=rule_ids), State.GENERAL_INFO)
            if not self.provider:
                return self._finish(session, fail_closed(self.policy, provider=True), State.PROVIDER_FAILURE)
            try:
                reply = self.provider.generate(narrative=narrative, rule_ids=rule_ids,
                                               instruction=instruction)
                p = validate_proposal(reply.text, expected_category=Category.GENERAL_INFO,
                                      allowed_rule_ids=set(rule_ids))
                return self._finish(session, Decision(category=Category.GENERAL_INFO,
                                    message=p.user_message + "\n\n" + instruction,
                                    rule_ids=rule_ids, provider_latency_ms=reply.latency_ms),
                                    State.GENERAL_INFO)
            except Exception:  # Any provider/validator exception is sanitized and fails closed.
                log_event("proposal_rejected")
                return self._finish(session, fail_closed(self.policy, provider=True), State.PROVIDER_FAILURE)
        if session.question_index < min(self.app.max_questions, len(self.protocol.questions)):
            q = self.protocol.questions[session.question_index]
            session.question_index += 1
            return self._finish(session, Decision(category=Category.CLARIFICATION,
                                message="A synthetic detail is missing; no urgency determination has been made.",
                                next_question=q.prompt), State.CLARIFICATION)
        return self._finish(session, fail_closed(self.policy), State.CLINICIAN_REFERRAL)
