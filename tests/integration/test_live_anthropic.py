"""Optional account-specific smoke test; never runs with the offline suite."""
import os
import pytest

from careguide.llm.anthropic_client import AnthropicProvider
from careguide.llm.response_validator import validate_proposal
from careguide.schemas import Category


@pytest.mark.live_api
def test_live_model_access_and_synthetic_json_contract():
    if os.getenv("CAREGUIDE_RUN_LIVE_API") != "1":
        pytest.skip("explicit CAREGUIDE_RUN_LIVE_API=1 required")
    provider = AnthropicProvider()
    assert provider.verify_model(), "model ID unavailable to authenticated account"
    reply = provider.generate(narrative="synthetic information marker",
                              rule_ids=["DEMO-INFO-MARKER"],
                              instruction="This is an educational software demonstration.")
    assert validate_proposal(reply.text, expected_category=Category.GENERAL_INFO,
                             allowed_rule_ids={"DEMO-INFO-MARKER"})
