# Pre-Build Checklist & Cross-Guideline Clinical Analysis

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Date:** 2026-11-01  
**Milestone:** Phase 0 Gate Approved → Pre-Build Step B  

---

## 1. Executive Summary & Gate 0 Adjustments

Phase 0 setup and dataset acquisition has been approved with two specific adjustments:
1. **Unspecified Date Types:** All printed dates whose exact legal/administrative meaning (e.g. publication vs review vs effective) is not explicitly defined in the document have been recorded with `date_type: "unspecified"`. Specifically, the ICMR Hypertension printed date `"May/2026"` and ICMR Diabetes printed date `"July/ 2022"` are treated as printed dates of unspecified type without editorial inference.
2. **Flowchart Visual Assets (Option A):** All 4 embedded flowchart algorithm pages across the MoHFW STG corpus have been rendered as high-resolution (1700 × 2200 px) PNG images and transcribed into structured decision-tree nodes. Each is tagged `needs_review: true` and `indexed_for_retrieval: false`. They will remain excluded from vector indexing until human verification against the page images is complete.
3. **LLM Provider Configuration:** The LLM client remains set to the local deterministic **Mock LLM** through Phases 1 and 2. Real provider selection (Ollama local vs OpenAI-compatible API) is deferred to Phase 3.

---

## 2. Acquired Corpus Integrity Verification

All 9 documents on disk are authentic, complete, valid PDFs starting with the `%PDF-` header:

| Doc ID | Organization | Document Title | Condition | Pages | Size (bytes) | SHA-256 (prefix) | Printed Date | Date Type | Version |
|---|---|---|---|---|---|---|---|---|---|
| `who_htn_001` | WHO | Pharmacological Treatment of Hypertension in Adults | HTN | 61 | 843,539 | `57f6376d5c9b...` | 2021 | `publication` | null |
| `who_t2dm_001` | WHO | HEARTS-D: Diagnosis and Management of Type 2 Diabetes | T2DM | 35 | 1,248,098 | `71b216b19a22...` | 2020 | `publication` | null |
| `icmr_htn_001` | ICMR / DHR | STW - Hypertension in Adults (ICD-11 BA00) | HTN | 1 | 3,297,566 | `bffc8acfa65c...` | May/2026 | `unspecified` | null |
| `icmr_t2dm_001` | ICMR / DHR | STW - Diabetes Mellitus Type 2 (ICD-10-E11) | T2DM | 1 | 332,368 | `bcad0bfca7c2...` | July/ 2022 | `unspecified` | null |
| `nice_htn_001` | NICE (UK) | NG136: Hypertension in Adults | HTN | 52 | 296,345 | `3f8255bf9c16...` | 2019-08-28 | `publication` | null |
| `nice_t2dm_001` | NICE (UK) | NG28: Type 2 Diabetes in Adults | T2DM | 131 | 569,249 | `249e1f3ad3d1...` | 2015-12-02 | `publication` | null |
| `mohfw_htn_001` | MoHFW (India) | STG - Hypertension (Background Document) | HTN | 144 | 1,438,955 | `8388906c4f3c...` | March 2016 | `unspecified` | null |
| `mohfw_htn_002` | MoHFW (India) | STG - Hypertension (Quick Reference Guide) | HTN | 54 | 1,748,005 | `62de7ccc3b98...` | May 2016 | `unspecified` | null |
| `mohfw_t2dm_001` | MoHFW (India) | STG - Endocrinology (Diabetes Mellitus, p.6-21) | T2DM | 49 | 725,300 | `7f681425fa91...` | null | null | null |

---

## 3. Flowchart Extraction & Verification Assets (Option A)

The 4 complex flowchart pages have been extracted to [`guideline_chatbot/data/reports/flowcharts/`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/):

1. **`mohfw_quickref_p40_adult_htn_algorithm.png`**:
   - High-resolution rendering of MoHFW QRG p. 40.
   - Content: Exercise prescription & pre-exercise cardiovascular risk screening algorithm (Source: Ref 85, Metkus et al.).
2. **`mohfw_quickref_p44_diabetic_htn_algorithm.png`**:
   - High-resolution rendering of MoHFW QRG p. 44.
   - Content: Overall adult hypertension diagnosis, risk stratification & management algorithm (Source: Ref 23).
3. **`mohfw_background_p127_screening_diagnosis_flowchart.png`**:
   - High-resolution rendering of MoHFW Background Document p. 127.
   - Content: Corresponds to Section 7 Management Pathway algorithm (Source: Ref 23).
4. **`mohfw_quickref_p52_pregnancy_htn_algorithm.png`**:
   - High-resolution rendering of MoHFW QRG p. 52.
   - Content: Antihypertensive formulary guidance with renal failure exclusion footnote (`CrCl < 30 ml/min`).

Structured JSON and Markdown representations are stored in:
- [`flowcharts_transcription.json`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/flowcharts_transcription.json)
- [`flowcharts_transcription.md`](file:///c:/Users/kavan/OneDrive/Desktop/capstone/guideline_chatbot/data/reports/flowcharts/flowcharts_transcription.md)

All nodes carry:
```json
{
  "needs_review": true,
  "indexed_for_retrieval": false,
  "verification_status": "draft_pending_human_verification"
}
```

---

## 4. Cross-Guideline Clinical Disagreement Table

Because clinical guidelines evolve across jurisdictions and time periods, the RAG chatbot must be aware of genuine guideline contradictions. Below is the evidentiary matrix of clinical divergence across our primary sources:

| Clinical Domain | India MoHFW (2016) | India ICMR STW (2022/2026) | WHO Guidelines (2020/2021) | NICE Guidelines (UK, NG136/NG28) | Clinical Implication for RAG / Coherence Layer |
|---|---|---|---|---|---|
| **Diagnostic Confirmation Strategy** | SBP $\ge 140$ or DBP $\ge 90\text{ mmHg}$ on $\ge 2$ clinic visits. No requirement for out-of-office BP. *(MoHFW QRG p. 7)* | SBP $\ge 140$ or DBP $\ge 90\text{ mmHg}$ on 2 clinic visits. Single visit sufficient if SBP $\ge 160$ or DBP $\ge 100$. *(ICMR HTN sheet)* | SBP $\ge 140$ or DBP $\ge 90\text{ mmHg}$. Initiate treatment immediately if SBP $\ge 140/90$ (or 130–139 if known CVD). *(WHO 2021 p. 17)* | Clinic BP $\ge 140/90\text{ mmHg}$ **must be confirmed with ABPM or HBPM**. Stage 1 = Clinic $\ge 140/90$ **and** daytime ABPM/HBPM $\ge 135/85$. *(NG136 §1.2)* | **High Divergence:** NICE forbids diagnosing Stage 1 on clinic BP alone without ABPM/HBPM. RAG must not flag Indian practice as invalid when answering Indian jurisdiction queries. |
| **General Blood Pressure Target** | $< 140/90\text{ mmHg}$ in adults $< 80$ years; $< 150/90\text{ mmHg}$ if $\ge 80$ years. *(MoHFW Background p. 114)* | $< 140/90\text{ mmHg}$ in general; $< 150/90$ in elderly $\ge 80$ years. *(ICMR HTN sheet)* | $< 140/90\text{ mmHg}$ in all adults with hypertension without comorbidities. SBP $< 130$ if known CVD. *(WHO 2021 p. 27)* | Clinic $< 140/90\text{ mmHg}$ (daytime ABPM $< 135/85$) in adults $< 80$ years; Clinic $< 150/90$ (ABPM $< 145/85$) if $\ge 80$ years. *(NG136 §1.4)* | Broad consensus on $< 140/90$ general, but NICE explicitly anchors targets to out-of-office ABPM readings ($135/85$). |
| **Blood Pressure Target in Diabetes Mellitus** | **$< 130/80\text{ mmHg}$** target in all diabetic patients or patients with proteinuria. *(MoHFW QRG p. 13)* | **$< 130/80\text{ mmHg}$** in patients with diabetes, CVD, or CKD. *(ICMR HTN & T2DM sheets)* | **$< 140/90\text{ mmHg}$** for general diabetes without CVD; SBP $< 130$ only if known CVD. *(WHO 2021 p. 28)* | **$< 140/90\text{ mmHg}$** (daytime ABPM $< 135/85$). Stricter $< 130/80$ target applies **only if CKD with ACR $\ge 70\text{ mg/mmol}$**. *(NG136 §1.4.5 & NG28)* | **Direct Disagreement:** Indian guidelines maintain aggressive $< 130/80$ for all diabetics, whereas NICE NG136 and WHO 2021 deliberately relaxed general diabetic targets to $< 140/90$. |
| **Initial Pharmacotherapy Strategy (Monotherapy vs Dual)** | **Monotherapy first:** 3-month trial of lifestyle for Grade 1; start single drug, titrate, then add second agent if uncontrolled. *(MoHFW QRG p. 12)* | **Dual combination by default:** "Combination therapy (two drugs from two different classes) could be the default initial pharmacological treatment for most adults." *(ICMR HTN)* | **Combination preferred:** Suggests initial combination therapy (preferably fixed-dose single-pill combination, FDC) for adults requiring pharmacotherapy. *(WHO 2021 p. 23)* | **Stepwise Monotherapy:** Strictly stratified monotherapy at Step 1, moving to dual combination only at Step 2. Single-pill combinations not default first-line. *(NG136 §1.4)* | **Evolutionary Divergence:** Older MoHFW 2016 and NICE advocate monotherapy start; newer ICMR (2022) and WHO (2021) advocate initial dual combination (FDC). |
| **First-Line Antihypertensive Drug Classes** | Age-based choice: $< 60$ years $\to$ ACEi or ARB (or CCB); $\ge 60$ years $\to$ CCB or Thiazide diuretic. In diabetes $\to$ ACEi/ARB. *(MoHFW QRG p. 13)* | Dual combination of **RAAS blocker (ACEi or ARB) + CCB or Thiazide/Thiazide-like diuretic** in single-pill combination (FDC). *(ICMR HTN sheet)* | Any of 3 classes: thiazide/thiazide-like, ACEi/ARB, or CCB. *(WHO 2021 p. 21)* | **Age and Ethnicity Stratified:**<br>• $< 55\text{y}$, non-Black: ACEi or ARB (A)<br>• $\ge 55\text{y}$ OR Black African/African-Caribbean origin (any age): CCB (C)<br>• If CCB intolerant: Thiazide-like (indapamide)<br>• T2DM (any age/origin): ACEi or ARB. *(NG136 §1.4)* | **Ethnic/Demographic Stratification:** NICE uniquely stratifies first-line choice by African/African-Caribbean ancestry due to renin profile; MoHFW and ICMR tailor to South Asian clinical considerations. |
| **First-Line Glucose-Lowering Therapy in T2DM** | **Metformin monotherapy** as initial drug of choice; sulfonylureas added second-line. *(MoHFW Endo p. 10)* | **Metformin monotherapy** first-line; initiate dual therapy if $\text{HbA1c} > 8.5\%$ or $> 1.5\%$ above target. *(ICMR T2DM sheet)* | **Metformin monotherapy** first line; sulfonylureas second line. Primary healthcare insulin protocol. *(WHO HEARTS-D p. 14)* | **Metformin + SGLT2-i:** If patient has chronic heart failure or established ASCVD, **combine Metformin with an SGLT2 inhibitor** with proven CV benefit immediately. *(NG28 §1.3.15)* | **Contemporary Cardiorenal Protection:** NICE NG28 mandates upfront SGLT2-i for high CV/renal risk; 2016 MoHFW guideline predates routine SGLT2-i first-line adoption. |
| **General Glycemic Target (HbA1c)** | $\text{HbA1c} < 7.0\%$ general; elderly $< 8.0\%$. *(MoHFW Endo p. 12)* | $\text{HbA1c} < 7.0\%$ general ($6.5\%$ young/newly diagnosed, $7.5\text{--}8.0\%$ elderly/frail). *(ICMR T2DM sheet)* | $\text{HbA1c} < 7.0\%$ general. *(WHO HEARTS-D p. 11)* | $48\text{ mmol/mol}$ ($6.5\%$) on lifestyle/monotherapy; $53\text{ mmol/mol}$ ($7.0\%$) on drugs with hypoglycemia risk or dual therapy. *(NG28 §1.3.6)* | Consensus around $\approx 7.0\%$, but NICE reports in IFCC units ($\text{mmol/mol}$) with dual $48/53$ target tiers. |

---

## 5. Architectural Implications for the Coherence Layer

The above clinical disagreements demonstrate why the **ClinCoherence Verification Layer** is essential:
1. **Target Mismatch & Jurisdiction Awareness:** When an Indian patient scenario asks about blood pressure targets in diabetes, answering `< 140/90` from NICE NG136 without noting the Indian MoHFW/ICMR recommendation of `< 130/80` represents a jurisdiction/target conflict.
2. **Evidence-Justified State Updates:** If a patient is diagnosed with Type 2 Diabetes during a conversation, the chatbot must update its BP target from `< 140/90` to `< 130/80` (under MoHFW/ICMR rules). If the chatbot drops this tighter target under user pushback ("my previous doctor said 140 was fine"), the Coherence Layer must flag an **unjustified belief reversal** or **correction collapse**.
3. **Contraindication Enforcement:** Both MoHFW and ICMR state: *"DO NOT combine two RAAS blockers (ACEi + ARB) as it increases the risk of acute kidney injury."* The coherence checker must deterministically catch any recommendation attempting dual ACEi + ARB therapy.
4. **Renal Safeguard Rules:** The MoHFW footnote (`CrCl < 30 ml/min`) forbids thiazides; the coherence layer must verify that patient lab state (`eGFR < 30`) triggers loop diuretics rather than thiazides.

---

## 6. Phase 1 Implementation Plan

With Gate 0 approved and Step B completed, Phase 1 will execute:
1. **Extraction (`extract_pdf.py`):**
   - High-fidelity per-page text extraction with native PyMuPDF font/layout analysis.
   - Multi-condition page range filters enforced (`relevant_page_ranges: "6-21"` for MoHFW Endocrinology).
2. **Cleaning (`clean.py`):**
   - Stripping running headers, footers, and Ministry boilerplate with logged before/after counts, preserving clinical recommendations intact.
3. **Recommendation-Aware Chunking (`recommendation_chunker.py`):**
   - Semantic clinical chunking by recommendation boundary (not fixed character counts).
   - Strict metadata enrichment: `doc_id`, `condition`, `heading`, `page_start`, `page_end`, `chunk_type`, `evidence_strength`, `population_tags`, `drug_class_tags`, `applicability_conditions`, `exceptions`.
4. **Flowchart Segregation:**
   - Transcribed flowchart nodes kept in `data/reports/flowcharts/` marked `needs_review: true`, excluded from ingestion chunks until user approval.
5. **Quality Audit:**
   - 30 randomly sampled chunks printed with provenance for review.
   - Comprehensive `data/reports/dataset_quality_report.md` generated.

---

## 7. Sign-Off & Next Steps

- [x] Phase 0 complete and verified.
- [x] Gate 0 adjustments (1) `date_type: unspecified` and (2) Option A flowcharts executed.
- [x] Step B `PRE_BUILD_CHECKLIST.md` produced with cross-source disagreement matrix.
- [x] Mock LLM confirmed active for offline testing.
- [ ] Awaiting user approval to begin Phase 1 (Extraction, Cleaning, and Recommendation-Aware Chunking).

