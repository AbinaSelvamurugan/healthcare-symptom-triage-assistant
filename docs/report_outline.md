# Project report outline

1. **Abstract:** A safety-first non-clinical symptom-interaction architecture, explicit unvalidated status.
2. **Problem statement:** Hazards of unconstrained medical chatbots; need for auditable escalation, privacy and bounded language output.
3. **Objectives and intended use:** Supported fictional flows, excluded clinical judgments, safety-governance boundary.
4. **Related work:** Clinical decision-support systems, conversational agents, hazard analysis, LLM prompt injection, software testing. Cite independent sources.
5. **Requirements and risk model:** Functional/nonfunctional requirements; accidental false reassurance; stale protocol; uncertain wording; data privacy.
6. **Architecture/system boundaries:** Layered data flow, threat model, rule independence, diagrams in `architecture.md`.
7. **Rule engine design:** Pydantic schemas, provenance model, priority logic, sticky escalation, uncertainty handling, limitations of keyword fixtures.
8. **Claude integration:** SDK, configurable model availability, timeout/retry, strict proposal validation, provider error recovery.
9. **Streamlit UI and session lifecycle:** Disclosure, history, clear escalation, metadata-only developer dashboard, TTL and reset.
10. **Guardrail testing:** Fixture versioning, unit/integration/scenario suite, injections, failure injection, model stubs.
11. **Results:** pytest run counts, case CSV and numerator/denominator metrics; classify clinical acceptance as **not clinically validated**.
12. **Privacy/security/ethics:** Data minimization, external API boundary, logs, incomplete security and compliance review.
13. **Limitations and threats to validity:** Synthetic distribution bias, no clinical protocol, no prospective clinical evaluation, limited natural-language detection.
14. **Future work:** Qualified clinical advisory board, licensed protocols, jurisdiction rules, language validation, audited clinical test sets, security/accessibility review, post-deployment human oversight.
15. **Conclusion:** Software verification supports a prototype architecture only; no implication of clinical approval or readiness.
16. **Appendices:** Test cases, project structure, API contract, requirements traceability, coverage and report artifacts.
