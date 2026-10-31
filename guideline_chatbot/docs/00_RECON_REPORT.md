# Phase 0 — Reconnaissance Report

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Date of Acquisition:** 2026-10-31  
**Status:** Completed successfully — Gate 0 Ready

---

## 1. Executive Summary

A complete development environment was provisioned from scratch with Python 3.11.9, Git 2.52.0, and 15 pinned dependencies. A verified corpus of **10 official clinical guideline documents** (comprising **568 total pages**) was acquired from four authoritative health organizations: MoHFW (India), ICMR (India), WHO (International), and NICE (United Kingdom).

100% of the downloaded documents are valid PDFs with full text extractability verified via PyMuPDF. SHA-256 cryptographic hashes, page counts, and metadata were captured in both CSV and JSON formats in `data/inventory/`.

---

## 2. Acquired Documents Inventory

| Doc ID | Organization | Document Title | Condition | Pages | Size (bytes) | SHA-256 (prefix) | Text Extractable | Status |
|---|---|---|---|---|---|---|---|---|
| `who_htn_001` | WHO | Guideline for the Pharmacological Treatment of Hypertension in Adults (2021) | HTN | 61 | 843,539 | `57f6376d5c9b...` | Yes | current |
| `who_t2dm_001` | WHO | HEARTS-D: Diagnosis and Management of Type 2 Diabetes (2020) | T2DM | 35 | 1,248,098 | `71b216b19a22...` | Yes | current |
| `icmr_htn_001` | ICMR / DHR | STW - Hypertension in Adults (ICD-11 BA00) | HTN | 1 | 3,297,566 | `bffc8acfa65c...` | Yes | current |
| `icmr_t2dm_001` | ICMR / DHR | STW - Diabetes Mellitus Type 2 (ICD-11 5A11) | T2DM | 1 | 332,368 | `bcad0bfca7c2...` | Yes | current |
| `nice_htn_001` | NICE (UK) | NG136: Hypertension in Adults: Diagnosis and Management | HTN | 52 | 296,345 | `3f8255bf9c16...` | Yes | current |
| `nice_t2dm_001` | NICE (UK) | NG28: Type 2 Diabetes in Adults: Management | T2DM | 131 | 569,249 | `249e1f3ad3d1...` | Yes | current |
| `mohfw_htn_001` | MoHFW (India) | STG - Hypertension (Full Document) | HTN | 144 | 1,438,955 | `8388906c4f3c...` | Yes | current |
| `mohfw_htn_002` | MoHFW (India) | STG - Hypertension (Quick Reference Guide) | HTN | 54 | 1,748,005 | `62de7ccc3b98...` | Yes | current |
| `mohfw_htn_003` | MoHFW (India) | STG - Cardiovascular Diseases in India (Part 1) | HTN | 40 | 1,358,378 | `92ed8b17fbe6...` | Yes | current |
| `mohfw_t2dm_001` | MoHFW (India) | STG - Endocrinology (Diabetes Mellitus) | T2DM | 49 | 725,300 | `7f681425fa91...` | Yes | current |

**Totals:** 10 documents, 568 pages, 11,857,803 bytes (~11.3 MB).

---

## 3. Network Discovery and Acquisition Details

### 3.1 World Health Organization (WHO IRIS)
- **Challenge:** Direct handles such as `https://iris.who.int/handle/10665/344424` serve an Angular single-page application (DSpace 7 frontend). Older `/bitstream/handle/...` URLs return the 755-byte shell HTML page rather than the binary stream.
- **Resolution:** By tracing the official publication landing pages (`who.int/publications/i/item/...`), verified persistent bitstream content endpoints were discovered:
  - Hypertension: `https://iris.who.int/server/api/core/bitstreams/f062769d-f075-4a00-87af-0a2106e0bd04/content` (61 pages)
  - Type 2 Diabetes (HEARTS-D): `https://iris.who.int/server/api/core/bitstreams/2a0b4f68-7155-4ad1-b543-945791e31830/content` (35 pages)
- **Outcome:** Successfully acquired, 100% text-extractable.

### 3.2 Indian Council of Medical Research (ICMR)
- **Structure:** ICMR STWs are structured as high-density, multi-panel clinical decision workflows (flowcharts + clinical guidance tables).
- **Resolution:** Verified direct PDF links hosted on the ICMR official object store:
  - Hypertension: `https://www.icmr.gov.in/icmrobject/uploads/STWs/1778941063_hypertensioninadults_final.pdf` (1 large poster/workflow page)
  - Diabetes Mellitus Type 2: `https://www.icmr.gov.in/icmrobject/uploads/STWs/1726567245_diabetes_mellitus_type_2.pdf` (1 large poster/workflow page)
- **Outcome:** Successfully acquired, text and diagram text extractable.

### 3.3 National Institute for Health and Care Excellence (NICE)
- **Structure:** NICE generates guidelines dynamically; the guidance pages link to timestamped PDF resources.
- **Resolution:** Dynamically scraped the guidance resource endpoints for NG136 and NG28:
  - NG136 (Hypertension): `https://www.nice.org.uk/guidance/ng136` (52 pages)
  - NG28 (Type 2 Diabetes): `https://www.nice.org.uk/guidance/ng28` (131 pages)
- **Outcome:** Successfully acquired, highly structured text with explicit recommendation numbering (e.g. 1.4.1, 1.5.2).

### 3.4 Ministry of Health and Family Welfare, India (MoHFW)
- **Structure:** Hosted under the Clinical Establishments portal (`clinicalestablishments.mohfw.gov.in`).
- **Resolution:** Acquired both condition-specific modular STGs and multi-condition parent volumes:
  - Hypertension Full Document: `5191.pdf` (144 pages)
  - Hypertension Quick Reference Guide: `6591.pdf` (54 pages)
  - Cardiovascular Diseases Part 1: `3811.pdf` (40 pages)
  - Endocrinology (Diabetes Mellitus): `3601.pdf` (49 pages)
- **Outcome:** Successfully acquired, all digital text (no scanned images requiring OCR).

---

## 4. Text Extractability and OCR Assessment

All 10 documents were inspected using PyMuPDF:
- **Digital PDFs:** 10 / 10 documents contain native, selectable, searchable digital text.
- **Scanned Image PDFs:** 0 / 10 documents are pure scans.
- **OCR Decision:** Standard text extraction via PyMuPDF is sufficient. Optical Character Recognition (OCR / Tesseract) is **not required** for text extraction in Phase 1, though visual flowchart extraction will isolate flowchart boxes as structured decision nodes.

---

## 5. Preliminary Observations on Guideline Differences & Overlaps

During reconnaissance, key clinical variations across jurisdictions were noted:
1. **Hypertension Initiation Thresholds:**
   - *WHO 2021:* Initiate pharmacotherapy at SBP ≥ 140 or DBP ≥ 90 mmHg; consider initiation at 130–139 mmHg for patients with known CVD, high cardiovascular risk, diabetes, or CKD.
   - *NICE NG136:* Stage 1 hypertension (clinic 140/90 to 159/99, ABPM/HBPM 135/85 to 149/94) — treat under 80s if target organ damage, established CVD, renal disease, diabetes, or 10-year CVD risk ≥ 10%. Stage 2 (clinic ≥ 160/100) — treat all adults regardless of age.
   - *MoHFW / ICMR:* Staged stratification tailored to availability of basic primary healthcare drugs (Amlodipine, Enalapril/Telmisartan, Hydrochlorothiazide).
2. **First-Line Pharmacotherapy Variations:**
   - *NICE NG136:* Strong stratification by age and ethnicity: ACEi/ARB first-line for age < 55 (non-Black African/African-Caribbean); CCB first-line for age ≥ 55 or Black African/African-Caribbean ancestry.
   - *WHO 2021:* Any of 3 classes (thiazide/thiazide-like, ACEi/ARB, CCB) as monotherapy or combination; dual combination encouraged from outset.
3. **Type 2 Diabetes Targets:**
   - *NICE NG28:* Specific HbA1c targets: 48 mmol/mol (6.5%) with lifestyle/single non-hypoglycaemic drug; 53 mmol/mol (7.0%) if on drug associated with hypoglycaemia (sulfonylurea).
   - *WHO HEARTS-D / ICMR:* Fasting blood glucose thresholds and HbA1c < 7.0% as universal target with relaxed targets for elderly or frail patients.

These cross-source variations provide the exact clinical grounding needed to test **target-evidence binding** and **patient-context mismatch** in ClinCoherence.

---

## 6. Concrete Plan for Phase 1

1. **Extraction (`extract_pdf.py`):**
   - Extract page-by-page text preserving physical page numbering.
   - Restrict multi-condition volumes (`mohfw_stg_cardiovascular_diseases_part1.pdf`) to relevant clinical sections.
   - Identify tables and convert them to structured markdown tables.
   - Identify flowcharts (ICMR 1-page posters, MoHFW quick reference trees) and extract as decision nodes.
2. **Cleaning (`clean.py`):**
   - Strip running headers, footers, page number artifacts, and Ministry boilerplate without losing clinical text.
3. **Recommendation-Aware Chunking (`recommendation_chunker.py`):**
   - Segment by recommendation block rather than naive token windowing.
   - Preserve recommendation conditions, target populations, drug class tags, contraindications, and evidence grades in the chunk metadata.
