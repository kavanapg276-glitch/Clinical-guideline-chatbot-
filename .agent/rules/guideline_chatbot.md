# Standing Rules — ClinCoherence Guideline Chatbot

These rules are **non-negotiable** and apply to all phases of development.

1. **Never invent** guideline text, recommendations, page numbers, URLs, dates, versions or citations. Every KB fact must trace to a real page of a real, preserved source file. Unknown fields are stored as `null` and flagged.
2. **Use only official sources** (MoHFW STG, ICMR STW, WHO, NICE). Download only what is needed for hypertension and type 2 diabetes. No bulk downloading.
3. **Preserve original files untouched** with SHA-256 hashes. Process copies.
4. **Check and record licensing/reuse terms** per source in `docs/LICENSING.md`. Add `data/raw/` to `.gitignore` unless a licence clearly allows redistribution.
5. **Never commit** API keys, credentials, `.env`, or patient-identifiable data. Provide `.env.example` only. Never hard-code a model provider or key.
6. **Modular, typed, tested:** Python 3.10+, type hints, docstrings, `pydantic` schemas, YAML config, `logging` (no stray prints), fixed random seeds, `pytest` tests per module.
7. **Git:** `git init`, create branch `feature/guideline-chatbot`, commit small and often with conventional messages (`feat:`, `fix:`, `docs:`, `test:`). Add a `.gitignore` first.
8. **Antigravity workflow:** use Planning mode. For each phase: (a) produce an Implementation Plan artifact, (b) wait for approval, (c) execute, (d) produce a Walkthrough artifact with **real** command output, (e) stop at the gate. Do not start the next phase until approved.
9. **Code quality gate:** at the end of every phase run `ruff check .`, `ruff format --check .`, `mypy` (best effort) and `pytest -q`; paste the real output; fix failures before asking for approval. Then do a **self-review pass** of the phase's diff and list: bugs found, hard-coded clinical claims (forbidden), duplicated logic, missing tests, security issues. Record in `docs/REVIEW_LOG.md`.
10. **Network failures:** if a download is blocked, times out, needs login/captcha, or a link is not found, **do not guess URLs or fabricate files**. Log it in `docs/OPEN_QUESTIONS.md`, list the exact document and the official page where it can be downloaded manually into `data/raw/<source>/`, and wait. Continue only with documents actually obtained.
11. When requirements are ambiguous, choose the safest documented default and log it; do not silently guess.
12. Clinical-safety posture: answers are grounded only in retrieved guideline text, always cited, state missing patient information, and abstain when evidence is inadequate. No doses, diagnoses or recommendations that are not in retrieved text.

