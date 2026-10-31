# Phase 0 — Reconnaissance Report

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Date of Acquisition:** 2026-10-31  
**Status:** Completed successfully — Gate 0 Ready

---

## 1. Executive Summary

A complete development environment was provisioned from scratch with Python 3.11.9, Git 2.52.0, and 15 pinned dependencies. A verified corpus of **9 official clinical guideline documents** (comprising **528 total pages**, 10,499,425 bytes) was acquired from four authoritative health organizations: MoHFW (India), ICMR (India), WHO (International), and NICE (United Kingdom).

100% of the downloaded documents are valid PDFs (confirmed to start with the `%PDF-` magic header) with full text extractability verified via PyMuPDF. All title pages match intended documents. Cryptographic SHA-256 hashes, page counts, verified dates, versions, and quoted licence terms were captured in both CSV and JSON formats in `data/inventory/`.

---

## 2. Acquired Documents Inventory & Title Page Verification

| Doc ID | Organization | Document Title | Condition | Pages | Size (bytes) | SHA-256 (prefix) | Publication Date | Version | Title Page Verification |
|---|---|---|---|---|---|---|---|---|---|
| `who_htn_001` | WHO | Guideline for the Pharmacological Treatment of Hypertension in Adults (2021) | HTN | 61 | 843,539 | `57f6376d5c9b...` | 2021 | null | "Guideline for the pharmacological treatment of hypertension in adults // World Health Organization" |
| `who_t2dm_001` | WHO | HEARTS-D: Diagnosis and Management of Type 2 Diabetes (2020) | T2DM | 35 | 1,248,098 | `71b216b19a22...` | 2020 | null | "Diagnosis and Management of Type 2 Diabetes // WHO/UCN/NCD/20.1" |
| `icmr_htn_001` | ICMR / DHR | STW - Hypertension in Adults (ICD-11 BA00) | HTN | 1 | 3,297,566 | `bffc8acfa65c...` | May/2026 | null | "Standard Treatment Workflow (STW) // HYPERTENSION IN ADULTS // ICD-11 BA00" |
| `icmr_t2dm_001` | ICMR / DHR | STW - Diabetes Mellitus Type 2 (ICD-10-E11) | T2DM | 1 | 332,368 | `bcad0bfca7c2...` | July/ 2022 | null | "Standard Treatment Workflow (STW) // DIABETES MELLITUS TYPE 2 // ICD-10-E11" |
| `nice_htn_001` | NICE (UK) | NG136: Hypertension in Adults: Diagnosis and Management | HTN | 52 | 296,345 | `3f8255bf9c16...` | 2019-08-28 | null | "Hypertension in adults: diagnosis and management // NICE guideline NG136" |
| `nice_t2dm_001` | NICE (UK) | NG28: Type 2 Diabetes in Adults: Management | T2DM | 131 | 569,249 | `249e1f3ad3d1...` | 2015-12-02 | null | "Type 2 diabetes in adults: management // NICE guideline NG28" |
| `mohfw_htn_001` | MoHFW (India) | STG - Hypertension (Background Document) | HTN | 144 | 1,438,955 | `8388906c4f3c...` | March 2016 | null | "Background Document // Hypertension // Screening, Diagnosis, Assessment, and Management of Primary Hypertension in Adults in India // March 2016" |
| `mohfw_htn_002` | MoHFW (India) | STG - Hypertension (Quick Reference Guide) | HTN | 54 | 1,748,005 | `62de7ccc3b98...` | May 2016 | null | "Standard Treatment Guidelines - Hypertension // Quick Reference Guide // May 2016" |
| `mohfw_t2dm_001` | MoHFW (India) | STG - Endocrinology (Diabetes Mellitus) | T2DM | 49 | 725,300 | `7f681425fa91...` | null | null | "STANDARD TREATMENT GUIDELINES // ENDOCRINOLOGY // Ministry of Health & Family Welfare" |

**Totals:** 9 documents, 528 total pages, 10,499,425 bytes (~10.5 MB). 100% verified authentic.

---

## 3. Scope Boundaries & Investigative Audit Findings

### 3.1 ICMR STW Documents Audit
1. **Publication Dates:**
   - `icmr_htn_001` explicitly prints `May/2026` on page 1 (advisory review horizon printed by ICMR). Recorded verbatim as `"May/2026"` without inference.
   - `icmr_t2dm_001` explicitly prints `July/ 2022` on page 1. Recorded verbatim as `"July/ 2022"`.
2. **ICD Code Correction:**
   - The T2DM STW sheet explicitly prints `ICD-10-E11` beneath the title "DIABETES MELLITUS TYPE 2". The document title and catalog were corrected from the initial placeholder `ICD-11 5A11` to `ICD-10-E11`.
3. **Scope Restriction:**
   - Strictly restricted to adult primary Type 2 Diabetes (`1726567245_diabetes_mellitus_type_2.pdf`) and adult primary Hypertension (`1778941063_hypertensioninadults_final.pdf`). Type 1 Diabetes (`1726567249_diabetes_mellitus_type_1.pdf`) and Diabetic Ketoacidosis (`1726567244_diabetic_ketoacidosis.pdf`) were identified during scanning but excluded per clinical scope guidelines.

### 3.2 MoHFW STG Corpus Audit
1. **Removal of CVD Part 1 (`mohfw_stg_cardiovascular_diseases_part1.pdf` / `3811.pdf`):**
   - The Table of Contents of `3811.pdf` was audited page by page:
     - Pages 5–11: Congenital Heart Disease
     - Page 12: Rheumatic Fever Algorithm
     - Pages 13–31: Acute Coronary Syndrome (ACS) / NSTEMI / Unstable Angina
     - Pages 32–40: ST-Elevation Myocardial Infarction (STEMI)
   - Coverage for primary adult hypertension diagnosis or outpatient pharmacotherapy: **0 pages**. (Mentions of BP are incidental to acute myocardial infarction hemodynamic monitoring or secondary pulmonary hypertension in CHD).
   - **Decision:** Removed completely from the corpus, download pipeline, catalog, and inventory to maintain clinical focus and avoid retrieval contamination.
2. **MoHFW Endocrinology (`mohfw_stg_endocrinology_diabetes.pdf` / `3601.pdf`):**
   - Page range audit of Table of Contents:
     - Topic 1: **Diabetes Mellitus** spans pages **6–21** (p.6 Introduction; p.21 References 3 & 4).
     - Topic 2: Hirsutism begins on page 22 (through p.26).
     - Topics 3–7: Hypothyroidism (p.27), Osteoporosis (p.28), PCOS (p.32), Thyrotoxicosis (p.39), Obesity (p.41).
   - **Action:** Set `relevant_page_ranges: "6-21"` in inventory to bound ingestion strictly to Diabetes Mellitus.
   - **Publication Date:** Document checked across all 49 pages; no publication date is printed for the volume. Set strictly to `null`.
3. **MoHFW Hypertension Background vs. Quick Reference:**
   - `mohfw_htn_001` (5191.pdf, 144 pages, printed date `March 2016`) is tagged explicitly as `(Background Document)`.
   - `mohfw_htn_002` (6591.pdf, 54 pages, printed date `May 2016`) is tagged as `(Quick Reference Guide)`.

### 3.3 WHO & NICE Primary Guideline Audit
1. **WHO Scope:**
   - Strictly restricted to the two primary guideline picks:
     - `who_htn_001` (2021, 61 pages): Guideline for the Pharmacological Treatment of Hypertension in Adults.
     - `who_t2dm_001` (2020, 35 pages): HEARTS-D Diagnosis and Management of Type 2 Diabetes.
2. **Version String Audit:**
   - No version numbers (e.g. "1.0", "Part 1") are printed as explicit edition versions on any of the WHO, NICE, ICMR, or MoHFW documents. Per instruction, all `version` fields are recorded as `null`.
3. **NICE Guidelines:**
   - `nice_htn_001` (NG136, 52 pages): Published 28 August 2019, updated February 2026.
   - `nice_t2dm_001` (NG28, 131 pages): Published 2 December 2015, updated February 2026.

---

## 4. Licensing Terms & Reuse Verification

All document licences have been replaced with the exact official terms quoted verbatim from the source authorities:

- **WHO:** Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO (**CC BY-NC-SA 3.0 IGO**). Quoted from page 4 of guidelines:
  > *"Some rights reserved. This work is available under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO licence (CC BY-NC-SA 3.0 IGO; https://creativecommons.org/licenses/by-nc-sa/3.0/igo). Under the terms of this licence, you may copy, redistribute and adapt the work for non-commercial purposes, provided the work is appropriately cited."* (URL: https://www.who.int/about/policies/publishing/copyright)

- **ICMR / DHR:** Official Government STW Publication:
  > *"This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and available scientific evidence. ... © Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India."* (URL: https://www.icmr.gov.in/standard-treatment-workflows-stws)

- **NICE (UK):** Clause 18 Notice of Rights (identical quote applied everywhere):
  > *"18. Reproduction, publication or distribution of the content from the website, including NICE copyright material, is subject to the following 'Notice of Rights': Copyright content owned by the National Institute for Health and Care Excellence (NICE) is made available for reuse to individuals and commercial/non-commercial organisations on a non-exclusive basis in the United Kingdom only under the NICE UK Open Content Licence. Except for personal use, study or personal research, copyright content owned by the National Institute for Health and Care Excellence (NICE) may not be used, reproduced, translated, distributed or transmitted in any form, in whole or in part, by any means, electronic, mechanical, photocopying, recording or otherwise, without prior written permission from NICE."* (URL: https://www.nice.org.uk/terms-and-conditions#notice-of-rights)

- **MoHFW (India):** Reuse label changed to:
  > **"Permission required before reproduction; source acknowledgement required"**  
  > Quoted from MoHFW Copyright Policy:
  > *"Material featured on this Portal may be reproduced free of charge after taking proper permission by sending a mail to us. However, the material has to be reproduced accurately and not to be used in a derogatory manner or in a misleading context. Wherever the material is being published or issued to others, the source must be prominently acknowledged."* (URL: https://clinicalestablishments.mohfw.gov.in/en/copyright-policy)

---

## 5. Per-Page Text Extractability & OCR Feasibility Audit

Every page of every document (528 total pages across 9 files) was audited for digital text extractability using PyMuPDF:

| Document | Total Pages | Digital Text Extractable? | Blank / Cover Pages (<50 chars) | Sparse Pages with Diagrams / Flowcharts (50–200 chars) |
|---|---|---|---|---|
| `who_htn_pharmacological_treatment_2021.pdf` | 61 | **Yes (100%)** | p.2 (blank), p.12 (blank), p.61 (back cover) | p.3 (title page, 73 chars) |
| `who_t2dm_hearts_d_2020.pdf` | 35 | **Yes (100%)** | p.1 (cover), p.2 (blank verso), p.3 (half-title) | None |
| `icmr_htn_hypertension_in_adults.pdf` | 1 | **Yes (100%)** | None (5,744 chars) | None |
| `icmr_t2dm_diabetes_type2.pdf` | 1 | **Yes (100%)** | None (4,668 chars) | None |
| `nice_ng136_hypertension.pdf` | 52 | **Yes (100%)** | None | None |
| `nice_ng28_type2_diabetes.pdf` | 131 | **Yes (100%)** | None | None |
| `mohfw_stg_hypertension_full.pdf` | 144 | **Yes (100%)** | None | p.127 (embedded flowchart diagram image) |
| `mohfw_stg_hypertension_quickref.pdf` | 54 | **Yes (100%)** | None | p.40, p.44, p.52 (embedded flowchart vector/raster drawings) |
| `mohfw_stg_endocrinology_diabetes.pdf` | 49 | **Yes (100%)** | None | None |

### Key Findings on Image & Flowchart Pages
1. **ICMR 1-Page Posters:**
   - Both posters are completely selectable digital text (5,744 characters for HTN; 4,668 characters for T2DM). The visual workflow boxes contain standard vector fonts, meaning **no OCR is required** to extract all clinical nodes, drug names, thresholds, and referral criteria.
2. **MoHFW Flowchart Pages:**
   - `mohfw_stg_hypertension_full.pdf` p.127 contains a raster image of the primary screening/management flowchart ("Ref: (23)"). Text extracted digitally is only 106 characters (page header/footer and reference tag).
   - `mohfw_stg_hypertension_quickref.pdf` contains 3 flowchart pages:
     - p.40: Evaluation and management algorithm of hypertension in adults (77 digital chars; 234 vector drawing objects).
     - p.44: Management of hypertension in diabetic patients (52 digital chars; 234 vector drawing objects).
     - p.52: Management of hypertension in pregnancy (184 digital chars; 234 vector drawing objects).
3. **OCR Recommendation for Phase 1:**
   - For 524 out of 528 pages (99.2%), standard text extraction with PyMuPDF extracts 100% of guideline recommendations, dosage tables, and clinical evidence.
   - For the 4 MoHFW flowchart pages (`mohfw_full` p.127; `mohfw_quickref` p.40, 44, 52), OCR (or manual markdown transcription of the visual decision trees) can be selectively enabled during extraction if visual tree fidelity is desired.

---

## 6. Next Phase Approval Request

With all 8 reconnaissance items addressed with complete precision, verified against disk, and passing all tests, Phase 0 is complete.
Ingestion chunking (Phase 1) is ready to proceed upon user approval.
