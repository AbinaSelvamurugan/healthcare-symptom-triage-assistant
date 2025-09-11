# Intended use, scope and clinical boundary

**Project:** CareGuide AI — Safety-First Healthcare Symptom Triage Assistant.
**Status:** educational SOFTWARE DEMONSTRATION, NOT A MEDICAL SERVICE. **No approved clinical protocol is supplied.**

Audience: developers, quality engineers and clinical reviewers testing architecture using **fictional, synthetic scenarios only**. This prototype is not intended for real patients, clinical practice, or medical decision-making. Operate locally in a development environment with demo fixtures; no medical device clearance, clinical evaluation or regulatory assessment is claimed.

Supported: short fictional symptom narratives, configured follow-up prompts, demonstration escalation markers, scope refusal, uncertainty referrals, fake-provider validation, optional constrained Claude text output. No autonomous diagnosis, medication guidance, dosing, definitive rulings-out, clinical clearance, or personalized care planning.

All rules shipped in `configs/clinical_rules.example.yaml` are **UNVALIDATED DEMONSTRATION RULES**, not authoritative clinical thresholds. No country, local emergency number, review date or sign-off has been invented. Default jurisdiction is **unspecified**. The application always discloses that real reports should go to a qualified local healthcare professional. For a real emergency, users must contact their local emergency service; do not rely on this demonstration to assess urgency.

Boundaries: deterministic rules are evaluated before optional model generation; no result is interpreted as proof of safety. The sample phrase matching has inherent false-negative and false-positive risk. Missing data are never treated as a negative result. Unknown situations yield an uncertainty/referral state, not a non-urgent classification. Real deployment requires a licensed, jurisdiction-specific protocol with clinical sign-off; governance, performance evaluation, security, privacy, accessibility and legal reviews; red-teaming; post-market monitoring; and authorization appropriate to intended use.

External transmission: In `offline_demo` (default), no narrative is sent to any provider. In `claude_demo`, the latest fictional narrative and configured context are sent to Anthropic under the operator's provider account; enabling that mode is an explicit developer choice. No conversation text is persisted by default. See `docs/privacy.md`.
