# Code Review Log

Self-review findings per phase in accordance with Standing Rule 9.
Each entry records: bugs found, hard-coded clinical claims (strictly forbidden), duplicated logic, missing tests, and security issues.

---

## Phase 0 — Environment Setup & Dataset Acquisition

**Review Date:** 2026-10-31  
**Reviewer:** Self-Review Pass (Automated Quality Gate + Static Analysis + User Review Items)  
**Status:** PASSED (Ready for Gate 0)

### 1. Pre-Gate 0 Final Fixes Addressed (8 Items)
1. **ICMR Publication Dates:**
   - Set to exact printed dates: `icmr_htn_001` set to `"May/2026"` (printed review horizon on sheet); `icmr_t2dm_001` set to `"July/ 2022"`.
   - `mohfw_t2dm_001` (Endocrinology) set to `null` because no publication date is printed in the document.
2. **Version String Cleanup:**
   - All version values not explicitly printed in documents set to `null` (including all placeholder `"1.0"` values).
3. **MoHFW CVD Part 1 Removal:**
   - Table of Contents of `mohfw_stg_cardiovascular_diseases_part1.pdf` audited: CHD (p.5–11), Rheumatic Fever (p.12), ACS/NSTEMI (p.13–31), STEMI (p.32–40). Primary hypertension treatment is not covered (0 pages).
   - Removed completely from disk, acquire pipeline, catalog, and inventory.
4. **Relevant Page Range Bounding:**
   - `mohfw_stg_endocrinology_diabetes.pdf` audited: Diabetes Mellitus is strictly pages `6–21` (Topic 2: Hirsutism starts on p.22). Inventory set to `relevant_page_ranges: "6-21"`.
5. **ICMR Diabetes ICD Code Correction:**
   - Corrected to `ICD-10-E11` matching the printed text on the PDF sheet (replacing placeholder `ICD-11 5A11`).
6. **MoHFW Reuse Label:**
   - Changed reuse label from `"Open Government STG"` to `"Permission required before reproduction; source acknowledgement required"` reflecting official MoHFW copyright policy.
7. **Canonical Identical NICE Quote:**
   - Clause 18 Notice of Rights from NICE Terms and Conditions quoted identically across inventory, licensing doc, and recon report.
8. **Per-Page Extractability & Flowchart Audit:**
   - Evaluated 528 pages across 9 PDFs: 524 pages contain native extractable text.
   - Identified 6 blank/cover pages (<50 chars) and 4 flowchart pages with raster/vector drawings (`mohfw_stg_hypertension_full.pdf` p.127; `mohfw_stg_hypertension_quickref.pdf` p.40, 44, 52).
   - Verified ICMR STW 1-page posters are 100% digital extractable text (no OCR required).

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
- **Pytest:** 58 passed in 55.84s.

### 6. Security & Privacy Audit
- Zero credentials or API keys committed.
- `.env` and `guideline_chatbot/data/raw/` strictly ignored in Git.
