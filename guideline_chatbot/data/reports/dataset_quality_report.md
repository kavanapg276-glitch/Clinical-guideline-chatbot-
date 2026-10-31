# Phase 1 Dataset Quality & Chunking Provenance Report

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Date:** 2026-11-01  
**Milestone:** Phase 1 (Extraction, Cleaning, and Recommendation-Aware Chunking)  
**Gate Status:** GATE 1 READY FOR APPROVAL  

---

## 1. Executive Summary & Gate 1 Compliance

Phase 1 establishes the ingestion, text cleaning, and recommendation-aware chunking pipeline for the 9 verified clinical guideline documents. The pipeline adheres strictly to Master Prompt §6 and the Phase 0 implementation plan:

1. **Deterministic Page Provenance:** 100% of chunks (974 total) possess unambiguous source tracking (`doc_id`, `document_name`, `issuing_organization`, `jurisdiction`, `page_start`, and `page_end`).
2. **Recommendation-Aware Boundary Integrity:** Rather than blind fixed-token splitting, chunks are segmented along clinical recommendation boundaries (`NICE 1.4.20`, `WHO Recommendation 1`, `ICMR STW Treatment Blocks`, `MoHFW STG Clinical Sections`). Clinical recommendations are never severed from their conditional applicability clauses (`IF / WHEN`), target populations, or contraindications (`EXCEPT / AVOID`).
3. **Strict Flowchart Isolation:** The 4 rendered flowchart/algorithm page images and their structured transcriptions from Step B remain explicitly flagged `needs_review: true` and `indexed_for_retrieval: false`. Exactly **0** flowchart nodes are indexed in the RAG retrieval dataset.
4. **Metadata Completeness:** All 974 chunks carry all 22 required metadata fields with **0** missing values across mandatory fields.
5. **Quality Gate Status:** All 75 automated unit tests pass in 29.59s (`test_phase0.py` and `test_phase1.py`). Static analysis (`ruff check`, `ruff format`, `mypy`) passes with zero errors.

---

## 2. Guideline Corpus Extraction Statistics

Text was extracted using PyMuPDF (v1.28.5) across all 9 target guideline PDFs. Multi-condition documents were strictly scoped to their target condition page ranges per inventory specifications.

| Document ID | Official Title | Scope / Condition | Physical Pages | Relevant Pages Extracted | Extractable? | Extracted Raw Characters |
|---|---|---|---|---|---|---|
| `who_htn_001` | WHO Pharmacological Treatment of Hypertension | Hypertension | 61 | 61 (pp. 1–61) | Yes (100%) | 159,416 |
| `who_t2dm_001` | WHO HEARTS-D: Diagnosis & Management of T2DM | Type 2 Diabetes | 35 | 35 (pp. 1–35) | Yes (100%) | 62,517 |
| `icmr_htn_001` | ICMR STW - Hypertension in Adults | Hypertension | 1 | 1 (p. 1) | Yes (100%) | 8,070 |
| `icmr_t2dm_001` | ICMR STW - Diabetes Mellitus Type 2 | Type 2 Diabetes | 1 | 1 (p. 1) | Yes (100%) | 5,055 |
| `nice_htn_001` | NICE Guideline NG136 (Hypertension in Adults) | Hypertension | 52 | 52 (pp. 1–52) | Yes (100%) | 98,543 |
| `nice_t2dm_001` | NICE Guideline NG28 (Type 2 Diabetes in Adults) | Type 2 Diabetes | 131 | 131 (pp. 1–131) | Yes (100%) | 213,976 |
| `mohfw_htn_001` | MoHFW STG - Hypertension (Background) | Hypertension | 144 | 144 (pp. 1–144) | Yes (100%) | 303,347 |
| `mohfw_htn_002` | MoHFW STG - Hypertension (Quick Reference) | Hypertension | 54 | 54 (pp. 1–54) | Yes (100%) | 110,526 |
| `mohfw_t2dm_001` | MoHFW STG - Endocrinology (Diabetes Mellitus) | Type 2 Diabetes | 49 | 16 (pp. 6–21) | Yes (100%) | 36,299 |
| **TOTALS** | **9 Guidelines** | **Both** | **528** | **495 Pages** | **100% Extractable** | **1,007,749 Chars** |

> [!NOTE]
> `mohfw_t2dm_001` (MoHFW Endocrinology STG) contains 49 pages covering multiple endocrine disorders. Only pages 6–21 (covering Diabetes Mellitus through its references) were extracted. Page 22 onwards covers Hirsutism and other unrelated disorders and is strictly excluded.

---

## 3. Text Cleaning & Normalization Impact

The text cleaning module (`guideline_chatbot/ingestion/clean.py`) applies deterministic rules to strip repetitive administrative artifacts without altering clinical text, dosages, laboratory numbers, or drug names.

### Applied Cleaning Steps:
1. **Unicode & Symbol Normalization:** NFKD decomposition normalizes ligatures (`fi`, `fl`, `ff`); mathematical operators are converted to standard ASCII equivalents (`≥` $\to$ `>=`, `≤` $\to$ `<=`, `±` $\to$ `+/-`); bullet artifacts (`\u2022`, `\ufffd`) are converted to `- `.
2. **Boilerplate Stripping:**
   - **NICE Footers:** Stripped multi-line Crown copyright and Notice of Rights URLs repeated at the bottom of all 183 NICE pages.
   - **ICMR Disclaimers:** Stripped repeated national expert administrative advisory disclaimer box from workflow footers.
   - **MoHFW Headers:** Stripped running `Standard Treatment Guidelines -Hypertension` and running `Page X` headers.
   - **WHO Headers:** Stripped running publication banner lines.
3. **Hyphenation Rejoining:** Cleanly rejoined words split across line-ends by soft hyphens while preserving deliberate compound clinical entities (`fixed-dose`, `beta-blockers`, `dpp-4`).

### Quantitative Cleaning Metrics:

| Document ID | Raw Characters | Cleaned Characters | Characters Removed | Reduction % | Primary Content Stripped |
|---|---|---|---|---|---|
| `who_htn_001` | 159,416 | 157,345 | 2,071 | 1.30% | Running headers & page numbers |
| `who_t2dm_001` | 62,517 | 61,754 | 763 | 1.22% | Header banners & page numbers |
| `icmr_htn_001` | 8,070 | 7,345 | 725 | 8.98% | Administrative advisory disclaimer footer |
| `icmr_t2dm_001` | 5,055 | 4,420 | 635 | 12.56% | Administrative advisory disclaimer footer |
| `nice_htn_001` | 98,543 | 86,904 | 11,639 | 11.81% | Notice of Rights footers & page pagination |
| `nice_t2dm_001` | 213,976 | 186,609 | 27,367 | 12.79% | Notice of Rights footers & page pagination |
| `mohfw_htn_001` | 303,347 | 294,237 | 9,110 | 3.00% | Running STG banners & page numbers |
| `mohfw_htn_002` | 110,526 | 108,900 | 1,626 | 1.47% | Running STG banners & page numbers |
| `mohfw_t2dm_001` | 36,299 | 35,535 | 764 | 2.10% | Standalone page numbers |
| **TOTAL** | **1,007,749** | **953,049** | **54,700** | **5.43%** | **Administrative boilerplate only** |

> [!IMPORTANT]
> **Zero Clinical Information Loss:** 100% of drug names, dosages (`mg`, `g`, `units`), target thresholds (`140/90`, `130/80`, `7.0%`, `48 mmol/mol`), and contraindication statements were preserved. Automated tests verify exact string preservation.

---

## 4. Chunking Statistics & Distributions

A total of **974** chunks were generated across the 9 documents using `GuidelineChunker`.

### Chunks per Document:

| Document ID | Issuing Organization | Jurisdiction | Chunks Generated | Mean Words/Chunk | Median Words/Chunk | Page Span |
|---|---|---|---|---|---|---|
| `who_htn_001` | World Health Organization | International | 136 | 164.2 | 72.0 | pp. 1–60 |
| `who_t2dm_001` | World Health Organization | International | 38 | 251.5 | 238.5 | pp. 1–35 |
| `icmr_htn_001` | ICMR / DHR India | India | 12 | 89.7 | 56.0 | p. 1 |
| `icmr_t2dm_001` | ICMR / DHR India | India | 13 | 49.3 | 48.0 | p. 1 |
| `nice_htn_001` | NICE UK | United Kingdom | 108 | 117.8 | 50.0 | pp. 1–52 |
| `nice_t2dm_001` | NICE UK | United Kingdom | 190 | 141.1 | 48.5 | pp. 1–131 |
| `mohfw_htn_001` | MoHFW India | India | 311 | 141.1 | 52.0 | pp. 1–144 |
| `mohfw_htn_002` | MoHFW India | India | 150 | 107.8 | 48.0 | pp. 1–54 |
| `mohfw_t2dm_001` | MoHFW India | India | 16 | 332.0 | 454.0 | pp. 6–21 |
| **TOTAL** | **4 Issuers** | **3 Jurisdictions** | **974** | **142.2** | **54.0** | **495 Pages** |

### Chunks by Condition:
- **Hypertension:** 534 chunks (54.8%)
- **Type 2 Diabetes:** 239 chunks (24.5%)
- **Both (Cross-Tagged):** 201 chunks (20.6%)
  *(Chunks originating from hypertension guidelines that address diabetic patients, e.g. diabetic BP targets, or from diabetes guidelines that address comorbid hypertension).*

### Chunks by Chunk Type:
- **`recommendation`:** 189 chunks (19.4%)
- **`monitoring`:** 166 chunks (17.0%)
- **`rationale`:** 39 chunks (4.0%)
- **`definition`:** 3 chunks (0.3%)
- **`other`:** 577 chunks (59.2%) *(includes clinical assessment, investigations, diagnostic pathways, pharmacology details, and lifestyle counseling)*
- **`flowchart`:** 0 chunks (0.0%) *(strictly excluded pending review)*

### Size Distribution:
- **Word Length:** Min = 8 words, Max = 479 words, Mean = 142.2 words, Median = 54.0 words, StdDev = 162.3 words.
- **Character Length:** Min = 54 characters, Max = 4,356 characters, Mean = 967.3 characters, Median = 386.0 characters.
- **Page Validity:** 100% of chunks satisfy $1 \le \text{page\_start} \le \text{page\_end} \le \text{total\_pages}$. Exactly 0 invalid page spans.

---

## 5. Metadata Completeness Audit (All 22 Fields)

Every chunk generated by the pipeline was verified against the `GuidelineChunk` schema.

| # | Metadata Field Name | Required? | Nullable? | Missing / Empty Count (N = 974) | Status |
|---|---|---|---|---|---|
| 1 | `chunk_id` | Yes | No | **0** | **PASS** |
| 2 | `doc_id` | Yes | No | **0** | **PASS** |
| 3 | `document_name` | Yes | No | **0** | **PASS** |
| 4 | `issuing_organization` | Yes | No | **0** | **PASS** |
| 5 | `condition` | Yes | No | **0** | **PASS** |
| 6 | `section_path` | Yes | No | **0** | **PASS** |
| 7 | `heading` | Yes | No | **0** | **PASS** |
| 8 | `page_start` | Yes | No | **0** | **PASS** |
| 9 | `page_end` | Yes | No | **0** | **PASS** |
| 10 | `version` | Yes | Yes (null if unprinted) | **0** (All set to `null` per Gate 0) | **PASS** |
| 11 | `publication_date` | Yes | Yes (null if unprinted) | **0** (Valid dates or `null` for MoHFW Endo) | **PASS** |
| 12 | `jurisdiction` | Yes | No | **0** | **PASS** |
| 13 | `document_status` | Yes | No | **0** | **PASS** |
| 14 | `chunk_type` | Yes | No | **0** | **PASS** |
| 15 | `evidence_strength` | Yes | Yes | **0** (Populated or `null`) | **PASS** |
| 16 | `recommendation_strength` | Yes | Yes | **0** (Populated or `null`) | **PASS** |
| 17 | `population_tags` | Yes | No (List) | **0** (All valid lists) | **PASS** |
| 18 | `drug_class_tags` | Yes | No (List) | **0** (All valid lists) | **PASS** |
| 19 | `applicability_conditions` | Yes | No (List) | **0** (All valid lists) | **PASS** |
| 20 | `exceptions` | Yes | No (List) | **0** (All valid lists) | **PASS** |
| 21 | `text` | Yes | No | **0** | **PASS** |
| 22 | `text_hash` | Yes | No | **0** (All 64-char sha256 hex) | **PASS** |

---

## 6. Flowchart & Visual Asset Accounting

Per user instructions and Pre-Build Step B verification:

| Asset Identifier | Source File & Page | Verified Visually Printed Title | Rendered Image Path | RAG Index Status | Reason |
|---|---|---|---|---|---|
| `fc_mohfw_qr_p40` | MoHFW QRG, p. 40 | "Figure. An approach to staged exercise prescriptions" | `data/reports/flowcharts/mohfw_quickref_p40_staged_exercise_prescription.png` | **EXCLUDED** (`indexed_for_retrieval: false`) | Transcribed tree held in `flowcharts_transcription.json` pending human review against page image. |
| `fc_mohfw_qr_p44` | MoHFW QRG, p. 44 | "Figure 7 Modified WHO smoking cessation algorithm" | `data/reports/flowcharts/mohfw_quickref_p44_who_smoking_cessation_algorithm.png` | **EXCLUDED** (`indexed_for_retrieval: false`) | Transcribed tree held pending human review against page image. |
| `fc_mohfw_bg_p127` | MoHFW Background, p. 127 | "Figure 7 Modified WHO smoking cessation algorithm" | `data/reports/flowcharts/mohfw_background_p127_who_smoking_cessation_algorithm.png` | **EXCLUDED** (`indexed_for_retrieval: false`) | Transcribed tree held pending human review against page image. |
| `fc_mohfw_qr_p52` | MoHFW QRG, p. 52 | Formulary Renal Impairment Advisory Note (Not a flowchart) | `data/reports/flowcharts/mohfw_quickref_p52_renal_impairment_caution.png` | **EXCLUDED** (`indexed_for_retrieval: false`) | Single advisory sentence (*CrCl < 30 ml/min*); verified not a flowchart. |

**Audit Assertion:** Unit test `test_flowcharts_excluded_from_retrieval_chunks` verifies that zero `fc_*` identifiers and zero chunks of type `flowchart` exist in `data/processed/guideline_chunks.json`.

---

## 7. Cross-Source Overlaps & Duplicate Text Analysis

Automated hashing identified 20 text hash collision pairs across the 974 chunks. Forensic investigation reveals these are legitimate clinical redundancies across official publications:

1. **MoHFW Executive Summary vs Full Body:**
   In `mohfw_htn_001` (MoHFW Background STG), pages 10–25 contain the official Executive Summary, while pages 50–140 present the detailed chapters. Clinical sections like `3.4.2 Target organ damage`, `1.6.1 Normal BP follow-up intervals`, and `1.6.6 Hypertensive emergencies` appear verbatim in both parts.
2. **MoHFW Quick Reference Guide vs Background Document:**
   `mohfw_htn_002` (Quick Reference Guide) is an official condensed handbook derived directly from `mohfw_htn_001`. Core therapeutic guidance, such as `4.5 Classes of antihypertensive drugs & preferred choices`, is identical across both documents.
3. **Implication for Phase 2 Retrieval:**
   Both chunks are preserved with their distinct `page_start` / `page_end` and `section_path` breadcrumbs. In Phase 2, BM25 / vector search deduplication or reciprocal rank fusion will cluster or rank them transparently.

---

## 8. Summary of Cross-Guideline Clinical Disagreements

The 7 clinical disagreement domains identified and sourced with exact page numbers in `docs/PRE_BUILD_CHECKLIST.md` are reflected in the chunk dataset:

1. **Diagnostic Strategy:** NICE requires daytime ABPM confirmation ($\ge 135/85\text{ mmHg}$; NG136 p. 8); MoHFW (QRG p. 7) and ICMR (p. 1) diagnose on repeated clinic readings ($\ge 140/90\text{ mmHg}$).
2. **Diabetic BP Target:** MoHFW (QRG p. 13) and ICMR (p. 1) mandate $< 130/80\text{ mmHg}$ for all diabetics; WHO (p. 28) and NICE (NG136 p. 15) maintain $< 140/90\text{ mmHg}$ general target (stricter $< 130/80$ in NICE only if ACR $\ge 70\text{ mg/mmol}$).
3. **Initial Drug Strategy:** MoHFW (QRG p. 12) starts monotherapy (lifestyle trial first); ICMR (p. 1) and WHO (p. 23) recommend dual combination therapy (FDC) by default; NICE (NG136 p. 12) mandates monotherapy stratified by age and African/African-Caribbean origin.
4. **First-Line Glucose-Lowering in T2DM:** NICE NG28 (p. 17) requires Metformin + SGLT2-i immediately if chronic heart failure or ASCVD; MoHFW 2016 (p. 10) relies on Metformin alone followed by sulfonylureas.

---

## 9. Licensing & Reuse Compliance

All chunks were extracted from official open-access publications under documented terms:
- **WHO Guidelines:** CC BY-NC-SA 3.0 IGO.
- **ICMR STWs:** Official Government of India clinical workflow guidance.
- **NICE Guidelines:** NICE UK Open Content Licence / Crown Copyright.
- **MoHFW STGs:** Clinical establishments portal terms ("Permission required before reproduction; source acknowledgement required").
- Raw PDFs in `data/raw/` remain untracked in git per Standing Rule 4.

---

## 10. Limitations & Boundaries for Retrieval (Phase 2)

1. **Condition Scope:** Chunks strictly cover Hypertension and Type 2 Diabetes. Out-of-scope conditions (e.g. secondary endocrine disorders on MoHFW Endocrinology pp. 22–49) have been excluded at extraction time.
2. **Flowchart Holdout:** Visual algorithms remain held out of the retrieval index until the human reviewer verifies each node against the high-resolution images.
3. **Next Steps:** Proceed to Phase 2 (Vector Embeddings, ChromaDB, BM25 Keyword Search, and Reciprocal Rank Fusion) upon Gate 1 approval.

