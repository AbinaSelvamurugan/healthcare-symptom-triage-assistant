"""Fake SDK contract and failure containment; no real network or credentials."""
import json
from types import SimpleNamespace
import pytest
from careguide.llm.anthropic_client import AnthropicProvider, ProviderUnavailable
from careguide.llm.response_validator import UnsafeProposal, validate_proposal
from careguide.schemas import Category


class FakeMessages:
    def __init__(self, should_fail=False):
        self.kwargs = None
        self.should_fail = should_fail

    def create(self, **kwargs):
        self.kwargs = kwargs
        if self.should_fail:
            raise RuntimeError("synthetic private token should not leak")
        reply = {"user_message": "Synthetic only, no assessment.",
                 "proposed_response_category": "GENERAL_INFO", "follow_up_question": None,
                 "missing_information": [], "referenced_rule_ids": ["DEMO-INFO-MARKER"],
                 "refusal": False, "escalation_recommendation": None,
                 "validation_status": "proposed"}
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps(reply))])


class FakeSDK:
    def __init__(self, fail=False):
        self.messages = FakeMessages(fail)
        self.models = SimpleNamespace(retrieve=lambda model: SimpleNamespace(id=model, lifecycle="active"))


def test_official_messages_sdk_shape_and_model_verification():
    sdk = FakeSDK()
    p = AnthropicProvider(model="configured-at-runtime", client=sdk)
    assert p.verify_model()
    r = p.generate(narrative="fictional input", rule_ids=["DEMO-INFO-MARKER"], instruction="Demo")
    assert r.latency_ms >= 0
    assert sdk.messages.kwargs["model"] == "configured-at-runtime"
    assert sdk.messages.kwargs["messages"][0]["role"] == "user"
    assert "fictional input" in sdk.messages.kwargs["messages"][0]["content"]
    assert validate_proposal(r.text, expected_category=Category.GENERAL_INFO,
                             allowed_rule_ids={"DEMO-INFO-MARKER"})


def test_provider_failure_sanitizes_exception():
    p = AnthropicProvider(model="fake-model", client=FakeSDK(fail=True))
    with pytest.raises(ProviderUnavailable, match="generation_failed") as exc:
        p.generate(narrative="private", rule_ids=[], instruction="demo")
    assert "synthetic private token" not in str(exc.value)


def test_missing_api_key_fails_before_network(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ProviderUnavailable, match="credentials_missing"):
        AnthropicProvider(model="test-model")


def test_no_model_fails(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
    with pytest.raises(ProviderUnavailable, match="model_not_configured"):
        AnthropicProvider()


def test_category_override_rejected():
    proposal = {"user_message": "No assessment", "proposed_response_category": "EMERGENCY",
                "follow_up_question": None, "missing_information": [],
                "referenced_rule_ids": [], "refusal": False, "escalation_recommendation": None,
                "validation_status": "proposed"}
    with pytest.raises(UnsafeProposal):
        validate_proposal(json.dumps(proposal), expected_category=Category.GENERAL_INFO,
                          allowed_rule_ids=set())
