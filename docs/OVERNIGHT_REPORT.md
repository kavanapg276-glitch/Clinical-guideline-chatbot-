# Autonomous Overnight Execution Report

**Project:** ClinCoherence Chatbot 2 — Clinical Guideline-Based Decision Support  
**Scope:** Hypertension and Type 2 Diabetes  
**Run Mode:** Autonomous Multi-Stage Pipeline Execution  
**Started At:** 2026-11-01T01:30:00+05:30  
**Completed At:** 2026-11-01T02:30:00+05:30  
**Current Status:** COMPLETED (Stages 1, 2, and 3 fully completed and verified)  

---

## 1. Stage Progress & Status Overview

| Stage | Scope | Status | Test Result | Static Analysis | Deliverables / Evidence |
|---|---|---|---|---|---|
| **STAGE 1** | Phase 1b: Fix Chunking Defects, Tagging Rules, Table Integrity, Noise Isolation | **COMPLETED** | **79 passed** (13.81s) | **All checks passed** (Ruff, Mypy) | `docs/TAGGING_RULES.md`, `data/reports/chunk_audit_v2.md` (10/10 traps pass), 953 chunks generated |
| **STAGE 2** | Phase 2: Embeddings, ChromaDB, Hybrid BM25/Semantic Retrieval, Retrieval Gold Set | **COMPLETED** | **91 passed** (24.27s) | **All checks passed** (Ruff, Format, Mypy 26 files) | ChromaDB index (917 chunks), BM25 index, `retrieval_gold_set.json` (42 queries), `data/reports/retrieval_evaluation_report.md` |
| **STAGE 3** | Phase 3 Slice: Patient State, Citation Generator, CLI, 5 Demo Dialogues | **COMPLETED** | **109 passed** (14.76s) | **All checks passed** (Ruff, Format, Mypy 34 files) | `patient_state.py`, `llm_client.py`, `citation_validator.py`, `generator.py`, `orchestrator.py`, `cli.py`, 5 transcripts in `demo_conversations/` |

---

## 2. Stage 1 (Phase 1b) Detailed Execution & Evidence

### A. Key Accomplishments:
1. **Applicability vs. Mention Tagging Enforced:**
   - Population tags now strictly mean clinical recommendation applicability.
   - Detected negations ("without previously diagnosed hypertension or renal disease") prevent incorrect tagging (`nice_htn_001` 1.2.12 tags `type_2_diabetes`, cleanly excludes `chronic_kidney_disease`).
   - Disambiguated `type_1_diabetes` vs `type_2_diabetes` (NICE 1.4.20 tags `type_1_diabetes`, not `type_2_diabetes`).
   - Prevented general routine screening mentions (NICE 1.3.3 HbA1c panel) and adverse drug reactions (MoHFW 5.3.2 thiazide hyperglycemia) from falsely tagging diabetic population.
   - Scoped `condition: both` strictly to chunks governing both conditions concurrently.
2. **Metadata Versioning & Fields:**
   - Extracted NICE recommendation bracketed years into `recommendation_year` (230 chunks).
   - Extracted `last_updated` and `last_updated_source` from document titles/metadata (297 chunks).
   - Filled `evidence_strength` (22 chunks) and `recommendation_strength` (41 chunks) only from explicit clinical text.
   - Filtered `applicability_conditions` (79 chunks) and `exceptions` (89 chunks) from strict clause triggers only, setting non-matching chunks to `None`.
3. **Table & Noise Handling:**
   - Integrated PyMuPDF table detection and structured markdown tables.
   - Preserved all 13 drugs, doses, contraindications, and side effects from the ICMR HTN poster row-by-row with 0 mismatches.
   - Preserved all 3 HbA1c strata and metabolic targets from ICMR T2DM STW with 0 mismatches.
   - Reclassified noise sections as `reference`, `methods`, `front_matter`, `contributors` with `indexed_for_retrieval: false` (36 chunks).
   - Segmented MoHFW Endocrinology STG into 22 recommendation/section chunks.
   - Reclassified audited chunks (`1.4.10`, `1.4.20`, `1.4.50`, `1.24.4`, `4.5.5`, `4.8.1.2`, `4.11.6`, `4.12.2`) as `recommendation`.
4. **Disagreement Table Rebuilt:**
   - Sourced all cells of `docs/PRE_BUILD_CHECKLIST.md` directly from chunk text with document name, page number, chunk ID, and `human_verified: false`.
   - Corrected MoHFW diabetes BP target to `< 140/90 mmHg` (chunks `mohfw_htn_001_c0062` and `mohfw_htn_001_c0209`, citing JNC 8 rationale on p. 95).

### B. Corpus Metrics & Counts:
- **Total Chunks:** 953
- **Indexed for Retrieval:** 917 (96.2%)
- **Excluded from Retrieval (Noise/Flowchart/References):** 36 (3.8%)
- **Chunk Types:** `recommendation`: 623 (65.4%), `other`: 206 (21.6%), `table`: 39 (4.1%), `rationale`: 29 (3.0%), `reference`: 22 (2.3%), `front_matter`: 10 (1.0%), `definition`: 10 (1.0%), `monitoring`: 10 (1.0%), `methods`: 3 (0.3%), `contributors`: 1 (0.1%).
- **Condition Distribution:** `hypertension`: 659, `type_2_diabetes`: 245, `both`: 49.
- **Word Count Distribution:** Min = 20, Max = 488, Mean = 144.2 words. All chunks < 20 words merged or dropped.

---

## 3. Stage 2 (Phase 2) Detailed Execution & Evidence

### A. Key Accomplishments:
1. **Dense Vector Store & Normalization:**
   - Built `EmbeddingManager` wrapping `sentence-transformers/all-MiniLM-L6-v2` with `normalize_embeddings=True` (384-dimensional unit vectors), SQLite vector caching (`embeddings_cache.sqlite3`), and strict offline execution (`HF_HUB_OFFLINE=1`).
   - Built `VectorStore` with persistent ChromaDB storage in `chroma/` (`hnsw:space: cosine`). Indexed all 917 indexable chunks with complete metadata fields.
   - Enriched embedded representation: `[{issuing_organization}] {heading}\n{text}` providing crucial document and section context for dense similarity.
2. **Clinical Sparse Keyword Retrieval:**
   - Built `KeywordIndex` wrapping `rank_bm25.BM25Okapi` with clinical tokenization (`clinical_tokenize`).
   - Expanded 28 clinical acronyms/synonyms (HTN, T2DM, ACEi, ARB, CCB, eGFR, SBP, DBP, HbA1c, MRA, SGLT2i, GLP1RA, DPP4i, FDC, ATTACC, Spironolactone, ICMR, NICE, WHO, MoHFW).
   - Stopword filtering and multi-field document indexing (`issuing_organization`, `document_name`, `heading`, `text`).
3. **Hybrid Fusion & Clinical Safety Gating:**
   - Reciprocal Rank Fusion ($k=60$) combining dense semantic and sparse BM25 scores with equal weights ($0.5 / 0.5$).
   - **Guideline Source Affinity:** Boosts chunks from requested issuing organizations ($1.45\times$) when queries explicitly name ICMR, NICE, WHO, or MoHFW.
   - **Patient-Aware Applicability Scoring:** Automatically flags `"matches"`, `"unknown"`, `"conflicts"` against structured patient context. Penalizes pregnancy contraindications (ACEi, ARB, thiazides demoted $0.1\times$) and boosts elderly targets $\ge 80$ ($1.25\times$).
   - **Out-of-Scope Domain Gating:** 100% rejection of out-of-scope clinical queries (pediatric asthma, appendicitis, cancer chemotherapy, rheumatoid arthritis, childhood vaccines, hip arthroplasty) with zero false-positive retrievals.
   - **Cross-Guideline Disagreement Detection:** Flags divergent blood pressure targets and monotherapy vs dual combination strategies across issuing organizations.
4. **Gold Retrieval Benchmark Evaluation:**
   - Created authoritative gold benchmark (`data/gold/retrieval_gold_set.json`) with 42 clinical queries across all required scenario categories: BP thresholds (6), first-line drugs (6), combination therapy (4), target organ damage (4), glycemic targets (6), pregnancy (5), resistant hypertension (5), out-of-scope (6).
   - Generated full benchmark report in `data/reports/retrieval_evaluation_report.md`.

### B. Benchmark Scores vs Acceptance Targets:

| Metric | Acceptance Target | Benchmark Score | Status | Evidence |
|:---|:---|:---|:---|:---|
| **Precision@5** | $\ge 0.80$ | **0.8611** | **PASS** | Mean precision over 36 clinical in-scope queries |
| **Recall@5** | $\ge 0.75$ | **0.8307** | **PASS** | Mean recall over 36 clinical in-scope queries |
| **MRR (Mean Reciprocal Rank)** | $\ge 0.85$ | **0.9583** | **PASS** | Reciprocal rank of first relevant hit |
| **NDCG@5** | $\ge 0.80$ | **0.8672** | **PASS** | Normalized discounted cumulative gain |
| **Out-of-Scope Rejection Rate** | $100\%$ | **100.0\%** | **PASS** | 0 false-positive retrievals on 6 out-of-scope queries |

### C. Automated Verifications & Tests:
- `pytest -q guideline_chatbot/tests/`: **91 passed in 24.27s** (Phase 0: 6, Phase 1: 73, Phase 2: 12)
- `ruff check guideline_chatbot`: **All checks passed!**
- `ruff format --check guideline_chatbot`: **39 files already formatted.**
- `mypy guideline_chatbot --ignore-missing-imports`: **Success: no issues found in 26 source files.**

---

## 4. Stage 3 (Phase 3) Detailed Execution & Evidence

### A. Key Accomplishments:
1. **Multi-Turn Patient State & Contradiction Tracking (`chatbot/patient_state.py`):**
   - Tracks demographics (age, sex, pregnancy, lactation), vitals (SBP, DBP, ABPM), comorbidities (hypertension, type 2 diabetes, CKD, heart failure, CVD), medications (metformin, amlodipine, ramipril, telmisartan, etc.), and allergies (penicillin, sulfa, aspirin, ACEi).
   - Detects and flags clinical contradictions into structured `DisputedFact` objects:
     - Blood pressure contradictions (normotensive claim vs elevated reading, or vice versa).
     - Comorbidity contradictions (asserting vs denying type 2 diabetes).
     - Medication and allergy contradictions (claiming "no meds/allergies" then listing active drugs/allergens).
     - Demographic discrepancies (e.g. age shift >= 5 years).
   - Preserves state history across turns for longitudinal coherence audits.
2. **Provider-Agnostic LLM Interface & Deterministic Mock (`chatbot/llm_client.py`):**
   - `LLMClient` abstract interface supporting `generate(prompt, system_prompt)`.
   - `MockLLMClient`: 100% deterministic offline mock implementing clinical decision support rules, out-of-scope abstention notices, conflict clarification prompts, and pushback rationale without requiring API keys or network access.
   - `OllamaLLMClient`: Native local open-weight model integration via Ollama REST API.
   - `OpenAICompatibleLLMClient`: Native HTTP integration for OpenAI-compatible completion endpoints via environment variables (`LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`).
   - Factory function `get_llm_client()` defaulting safely to `MockLLMClient`.
3. **Citation Extraction & Grounding Verification (`chatbot/citation_validator.py`):**
   - Extracts bracketed citations (`[Document Name, p. X, §Section, Year]` or `[doc_id, p. X]`).
   - Verifies each cited claim against retrieved chunk metadata (document title, document ID, issuing organization, and page range).
   - Discriminates between real citations and non-citation markdown tokens (e.g. `[IMAGE]`, `[TABLE]`, `[2019]`).
   - Returns structured `CitationValidationResult(valid, total_citations, validated_citations, unverified_citations, unsupported_claims_flagged)`.
4. **Structured Clinical Response Generator (`chatbot/generator.py`):**
   - Enforces a 6-part clinical response schema:
     1. `### Guideline Recommendation(s)` with inline citations `[Document Name, p. X, §Section, Year]`.
     2. `### Patient Applicability & Context Analysis` (evaluating age, BP stage, diabetes, microalbuminuria, pregnancy).
     3. `### Missing Patient Information & Recommended Workup` (identifying missing ABPM, HbA1c, eGFR, urine ACR).
     4. `### Cross-Guideline Consensus & Divergence` (detailing divergent thresholds or monotherapy vs dual FDC strategies).
     5. `### General Clinical Rationale` (visibly labeled: *General Clinical Rationale — Not a Formal Guideline Recommendation*).
     6. `### Research Prototype Disclaimer` ("*Research Prototype Disclaimer: For evaluation and research purposes only...*").
   - **Contradiction Clarification Gate:** Automatically pauses recommendations and requests clarification if contradictory patient facts are detected.
   - **Out-of-Scope Domain Abstention:** Deterministically abstains with safe guidance to consult specialists on non-domain queries.
   - **Evidence-Based Pushback Resilience:** Detects user/patient reluctance or pushback against medication and firmly restates guideline evidence on cardiovascular morbidity risk without wavering.
5. **Single Entry Point Chatbot Orchestrator (`chatbot/orchestrator.py`):**
   - Single entry point: `orchestrator.handle_turn(session_id, user_message) -> TurnResult`.
   - Manages session lifecycle (`get_or_create_session`, `clear_session`, `get_session_state`).
   - Coordinates: User Message -> PatientStateManager -> HybridRetriever -> ClinicalResponseGenerator -> CitationValidator -> TurnResult.
6. **Interactive Terminal CLI REPL (`integration/cli.py`):**
   - Multi-turn command-line interface with interactive commands:
     - `/state`: Displays active patient state summary.
     - `/conflicts`: Displays any recorded clinical contradictions.
     - `/clear`: Clears session history and patient state.
     - `/help`: Displays command usage.
     - `/quit`: Terminates REPL.
   - Formatted markdown output with citation verification banners and contradiction alerts.
7. **5 Scripted Demo Conversations (`evaluation/demo_conversations/`):**
   - Generated both `.json` and `.md` transcripts for 5 required scenarios:
     - `scenario1_normal_htn`: 3 turns, Stage 1 HTN initial pharmacotherapy & targets (NICE/WHO), baseline workup.
     - `scenario2_gradual_disclosure`: 3 turns, gradual reveal of T2DM (HbA1c 8.2%) and microalbuminuria (urine ACR 4.2 mg/mmol), triggering prompt drug reassessment (ACEi/ARB).
     - `scenario3_conflicting_statement`: 3 turns, Turn 1 normal BP assertion vs Turn 2 168/104 mmHg, triggering `action_type: clarify` with contradiction detection and subsequent Stage 2 guidance.
     - `scenario4_patient_pushback`: 3 turns, patient refuses medication and demands lifestyle alone; chatbot defends guideline treatment rationale (`action_type: pushback_reaffirm`).
     - `scenario5_out_of_scope`: 2 turns, pediatric asthma prednisolone and inhaler inquiries; chatbot safely abstains with 100% precision (`action_type: abstain`, `is_abstention: true`).
8. **Phase 3 Test Suite (`tests/test_phase3.py`):**
   - 18 unit and integration tests covering all Phase 3 capabilities.

### B. Automated Verifications & Tests (Complete Project):
- `pytest -q`: **109 passed in 14.76s**
  - Phase 0 Tests (`test_phase0.py`): 6 passed
  - Phase 1b Tests (`test_phase1.py`): 73 passed
  - Phase 2 Tests (`test_phase2.py`): 12 passed
  - Phase 3 Tests (`test_phase3.py`): 18 passed
- `ruff check guideline_chatbot`: **All checks passed!**
- `ruff format --check guideline_chatbot`: **52 files already formatted.**
- `mypy guideline_chatbot --ignore-missing-imports`: **Success: no issues found in 34 source files.**

---

## 5. Decision Log & Deviations

1. **Enriched Embedded Chunk Representations:** Rather than embedding raw body text alone, prepended issuing organization and section heading (`[{c.issuing_organization}] {c.heading}\n{c.text}`). This dramatically improved dense retrieval alignment for queries referencing specific guidelines or clinical sections without distorting underlying chunk body text.
2. **Guideline Source Affinity Multiplier:** Implemented a targeted $1.45\times$ rank multiplier for chunks matching the issuing organization when the query explicitly names that source (e.g. "in ICMR STW" or "in NICE NG136"). Cross-guideline queries without specified organizations remain completely neutral and balanced.
3. **Multi-Turn Query Contextualization for Follow-ups:** In multi-turn dialogues where users ask follow-up questions without repeating the diagnosis (e.g. "What baseline monitoring workup should be scheduled?"), contextualized the retrieval query with established patient conditions from `PatientState` (`hypertension`, `type_2_diabetes`). This prevents false out-of-scope rejections on legitimate clinical follow-up turns while preserving 100% rejection on genuinely out-of-scope non-domain queries.
4. **Non-Citation Token Discrimination:** Enhanced `CitationValidator` to explicitly exclude markdown visual/layout tokens (e.g., `[IMAGE]`, `[TABLE]`, `[FIGURE]`) that PyMuPDF extracted from image captions, avoiding false citation validation failures on valid chunk text.
5. **Name Shadowing Prevention in Dataclasses:** Switched from `from dataclasses import field` to `dataclasses.field` in classes defining a clinical attribute named `field` (e.g., `DisputedFact.field: str`), ensuring total typing compatibility with Mypy and Python's scoping rules.
6. **Vector Cache Security:** Added `guideline_chatbot/data/cache/` to `.gitignore` to prevent committing SQLite vector caches while preserving deterministic rebuild capability.
7. **Flowchart Status:** Flowchart nodes continue to be explicitly held out (`needs_review: true`, `indexed_for_retrieval: false`) per standing user instructions.

---

*(All three overnight stages — Stage 1, Stage 2, and Stage 3 — are now fully complete and ready for user morning review.)*
