from careguide.config import Policy
from careguide.schemas import Category, Decision


def fail_closed(policy: Policy, *, provider: bool = False) -> Decision:
    return Decision(category=Category.PROVIDER_FAILURE if provider else Category.CLINICIAN_REFERRAL,
                    message=policy.provider_failure_instruction if provider else policy.uncertainty_instruction,
                    validation_status="fallback")
