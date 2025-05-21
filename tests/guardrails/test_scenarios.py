"""All cases evaluated offline; raw inputs are fictional and not logged."""
import json
import pytest
from careguide.reporting.scenarios import evaluate_case, make_metrics
from careguide.config import ROOT

CASES = json.loads((ROOT / "tests/fixtures/scenarios.v1.json").read_text())


@pytest.mark.parametrize("scenario", CASES, ids=lambda c: c["id"])
def test_guardrail_scenario(scenario):
    outcome = evaluate_case(scenario, ROOT)
    assert outcome["status"] == "PASS", outcome


def test_guardrail_suite_has_critical_coverage():
    results = [evaluate_case(c, ROOT) for c in CASES]
    metrics = make_metrics(results)
    assert metrics["missed_escalations"]["numerator"] == 0
    assert metrics["false_reassurance_count"]["numerator"] == 0
    assert metrics["state_transition_violations"]["numerator"] == 0
    assert {c["expected_rule"] for c in CASES if c.get("expected_rule", "").startswith("DEMO-EMERGENCY")} == {
        "DEMO-EMERGENCY-BREATHING", "DEMO-EMERGENCY-STROKE", "DEMO-EMERGENCY-CHEST",
        "DEMO-EMERGENCY-UNRESPONSIVE", "DEMO-EMERGENCY-BLEEDING"}
