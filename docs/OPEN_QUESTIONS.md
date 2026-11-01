# Open Questions & Design Decisions

*Maintained per Standing Rule 10 & 11. Documents open design decisions and any manual actions.*

---

## Current Status (Phase 0 Complete)

**All 10 target guideline documents were successfully downloaded with 100% valid PDF verification.** There are no blocking download failures.

### Logged Design Decisions

1. **ICMR Scope Decision:**
   - *Scope Chosen:* Only the adult hypertension workflow (`1778941063_hypertensioninadults_final.pdf`) and adult Type 2 Diabetes Mellitus workflow (`1726567245_diabetes_mellitus_type_2.pdf`) were acquired, strictly honoring the Master Prompt scope for Hypertension and Type 2 Diabetes.
   - *Note:* ICMR also provides STWs for Type 1 Diabetes, Diabetic Ketoacidosis (DKA), and Diabetic Foot. These were noted in reconnaissance but omitted to avoid out-of-scope noise in retrieval.

2. **MoHFW Scope Decision:**
   - Acquired both the standalone modular STGs (Hypertension Full Document 144p and Quick Reference Guide 54p) and the parent specialty volumes (Cardiovascular Diseases Part 1 40p and Endocrinology 49p).
   - In Phase 1 chunking, the multi-condition volumes will have their relevant page ranges explicitly bounded per `source_inventory.csv`.

3. **Embedding Model:**
   - `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions) downloaded, verified, and cached locally. Tested with inference.

4. **Strictly Evidence-Bound Clinical Response Generator (Stage A2):**
   - *Design Goal:* Eliminate all ungrounded model hallucinations, hardcoded clinical assertions, and default drug statements from conversational responses.
   - *Implementation in `guideline_chatbot/chatbot/generator.py`:*
     - Removed all static clinical assertions (e.g., hardcoded metformin recommendations, dual therapy defaults, ACEi/ARB renal protection paragraphs).
     - Every recommendation statement is constructed directly from retrieved chunk texts, tagged with an inline citation `[^N]` mapping to retrieved hit `N`.
     - Standardized citation metadata to use verified publication years (`DOC_YEARS` mapping: MoHFW 2016, WHO HTN 2021, WHO HEARTS 2020, NICE NG136 2019/2022, NICE NG28 2015/2022, ICMR HTN 2026, ICMR T2DM 2022) instead of the vague placeholder `"current"`.
     - When retrieval yields no in-scope hits, the generator explicitly emits: *"No guideline evidence was retrieved for this point. Please verify primary guideline documentation."*
     - Derived "Missing Patient Information & Recommended Workup" dynamically via `_derive_missing_info()` by cross-referencing retrieved chunks' `applicability_conditions` and `exceptions` against unknown/unrecorded patient state attributes (e.g. unmeasured ABPM, eGFR, potassium, urine ACR, pregnancy status in reproductive-age females), removing hardcoded disease-specific checklists.
     - Suppressed introductory conversational boilerplate across multi-turn interactions (`turn_count > 1`).
