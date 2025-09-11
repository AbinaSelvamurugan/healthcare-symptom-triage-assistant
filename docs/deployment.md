# Local demo deployment and troubleshooting

This build is for isolated software demonstration only. It is **not authorized** for clinical deployment or real patients.

Recommended Python: 3.11+ with a dependency resolver and network access. See README for venv and installation commands. Start with `python scripts/validate_rules.py`; any config failure must be corrected before the UI opens. Launch `streamlit run app/streamlit_app.py --server.address 127.0.0.1`. Keep the browser/server bound to loopback; do not publicly expose health-related prototypes without appropriate controls.

**Offline mode:** Configured in `configs/application.yaml` or process variable `CAREGUIDE_MODE=offline_demo`, with no key required. `python -m pytest` and the standalone report generator require no Anthropic SDK network traffic.

**Optional provider mode:** Set `CAREGUIDE_MODE=claude_demo`, `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL` via the environment; check access to the configured model with `python scripts/verify_claude.py`. Do not paste the key in the UI. Official Anthropic SDK handles bounded retry (configured <=2), timeout (default 12 s), and rate limiting/error exceptions through a sanitized fallback. Live network integration with the provider has not been exercised.

**Evaluation UI:** Developer-only script `app/pages/evaluation.py` requires `CAREGUIDE_ENABLE_DEV_DASHBOARD=true` and must be bound to `127.0.0.1`. It has no built-in authentication; do not host it for end users.

**Troubleshooting:** `ModuleNotFoundError` indicates an incomplete installation or missing editable package; activate `.venv` and install again with connectivity. A missing model returns a provider-failure or configuration warning, never a fabricated diagnosis. Expired sessions require starting a new fiction-only session. Invalid YAML fails application loading. Invalid Claude response fails with the configured failure message. Core `pytest` runs where `pydantic`, `PyYAML`, `pandas` and `pytest` are installed; the Streamlit UI and SDK calls additionally require those packages.

Before any real deployment, establish licensed clinician-reviewed rules, approved service routing, real-world test governance, authenticated access, threat modeling, an incident response plan, privacy/security assessment, cross-language and adversarial evaluation, emergency contact maintenance, clinical human oversight, model version control, and regulatory review.
