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
