# Software testing methodology and metrics

Test fixture suite: `tests/fixtures/scenarios.v1.json`, version 1.0.0, all synthetic, with per-case IDs, description, messages, expected rule/category, required instruction, forbidden words, expected validation, attack tagging and provider behavior. `pytest` evaluates each case independently and uses deterministic fake SDK responses. Real Claude credentials are NOT used in the core tests. Separate optional live integration coverage must be explicitly opted into. The suite checks matching, precedence, emergency retention, invalid output rejection, refusals, provider failures, session transitions, metadata-only logs, and escalation presentation view-models.

Metrics are calculated from the actual case outcomes by `src/careguide/reporting/scenarios.py`, not hardcoded. For all metrics: the numerator and denominator are explicitly serialized in the JSON report; undefined denominators yield `null` rather than zero. Expected values are synthetic test targets, not clinical targets.

| Metric | Numerator | Denominator | Interpretation |
|---|---|---|---|
| Required escalation recall | exact-category matches | configured emergency + urgent scenarios | Synthetic rule expectation coverage, target 100% |
| Missed escalation count | expected escalation but got non-escalation | all mandatory synthetic escalation scenarios | Critical misses, target 0 |
| False reassurance | regex-detected false safety/clearance claims | all scenarios | Target 0; incomplete detector |
| Unauthorized diagnosis | regex-detected diagnosis claims | all scenarios | Target 0; incomplete detector |
| Unsupported treatment advice | regex-detected dose/treatment instructions | all scenarios | Target 0; incomplete detector |
| Refusal compliance | PASS on refusal cases | all refusal cases | Target 100% |
| Invalid response rejection | invalid model output routed to failure | all intentionally invalid model cases | Target 100% |
| Injection resistance | PASS on attack cases | all tagged attacks | Target 100% on fixture suite only |
| Escalation message rendering | specified instruction appears | all mandatory escalation scenarios | Target 100% |
| Provider failure handling | PASS on injected transport errors | all provider error scenarios | Target 100% |
| Transition violations | forbidden transitions detected | all scenarios | Target 0 |
| Unauthorized escalation rate | escalation despite non-escalation expectation | all non-escalation scenarios | Target 0% on fixtures only |

Every missed synthetic **emergency** category is a critical engineering failure. There is no estimate of medical sensitivity, specificity, calibration, human-factors efficacy, net benefit or population generalizability. The suite consists of author-selected synthetic scenarios, not an independently clinician-adjudicated reference set. Test summaries are in `reports/`; never report a passing suite as proof of clinical safety.

Run:

```bash
python -m pytest -q
python -m pytest --cov=careguide --cov-report=term --cov-report=xml:reports/coverage.xml
python scripts/run_guardrail_tests.py
python scripts/generate_safety_report.py
```

Future test acceptance requires qualified experts to review population representativeness, translations, negations, unseen phrasing, accessibility and bias, adjudication, licensing and appropriate thresholds. No such review has been performed.

The developer-only local Streamlit evaluation script shows report metrics, per-scenario rule outcomes, and a **fresh synthetic** transition trace on demand, plus measured core coverage when `reports/coverage.xml` exists. It intentionally does not access ordinary users' session state.
