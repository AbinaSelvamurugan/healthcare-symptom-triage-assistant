from careguide.schemas import Category, Decision
from careguide.clinical_rules.engine import Match


def locked_escalation(match: Match, emergency_contact: str | None) -> Decision:
    if match.category not in (Category.EMERGENCY, Category.URGENT):
        raise ValueError("requires escalation")
    instructions = list(dict.fromkeys(rule.user_instruction for rule in match.rules))
    message = "\n\n".join(instructions)
    if match.category == Category.EMERGENCY and emergency_contact:
        message += "\n\nConfigured local emergency contact: " + emergency_contact
    return Decision(category=match.category, message=message,
                    rule_ids=[rule.id for rule in match.rules])
