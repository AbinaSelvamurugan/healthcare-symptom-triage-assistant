"""Explicit state machine. Emergency/urgent latches have no downgrade transition."""
from __future__ import annotations
from enum import StrEnum


class State(StrEnum):
    DISCLOSURE = "DISCLOSURE"
    COLLECTION = "COLLECTION"
    EVALUATING = "EVALUATING"
    CLARIFICATION = "CLARIFICATION"
    EMERGENCY = "EMERGENCY"
    URGENT = "URGENT"
    GENERAL_INFO = "GENERAL_INFO"
    CLINICIAN_REFERRAL = "CLINICIAN_REFERRAL"
    UNSUPPORTED = "UNSUPPORTED"
    PROVIDER_FAILURE = "PROVIDER_FAILURE"
    COMPLETE = "COMPLETE"


ALLOWED: dict[State, set[State]] = {
    State.DISCLOSURE: {State.COLLECTION},
    State.COLLECTION: {State.EVALUATING, State.COMPLETE},
    State.CLARIFICATION: {State.EVALUATING, State.COMPLETE},
    State.GENERAL_INFO: {State.EVALUATING, State.COMPLETE},
    State.CLINICIAN_REFERRAL: {State.EVALUATING, State.COMPLETE},
    State.UNSUPPORTED: {State.EVALUATING, State.COMPLETE},
    State.PROVIDER_FAILURE: {State.EVALUATING, State.COMPLETE},
    State.EVALUATING: {State.EMERGENCY, State.URGENT, State.CLARIFICATION, State.GENERAL_INFO,
                       State.CLINICIAN_REFERRAL, State.UNSUPPORTED, State.PROVIDER_FAILURE},
    State.EMERGENCY: {State.EMERGENCY},
    State.URGENT: {State.URGENT, State.EMERGENCY},
    State.COMPLETE: set(),
}


def check_transition(old: State, new: State) -> None:
    if new not in ALLOWED[old]:
        raise ValueError(f"invalid state transition: {old.value} -> {new.value}")
