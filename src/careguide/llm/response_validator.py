"""Allow-list model categories plus conservative text-level rejection.

This filter is a defense in depth, NOT proof that natural-language claims are safe.
"""
import re
from pydantic import ValidationError

from careguide.schemas import Category, ModelProposal

FORBIDDEN = re.compile(
    r"\b(?:you (?:have|definitely have|don't have) (?:a |an )?(?:disease|condition|diagnosis)|"
    r"you (?:are|will be) (?:definitely )?(?:fine|safe)|"
    r"no (?:risk|emergency)|rule[ds]? out|"
    r"(?:take|stop taking|increase|decrease) \d+ ?(?:mg|ml)|"
    r"i am (?:a |your )?(?:doctor|physician))\b", re.I,
)


class UnsafeProposal(ValueError):
    pass


def validate_proposal(raw: str, *, expected_category: Category, allowed_rule_ids: set[str]) -> ModelProposal:
    try:
        proposal = ModelProposal.model_validate_json(raw)
    except (ValidationError, ValueError) as exc:
        raise UnsafeProposal("provider schema invalid") from exc
    if expected_category != Category.GENERAL_INFO or proposal.proposed_response_category != expected_category:
        raise UnsafeProposal("provider may not determine triage category")
    if proposal.follow_up_question or proposal.missing_information or proposal.refusal:
        raise UnsafeProposal("provider requested unsupported dialogue change")
    if proposal.escalation_recommendation is not None:
        raise UnsafeProposal("provider proposed unauthorized escalation category")
    if not set(proposal.referenced_rule_ids).issubset(allowed_rule_ids):
        raise UnsafeProposal("unknown or spoofed rule ID")
    if FORBIDDEN.search(proposal.user_message):
        raise UnsafeProposal("unsafe certainty, diagnosis or treatment language")
    return proposal
