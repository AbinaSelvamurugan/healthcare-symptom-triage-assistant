"""Detect limited contradictions without assuming silence or uncertain text means NO."""
import re
from careguide.conversation.session import Session

POS = re.compile(r"\bi have\s+(?:a|an)\s+([a-z]{3,18})\b", re.I)
NEG = re.compile(r"\b(?:i (?:do not|don't) have|i have no)\s+(?:a|an)?\s*([a-z]{3,18})\b", re.I)


def contradictory(session: Session, text: str) -> bool:
    # Heuristic restricted to simple syntactic contradictions; incomplete NLP coverage.
    for polarity, regex in (("yes", POS), ("no", NEG)):
        for item in regex.findall(text):
            session.signs.setdefault(item.lower(), set()).add(polarity)
    return any(len(polarities) > 1 for polarities in session.signs.values())
