# Security and responsible reporting

**CareGuide AI is an unvalidated educational prototype and must not be used for real patients, protected health information, clinical decision-making, or public medical advice.** The examples and rule triggers are synthetic, demonstration-only fixtures.

## Reporting a software vulnerability

If you discover a security weakness, do **not** include any real patient data, secrets, access tokens, or private prompts in the report. Prefer a private GitHub security advisory to a public issue when the repository owner has enabled private vulnerability reporting. Otherwise contact the repository maintainer through a private channel configured by that owner. A disclosure-response SLA or monitored mailbox has **not** been established by this sample project.

## Secrets and private data

- Never commit `.env`, Anthropic API keys, medical narratives, or identifiable information.
- `.gitignore` excludes `.env`, local virtual environments, Python caches, coverage databases, and local SQLite databases. Check `git status` before every push.
- The CI workflow uses synthetic fixtures only, needs no Anthropic key, and must not be repurposed to send real medical information to an LLM.
- The optional developer evaluation page has **no authentication** and must remain local-only.
- Provider mode transmits supplied text to Anthropic; use *fictional test cases only* and consult `docs/privacy.md`.

## Safety governance

Software bug fixes, tests, and prompt changes do not make clinical rules valid. Clinical safety approval, clinical data processing, and public deployment are outside the reviewed scope. See `docs/escalation_protocol.md` and `docs/limitations.md`.
