# Clinical Entity Tagging & Provenance Rules Specification

**Document:** `docs/TAGGING_RULES.md`  
**Purpose:** Defines deterministic rules for metadata extraction, clinical population tagging, pharmacological class classification, and condition scoping in the ClinCoherence RAG pipeline.  
**Audience:** ClinCoherence Ingestion Pipeline, Verifier Layer, and Human Auditors  

---

## 1. Core Principle: Applicability vs. Mere Mention

> [!IMPORTANT]
> **A population tag denotes that the clinical recommendation or guidance directly APPLIES TO that subpopulation.**  
> Simply mentioning a word, listing a laboratory test, or naming a drug side effect does NOT justify tagging a clinical population.

### Audited Failure Modes & Resolution:
1. **Diagnostic Screening Tests:**  
   *Negative Example:* NICE NG136 Recommendation 1.3.3 instructs clinicians: *"For all people with hypertension offer to: test for the presence of protein in the urine... measure HbA1c..."*  
   *Rule:* Because this recommendation applies to **all adults with hypertension** to screen for potential organ damage, it must NOT be tagged with `type_2_diabetes`.
2. **Negation and Exclusions:**  
   *Negative Example:* NICE NG136 Recommendation 1.2.12 states: *"Measure blood pressure at least annually in an adult with type 2 diabetes without previously diagnosed hypertension or renal disease."*  
   *Rule:* The phrase *"without ... renal disease"* explicitly excludes CKD patients from this specific annual cadence. The pipeline must detect negation patterns (`without`, `excluding`, `in the absence of`, `except`) and **MUST NOT** tag `chronic_kidney_disease`.
3. **Cross-References vs Target Population Applicability:**  
   *Negative Example:* NICE NG136 Recommendation 1.4.20 contains a cross-reference statement: *"See also table 1 for guidance on clinic blood pressure targets for people aged under 80 with type 1 diabetes or severe chronic kidney disease."*  
   *Rule:* Mentioning a population exclusively within an explicit cross-reference ("See also table...", "see the section on...", "see NICE guideline on...") directs clinicians to a separate protocol; it does NOT mean this chunk governs that subpopulation. The pipeline parses all cross-reference clauses into `cross_references: list[str]` and strips them before extracting population tags. Recommendation 1.4.20 therefore carries `population_tags: []` (general adult hypertension under 80), not `type_1_diabetes` or `chronic_kidney_disease`.
4. **Drug Adverse Effect Mentions:**  
   *Negative Example:* MoHFW STG §5.3.2 notes: *"The common side effects of diuretics are metabolic side effects like hypokalemia, hyperglycemia..."*  
   *Rule:* Listing hyperglycemia as a pharmacological side effect of thiazides is not a recommendation for diabetic patients. It must not be tagged with `type_2_diabetes`.

---

## 2. Standardized Clinical Population Tags

The pipeline recognizes the following standardized population tags:

| Tag Identifier | Defining Clinical Criteria | Positive Match Patterns | Mandatory Exclusion / Negation Patterns |
|---|---|---|---|
| `elderly` | Adults aged $\ge 65$ or $\ge 80$, frail, octogenarians | `aged >= 80`, `aged 80 and over`, `over 80`, `elderly`, `frail` | `aged under 80`, `< 80 years`, `younger adults` |
| `type_2_diabetes` | Adults with established Type 2 Diabetes Mellitus | `type 2 diabetes`, `t2dm`, `diabetic patients`, `in people with type 2 diabetes` | `type 1 diabetes`, `without diabetes`, `excluding diabetes`, `screen for diabetes` (general pop) |
| `type_1_diabetes` | Adults or children with Type 1 Diabetes Mellitus | `type 1 diabetes`, `t1dm`, `autoimmune diabetes` | `type 2 diabetes`, `without type 1 diabetes` |
| `chronic_kidney_disease` | Adults with established CKD, eGFR $< 60$, or persistent proteinuria/albuminuria | `chronic kidney disease`, `ckd`, `renal impairment`, `egfr < 60`, `diabetic nephropathy` | `without renal disease`, `normal renal function`, `excluding ckd` |
| `pregnancy` | Pregnant women, gestational diabetes, pre-eclampsia | `pregnant`, `pregnancy`, `gestational`, `pre-eclampsia`, `women planning pregnancy` | `non-pregnant`, `excluding pregnancy` |
| `cardiovascular_disease` | Adults with established ASCVD, CAD, heart failure, stroke, or post-MI | `coronary artery disease`, `cad`, `heart failure`, `previous stroke`, `myocardial infarction`, `ascvd` | `without cvd`, `no history of cvd`, `without cardiovascular disease` |
| `african_caribbean` | Adults of Black African or African-Caribbean family origin | `black african`, `african-caribbean`, `african family origin` | `not of black african`, `excluding african origin` |
| `young_adults` | Adults aged $< 40$ or $< 55$ evaluated for secondary causes | `aged under 40`, `young adults`, `age < 40`, `younger than 55` | `aged >= 80`, `older adults` |

---

## 3. Condition Scoping (`hypertension`, `type_2_diabetes`, `both`)

The field `condition` indicates the therapeutic disease domain to which the chunk applies:
- `hypertension`: Guidance addressing blood pressure measurement, classification, lifestyle modification, and pharmacological management of hypertension (applies generally to adults with hypertension unless explicitly restricted).
- `type_2_diabetes`: Guidance addressing glycemic control, HbA1c targets, lifestyle modification, and glucose-lowering agents in type 2 diabetes (applies generally to adults with diabetes unless explicitly restricted).
- `both`: Applied when guidance specifically governs patients presenting with **both** conditions simultaneously (e.g. blood pressure thresholds/targets in diabetic patients, ACEi/ARB preferential selection in diabetic hypertension, or screening for diabetes in hypertensive patients).

### Multi-Condition Retrieval Semantics:
When a patient has **both** hypertension and type 2 diabetes, clinical decision support requires access to general hypertension recommendations, general diabetes recommendations, and combination-specific guidance. Therefore, the retrieval layer dynamically retrieves across `hypertension`, `type_2_diabetes`, and `both` (e.g. `{"condition": {"$in": ["hypertension", "type_2_diabetes", "both"]}}`). Chunks tagged `both` are also indexed for single-condition queries when relevant.

---

## 4. Applicability Conditions and Exceptions Extraction

The fields `applicability_conditions` and `exceptions` capture conditional clinical logic:

### `applicability_conditions`:
- **Requirement:** Extracted ONLY when explicit conditional clauses define when the recommendation is activated:
  - Clause triggers: `if clinic blood pressure is...`, `when eGFR is...`, `in adults with confirmed...`, `for people aged...`, `where daytime ABPM is...`.
  - If no explicit conditional trigger is present in the text, the field is set to `null`.
- **Prohibited Content:** PICO research questions, systematic review certainty ratings, reference citations, and document titles must never be stored as applicability conditions.

### `exceptions`:
- **Requirement:** Extracted ONLY from explicit contraindication, avoidance, or exclusion statements:
  - Clause triggers: `do not offer...`, `do not prescribe...`, `avoid in...`, `contraindicated in...`, `caution in...`, `except in...`, `unless...`, `discontinue if...`.
  - If no explicit contraindication is present in the text, the field is set to `null`.

---

## 5. Noise Classification & Retrieval Filtering

To ensure high-precision clinical retrieval in Phase 2, chunks are classified into distinct functional types. Non-clinical background sections are preserved in the dataset for traceability but flagged with `indexed_for_retrieval: false`:

| Chunk Type | Clinical Meaning | Indexable for RAG Retrieval? | Examples |
|---|---|---|---|
| `recommendation` | Actionable clinical instruction or target | **YES** (`indexed_for_retrieval: true`) | NICE 1.4.20, WHO Rec 1, ICMR treatment steps |
| `table` | Structured tabular dosing, targets, or classifications | **YES** (`indexed_for_retrieval: true`) | Drug dosing tables, diagnostic cutoff tables |
| `definition` | Disease criteria, BP stages, HbA1c diagnostic cutoffs | **YES** (`indexed_for_retrieval: true`) | Definition of Stage 1 HTN, IFG/IGT criteria |
| `monitoring` | Follow-up schedules, laboratory monitoring intervals | **YES** (`indexed_for_retrieval: true`) | Re-assessment intervals, annual urine ACR checks |
| `rationale` | Evidence summaries, clinical trial justifications | **YES** (`indexed_for_retrieval: true`) | GDG evidence-to-decision rationale, JNC 8 review |
| `other` | Clinical pathophysiology, non-pharm lifestyle advice | **YES** (`indexed_for_retrieval: true`) | Dietary sodium reduction, exercise counselling |
| `reference` | Bibliographies, reference citations, literature lists | **NO** (`indexed_for_retrieval: false`) | Numbered citations, journal publication lists |
| `methods` | Guideline methodology, analytical frameworks, PICOs | **NO** (`indexed_for_retrieval: false`) | GRADE methodology descriptions, PICO questions |
| `front_matter` | Acknowledgements, executive summaries, acronym tables | **NO** (`indexed_for_retrieval: false`) | Document covers, abbreviations, copyright notices |
| `contributors` | Committee rosters, review panel member names | **NO** (`indexed_for_retrieval: false`) | AMRO/EMRO participant rosters, conflict of interest lists |
| `flowchart` | Algorithm diagrams and visual decision flowcharts | **NO** (`indexed_for_retrieval: false`) | Transcribed flowchart trees held pending review |
