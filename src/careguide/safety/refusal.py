"""Out-of-scope requests; escalate BEFORE checking refusals."""
import re

UNSUPPORTED = re.compile(
    r"\b(?:diagnos(?:e|is)|prescrib(?:e|ing)|dosage|dose of|stop taking|discontinue|"
    r"change my medication|rule out|medical clearance|clear me|pretend to be a doctor)\b",
    flags=re.I,
)
INJECTION = re.compile(
    r"\b(?:ignore (?:your|all|the) (?:medical )?(?:safety )?rules|"
    r"always classify|do not mention emergency services|"
    r"never escalate|override safety rules)\b", flags=re.I,
)


def is_unsupported(text: str) -> bool:
    return bool(UNSUPPORTED.search(text) or INJECTION.search(text))
