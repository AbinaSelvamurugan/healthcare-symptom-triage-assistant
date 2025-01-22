# CareGuide AI — Safety-First Healthcare Symptom Triage Assistant

CareGuide AI is an educational, non-clinical engineering prototype. It is not a medical service or medical device, it is not approved for real patient data, and it is not clinically validated. It does not diagnose, prescribe, or calculate medication doses, and a missing match never implies clinical safety. For a real medical concern, contact a qualified healthcare professional. For an emergency, contact your local emergency service rather than consulting this demo.

The bundled rules and the patient-like example inputs are demonstration and synthetic test fixtures, not clinical content.

## What it does

The app provides a Pydantic input gateway, a versioned demo-rule loader and deterministic priority engine, a session-scoped mandatory escalation latch, conservative handling of uncertainty and unsupported requests, an optional Anthropic Python SDK adapter, JSON proposal-schema and safety validation, a Streamlit interface with visible disclaimer and escalation banners, and a synthetic scenario suite that produces safety metrics. It performs no disease classification, prescribing, medication dosing, or clinical clearance.

## Intended use

Read [intended use](docs/intended_use.md), [architecture](docs/architecture.md), [rule governance](docs/escalation_protocol.md), [privacy](docs/privacy.md), and [limitations](docs/limitations.md) before using the program. Use only fictional data. Every shipped rule is flagged `DEMONSTRATION_ONLY`, with unknown jurisdiction and no emergency number, and the app has no approved-rule production mode.

## Repository layout and CI

The repository includes `.github/workflows/ci.yml`, which runs the offline synthetic tests on Python 3.11 and 3.13, along with `SECURITY.md`, `LICENSE`, `.gitignore`, the source code, test fixtures, and generated reports. Never commit `.env` or real health data.

## Environment and installation

Python 3.11+. The commands below target a POSIX shell from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
cp .env.example .env
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1` and copy with `Copy-Item .env.example .env`. Installing dependencies requires a working network or a configured local package mirror.

## Validating and running offline

```bash
python scripts/validate_rules.py
python -m pytest -q
python -m pytest --cov=careguide --cov-report=term --cov-report=xml:reports/coverage.xml
python scripts/run_guardrail_tests.py
python scripts/generate_safety_report.py
python -m ruff check .
streamlit run app/streamlit_app.py --server.address 127.0.0.1
```

The offline tests run without an API key. The default config `CAREGUIDE_MODE=offline_demo` does not contact Anthropic. The test CLI writes `reports/safety_report.json`, `reports/safety_report.md`, `reports/scenario_results.csv`, and `reports/safety_metrics.csv`.

## Optional Claude language-generation demo

Only use fictional examples. Set `ANTHROPIC_API_KEY` and `CAREGUIDE_MODE=claude_demo`, and pick a model identifier that is available to your account (do not assume a model ID is available to your account). Export these variables in your shell or load `.env` through a secure mechanism; CLI modules do not implicitly read `.env`. For a local shell:

```bash
set -a
source .env
set +a
python scripts/verify_claude.py
CAREGUIDE_RUN_LIVE_API=1 python -m pytest -m live_api -q
streamlit run app/streamlit_app.py --server.address 127.0.0.1
```

`verify_claude.py` calls the official Models retrieval API with the authenticated account. In Claude demo mode the provider is used only for synthetic `GENERAL_INFO` cases: escalation is computed before any model call, and Claude cannot change its category or instruction. Malformed output, network or API failure, or unsupported text returns a predetermined provider-failure message. Live tests require a separate opt-in flag; see `docs/deployment.md`.

Official documentation: [Python SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python) and [Models API](https://platform.claude.com/docs/en/api/models/list). The SDK Messages API uses `client.messages.create(model=..., max_tokens=..., system=..., messages=...)` and supports configurable `timeout` and `max_retries`.

## Developer-only evaluation

A separate entry point runs locally; it is not linked from the public UI and has no authentication. Never expose it over a public network:

```bash
CAREGUIDE_ENABLE_DEV_DASHBOARD=true streamlit run app/pages/evaluation.py --server.address 127.0.0.1
```

It displays the synthetic report and metadata; only the current in-memory `Session` keeps individual transition traces. The public app never exposes internal prompts or trace tables.

## Data protection

Raw fictional conversation text is held only in Streamlit session memory; no database writes, web telemetry, or persistent symptom logs are enabled by default. `Reset` clears conversation history. Session TTL defaults to 30 minutes, and an expired session is discarded on the next interaction. In Anthropic mode, the latest scenario and a configured instruction cross the external API boundary. Review the provider's terms and platform behavior before sending any data. This prototype makes no regulated-data compliance claims.

## Rule governance and clinical scope

A rule's approval requires independently documented provenance, population and jurisdiction, reviewer, licensing, validation, and appropriate authorizations. The repository cannot be switched to clinical mode by setting an environment variable. See [testing methodology](docs/testing_methodology.md).

## License

Released under the MIT License; see [LICENSE](LICENSE). Third-party components, including the Anthropic Python SDK, remain under their own licenses.
