"""Pure view-model for render tests. Streamlit never chooses an urgency category."""
from dataclasses import dataclass
from careguide.schemas import Category, Decision


@dataclass(frozen=True)
class Banner:
    heading: str
    instruction: str
    prominent: bool
    kind: str


def banner_for(decision: Decision) -> Banner:
    headings = {
        Category.EMERGENCY: "DEMONSTRATION EMERGENCY ESCALATION — ACT NOW IF REAL",
        Category.URGENT: "DEMONSTRATION URGENT FLAG — PROFESSIONAL ASSESSMENT",
        Category.PROVIDER_FAILURE: "SERVICE / OUTPUT FAILURE — NO ASSESSMENT",
        Category.CLINICIAN_REFERRAL: "INSUFFICIENT INFORMATION — SEEK PROFESSIONAL ASSESSMENT",
        Category.CLARIFICATION: "CLARIFICATION REQUEST — NO URGENCY DETERMINATION",
        Category.UNSUPPORTED: "OUTSIDE THE DEMONSTRATION'S SCOPE",
        Category.GENERAL_INFO: "SYNTHETIC INFORMATION ONLY — NO CLINICAL CLEARANCE",
    }
    return Banner(heading=headings[decision.category], instruction=decision.message,
                  prominent=decision.category in {Category.EMERGENCY, Category.URGENT},
                  kind=decision.category.value)
