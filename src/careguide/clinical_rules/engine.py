"""Deterministic demo-only match engine; NEVER a clinical classifier."""
from __future__ import annotations

import re
from dataclasses import dataclass

from careguide.clinical_rules.validator import demo_only
from careguide.schemas import Category, Protocol, Rule

PRIORITY = {Category.EMERGENCY: 0, Category.URGENT: 1, Category.GENERAL_INFO: 2}


@dataclass(frozen=True)
class Match:
    category: Category
    rules: tuple[Rule, ...]


# Explicit, local negation immediately preceding the trigger. Not medical NLP.
NEGATION = re.compile(r"(?:\bno\s+|\bnot\s+|\bwithout\s+|\bdon't have\s+|\bdo not have\s+)$", re.I)


def _trigger_matches(text: str, phrase: str) -> bool:
    # A period in a configured trigger intentionally stands for a single punctuation
    # character; e.g. can.t matches can't. All other characters are escaped.
    pattern = r"(?<!\w)" + re.escape(phrase).replace(r"\.", r"[\W_]") + r"(?!\w)"
    for match in re.finditer(pattern, text, flags=re.I):
        if not NEGATION.search(text[max(0, match.start() - 25):match.start()]):
            return True
    return False


class RuleEngine:
    def __init__(self, protocol: Protocol):
        demo_only(protocol)
        self.protocol = protocol

    def evaluate(self, narrative: str) -> Match | None:
        matching = [r for r in self.protocol.rules
                    if any(_trigger_matches(narrative, t) for t in r.trigger_any)]
        if not matching:
            return None
        category = min((Category(r.escalation_category) for r in matching), key=PRIORITY.__getitem__)
        chosen = tuple(r for r in matching if r.escalation_category == category.value)
        return Match(category=category, rules=chosen)
