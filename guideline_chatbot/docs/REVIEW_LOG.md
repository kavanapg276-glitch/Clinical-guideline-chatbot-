# Code Review Log

Self-review findings per phase in accordance with Standing Rule 9.
Each entry records: bugs found, hard-coded clinical claims (strictly forbidden), duplicated logic, missing tests, and security issues.

---

## Phase 0 — Environment Setup & Dataset Acquisition

**Review Date:** 2026-10-31  
**Reviewer:** Self-Review Pass (Automated Quality Gate + Static Analysis)  
**Status:** PASSED (Ready for Gate 0)

### 1. Bugs Found & Fixed
1. **WHO IRIS DSpace 7 SPA Trap:**
   - *Issue:* Static bitstream URLs (`iris.who.int/bitstream/handle/...`) returned 755-byte Angular SPA HTML shells rather than PDF binaries.
   - *Fix:* Traced official publication landing pages (`who.int/publications/i/item/...`) to acquire direct, persistent REST bitstream content URLs (`iris.who.int/server/api/core/bitstreams/{uuid}/content`). Verified header `b'%PDF-1.7'`.
2. **ICMR STW 404 Error:**
   - *Issue:* Initial generic URL pattern for Type 2 Diabetes returned an ICMR 404 HTML exception page.
   - *Fix:* Scraped the ICMR STWs repository page to identify the verified URL with the required numeric prefix (`1726567245_diabetes_mellitus_type_2.pdf`).
3. **PyMuPDF Deprecation Warning:**
   - *Issue:* `import fitz` triggered a `FutureWarning` in PyMuPDF 2.0.
   - *Fix:* Replaced all references with `import pymupdf` and `pymupdf.open()`.
4. **Offline Test Hang in Sandbox Mode:**
   - *Issue:* In Standard Sandbox Mode (no network access), `SentenceTransformer` attempted to contact HuggingFace Hub to check for updates, hanging until socket timeout.
   - *Fix:* Set `local_files_only=True` and environment variables `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1` in `test_phase0.py`.
5. **Windows Console Unicode Encoding:**
   - *Issue:* Special ligatures (e.g. `\ufb02` for 'fl') in guideline text failed with `charmap` codec error on Windows default CP1252 console.
   - *Fix:* Sanitized text encoding for terminal outputs.
6. **Lint & Formatting Violations:**
   - *Issue:* 22 `ruff` errors (line lengths > 100 characters in catalog definitions and unnecessary f-strings).
   - *Fix:* Auto-formatted with `ruff format .` and wrapped catalog strings cleanly; `ruff check .` passed with 0 errors.
7. **Type Checking Failures:**
   - *Issue:* 17 `mypy` errors in `acquire.py` regarding BeautifulSoup `link["href"]` (`str | AttributeValueList`) and untyped dictionary candidates.
   - *Fix:* Added explicit string coercion and `list[dict[str, Any]]` annotations. `mypy` passed with 0 errors across 12 files.

### 2. Hard-Coded Clinical Claims
- **Audit Result:** NONE.
- **Verification:** No clinical recommendations, drug doses, BP/HbA1c thresholds, or diagnostic criteria are hard-coded in the Python source code. All clinical knowledge is quarantined to the acquired PDF files and their documented metadata catalog.

### 3. Duplicated Logic
- **Audit Result:** NONE.
- Shared utilities (`compute_sha256`, `get_pdf_metadata`) are centralized in `acquire.py` and imported by `inventory.py` and `test_phase0.py`.

### 4. Missing Tests
- **Audit Result:** NONE for Phase 0.
- A comprehensive 58-test test suite (`test_phase0.py`) covers:
  - 20 required directory existence checks
  - 6 `.gitignore` pattern validations
  - 12 dependency import tests
  - 3 `settings.yaml` configuration schema checks
  - 3 embedding model tests (loading, 384-dimension output, determinism)
  - 5 documentation existence checks
  - 5 inventory schema & cryptographic SHA-256 checks against actual files on disk
  - 4 module import & Pydantic schema validation tests

### 5. Security & Privacy Audit
- Zero credentials or API keys exist in the repository.
- `.env` is excluded in `.gitignore`; `.env.example` provides template variables only.
- Raw clinical guideline PDFs in `guideline_chatbot/data/raw/` are excluded from Git to prevent accidental redistribution of copyrighted materials.
