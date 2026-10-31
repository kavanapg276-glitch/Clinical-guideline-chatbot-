# Phase 0 — Reconnaissance Report

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Date of Acquisition:** 2026-10-31  
**Status:** Completed successfully — Gate 0 Ready

---

## 1. Executive Summary

A complete development environment was provisioned from scratch with Python 3.11.9, Git 2.52.0, and 15 pinned dependencies. A verified corpus of **10 official clinical guideline documents** (comprising **568 total pages**) was acquired from four authoritative health organizations: MoHFW (India), ICMR (India), WHO (International), and NICE (United Kingdom).

100% of the downloaded documents are valid PDFs (starts with `%PDF-` magic header) with full text extractability verified via PyMuPDF. All title pages match intended documents. SHA-256 cryptographic hashes, page counts, verified versions, and official quoted licence terms were captured in both CSV and JSON formats in `data/inventory/`.

---

## 2. Acquired Documents Inventory & Title Page Verification

| Doc ID | Organization | Document Title | Condition | Pages | Size (bytes) | SHA-256 (prefix) | Version Status | Title Page Verification |
|---|---|---|---|---|---|---|---|---|
| `who_htn_001` | WHO | Guideline for the Pharmacological Treatment of Hypertension in Adults (2021) | HTN | 61 | 843,539 | `57f6376d5c9b...` | **Current** (2021 active) | "Guideline for the pharmacological treatment of hypertension in adults // World Health Organization" |
| `who_t2dm_001` | WHO | HEARTS-D: Diagnosis and Management of Type 2 Diabetes (2020) | T2DM | 35 | 1,248,098 | `71b216b19a22...` | **Current** (2020 active) | "Diagnosis and Management of Type 2 Diabetes // WHO/UCN/NCD/20.1" |
| `icmr_htn_001` | ICMR / DHR | STW - Hypertension in Adults (ICD-11 BA00) | HTN | 1 | 3,297,566 | `bffc8acfa65c...` | **Current** (May 2022 active) | "Standard Treatment Workflow (STW) // HYPERTENSION IN ADULTS // ICD-11 BA00" |
| `icmr_t2dm_001` | ICMR / DHR | STW - Diabetes Mellitus Type 2 (ICD-11 5A11) | T2DM | 1 | 332,368 | `bcad0bfca7c2...` | **Current** (2022 active) | "Standard Treatment Workflow (STW) // DIABETES MELLITUS TYPE 2 // ICD-10-E11" |
| `nice_htn_001` | NICE (UK) | NG136: Hypertension in Adults: Diagnosis and Management | HTN | 52 | 296,345 | `3f8255bf9c16...` | **Current** (Updated Feb 2026) | "Hypertension in adults: diagnosis and management // NICE guideline NG136" |
| `nice_t2dm_001` | NICE (UK) | NG28: Type 2 Diabetes in Adults: Management | T2DM | 131 | 569,249 | `249e1f3ad3d1...` | **Current** (Updated Feb 2026) | "Type 2 diabetes in adults: management // NICE guideline NG28" |
| `mohfw_htn_001` | MoHFW (India) | STG - Hypertension (Background Document) | HTN | 144 | 1,438,955 | `8388906c4f3c...` | **Current** (Background, March 2016) | "Background Document // Hypertension // Screening, Diagnosis, Assessment, and Management of Primary Hypertension in Adults in India // March 2016" |
| `mohfw_htn_002` | MoHFW (India) | STG - Hypertension (Quick Reference Guide) | HTN | 54 | 1,748,005 | `62de7ccc3b98...` | **Current** (QRG, May 2016) | "Standard Treatment Guidelines - Hypertension // Quick Reference Guide // May 2016" |
| `mohfw_htn_003` | MoHFW (India) | STG - Cardiovascular Diseases in India (Part 1) | HTN | 40 | 1,358,378 | `92ed8b17fbe6...` | **Current** (Part 1, 2016) | "GUIDELINES FOR THE MANAGEMENT OF CARDIOVASCULAR DISEASES IN INDIA // Part 1" |
| `mohfw_t2dm_001` | MoHFW (India) | STG - Endocrinology (Diabetes Mellitus) | T2DM | 49 | 725,300 | `7f681425fa91...` | **Current** (2016) | "STANDARD TREATMENT GUIDELINES // ENDOCRINOLOGY // Ministry of Health & Family Welfare" |

**Totals:** 10 documents, 568 pages, 11,857,803 bytes (~11.3 MB). 100% verified authentic.

---

## 3. Scope Boundaries & Specific Inclusions

1. **ICMR Scope (Type 2 Diabetes Only):**
   - Strictly restricted to `icmr_t2dm_diabetes_type2.pdf` (ICD-10-E11) and `icmr_htn_hypertension_in_adults.pdf` (ICD-11 BA00).
   - Type 1 Diabetes (`1726567249_diabetes_mellitus_type_1.pdf`) and Diabetic Ketoacidosis (`1726567244_diabetic_ketoacidosis.pdf`) were identified during scanning but excluded from the corpus per user instruction.

2. **WHO Scope (Two Primary Picks Only):**
   - Restricted strictly to:
     - `who_htn_pharmacological_treatment_2021.pdf` (Guideline for the Pharmacological Treatment of Hypertension in Adults, 2021)
     - `who_t2dm_hearts_d_2020.pdf` (HEARTS-D: Diagnosis and Management of Type 2 Diabetes, 2020)
   - Other WHO PEN general manuals and ancillary implementation guides omitted to prevent out-of-scope dilution.

3. **MoHFW Scope & Background Document Tagging:**
   - `mohfw_htn_001` (5191.pdf, 144 pages) is officially titled *"Background Document: Hypertension — Screening, Diagnosis, Assessment, and Management of Primary Hypertension in Adults in India (March 2016)"*.
   - Tagged explicitly as `background` in the inventory name and notes to distinguish foundational evidence reviews from operational treatment algorithms.
   - `mohfw_htn_002` (6591.pdf, 54 pages) provides the corresponding operational Quick Reference Guide.
   - Multi-condition volumes (`mohfw_stg_cardiovascular_diseases_part1.pdf` and `mohfw_stg_endocrinology_diabetes.pdf`) have page ranges bounded in the inventory.

---

## 4. Licensing & Official Source Terms

All documents were checked against official terms of use and copyright notices:

- **WHO:** CC BY-NC-SA 3.0 IGO. Quoted from page 4 of each document and [who.int copyright policy](https://www.who.int/about/policies/publishing/copyright).
- **ICMR / DHR:** Official Government Publication for Healthcare System Education. Quoted from document title panels and [icmr.gov.in terms](https://www.icmr.gov.in/standard-treatment-workflows-stws).
- **NICE (UK):** UK Notice of Rights / Crown Copyright. Personal and academic research permitted under Clause 18 of [nice.org.uk terms and conditions](https://www.nice.org.uk/terms-and-conditions#notice-of-rights).
- **MoHFW (India):** Government of India Official STGs under the Clinical Establishments Act. Permitted for accurate, non-derogatory reproduction with attribution per [clinicalestablishments.mohfw.gov.in copyright policy](https://clinicalestablishments.mohfw.gov.in/en/copyright-policy).

Detailed quotes are documented in `docs/LICENSING.md`.

---

## 5. Phase 1 Roadmap

1. **Extraction (`extract_pdf.py`):**
   - Extract page text preserving original page numbering.
   - Separate tables into structured markdown.
   - Extract flowchart trees (ICMR 1-page posters, MoHFW flowcharts) into structured decision nodes.
2. **Cleaning (`clean.py`):**
   - Strip running headers, footers, and Ministry boilerplate without losing clinical text.
3. **Recommendation-Aware Chunking (`recommendation_chunker.py`):**
   - Segment by clinical recommendation block.
   - Preserve conditions, target population, contraindications, and evidence grades in chunk metadata.
