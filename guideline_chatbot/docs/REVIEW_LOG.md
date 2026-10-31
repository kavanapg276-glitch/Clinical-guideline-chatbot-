# Code Review Log

Self-review findings per phase in accordance with Standing Rule 9.
Each entry records: bugs found, hard-coded clinical claims (strictly forbidden), duplicated logic, missing tests, and security issues.

---

## Phase 0 — Environment Setup & Dataset Acquisition

**Review Date:** 2026-10-31  
**Reviewer:** Self-Review Pass (Automated Quality Gate + Static Analysis + User Review Items)  
**Status:** PASSED (Ready for Gate 0)

### 1. Pre-Gate 0 User Review Items Addressed
1. **MoHFW Background Document Tagging:**
   - Tagged `mohfw_htn_001` (5191.pdf, 144 pages) explicitly as `"MoHFW STG - Hypertension (Background Document)"` in both CSV and JSON inventories.
   - Page 1 explicitly verified: *"Background Document: Hypertension Screening, Diagnosis, Assessment, and Management of Primary Hypertension in Adults in India (March 2016)"*.
2. **Real PDF & Title Page Verification:**
   - All 10 documents verified byte-for-byte to start with `%PDF-` magic header (no HTML error pages, no truncated bodies).
   - Extracted title page text for all 10 PDFs via PyMuPDF; confirmed 100% match with intended guidelines.
   - All source URLs verified as direct, live official endpoints (no partial/recalled URLs).
3. **Official Quoted Licence Terms:**
   - Replaced placeholder licence strings with verbatim quotes from official policy pages:
     - WHO: CC BY-NC-SA 3.0 IGO notice quoted with URL `https://www.who.int/about/policies/publishing/copyright`
     - ICMR: Official STW notice quoted with URL `https://www.icmr.gov.in/standard-treatment-workflows-stws`
     - NICE: Clause 18 Notice of Rights quoted with URL `https://www.nice.org.uk/terms-and-conditions#notice-of-rights`
     - MoHFW: Portal Copyright Policy quoted with URL `https://clinicalestablishments.mohfw.gov.in/en/copyright-policy`
4. **Current vs. Superseded Version Tracking:**
   - Every inventory record confirmed as `document_status: current` with publication date, version string, and verification notes.
5. **Strict Scope Control:**
   - ICMR: Restricted strictly to adult Type 2 Diabetes (`1726567245_diabetes_mellitus_type_2.pdf`) and adult Hypertension (`1778941063_hypertensioninadults_final.pdf`). Type 1 and DKA workflows excluded.
   - WHO: Restricted strictly to the two primary picks: Pharmacological Treatment of Hypertension (2021) and HEARTS-D Type 2 Diabetes (2020).

### 2. Bugs Found & Fixed
- Resolved DSpace 7 SPA HTML trapping on WHO IRIS bitstreams.
- Resolved ICMR diabetes STW 404 URL pattern by discovering the exact numeric object path.
- Replaced PyMuPDF deprecated `fitz` API with modern `import pymupdf`.
- Configured offline environment variables (`HF_HUB_OFFLINE=1`) for sandbox-safe embedding tests.
- Sanitized Windows console CP1252 output encoding.
- Resolved 22 `ruff` formatting/lint errors and 17 `mypy` typing errors.

### 3. Hard-Coded Clinical Claims
- **Audit Result:** NONE.
- All clinical knowledge is preserved exclusively in source PDFs and documented metadata.

### 4. Duplicated Logic
- **Audit Result:** NONE.
- Shared hashing and metadata extraction centralized in `acquire.py`.

### 5. Test Suite & Static Analysis
- **Ruff Check:** Passed (0 errors).
- **Ruff Format Check:** Passed (19 files formatted).
- **Mypy Check:** Passed (0 errors across 12 files).
- **Pytest:** 58 passed in 25.03s.

### 6. Security & Privacy Audit
- Zero credentials or API keys committed.
- `.env` and `guideline_chatbot/data/raw/` strictly ignored in Git.
