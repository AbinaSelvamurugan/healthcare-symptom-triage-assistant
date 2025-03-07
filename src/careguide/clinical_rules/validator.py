"""Protocol governance gate: demo rules may not masquerade as approved guidance."""
from careguide.schemas import Protocol


def demo_only(protocol: Protocol) -> None:
    if protocol.status != "DEMONSTRATION_ONLY":
        raise ValueError("No clinical governance approval or production protocol is provisioned")
    if any(rule.approval_status != "DEMONSTRATION_ONLY" for rule in protocol.rules):
        raise ValueError("Mixed/approved rules cannot run in the demonstration engine")
