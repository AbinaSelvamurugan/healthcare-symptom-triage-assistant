# Known limitations

1. **BLOCKER:** No independently sourced, licensed, reviewed and approved clinical protocol, qualified reviewer, or clinical population/jurisdiction is provided. All supplied rules are unvalidated fiction-only fixtures. No real triage can be performed.
2. **BLOCKER:** No authenticated Anthropic model/API access was available, so no live model call or provider compatibility test has been performed. The official SDK request shape and model-list method were cross-checked against provider documentation.
3. Live Streamlit UI rendering and Ruff linting have not been exercised; the test suite covers the pure view model only.
4. Phrase matching and simplistic negation have serious false-negative and false-positive risks. English-only; no validated coverage across demographics, languages, differentials or rare presentations. Prompt filtering is not a complete clinical safety filter.
5. This software does not persist symptom conversations or have a clinical audit/analytics infrastructure. In-memory session TTL is checked on interaction rather than asynchronously. Infrastructure and provider retention are not controlled by this code.
6. Session reset removes the emergency latch as a new session; no clinician-approved correction or identity/authentication workflow exists. This is suitable only for fictional testing.
7. No emergency number is included because the jurisdiction is unspecified. No timing promises or nonurgent classification from missing information are generated.
8. Fake-provider and fixture tests verify code behavior only. Synthetic pass rates do not establish real-world sensitivity, clinical safety, clinical validity, fairness, or regulatory compliance.
