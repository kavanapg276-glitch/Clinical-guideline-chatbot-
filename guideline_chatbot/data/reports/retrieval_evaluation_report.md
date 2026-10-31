# Retrieval Evaluation Report: Phase 2 Hybrid Retrieval Benchmark

**Benchmark Dataset:** `guideline_chatbot\data\gold\retrieval_gold_set.json`  
**Total Benchmark Queries:** 42 (36 in-scope, 6 out-of-scope)  
**Evaluation Rank Cutoff (Top-K):** 5  
**Dense Retriever:** `sentence-transformers/all-MiniLM-L6-v2` (384-d normalized, ChromaDB)  
**Sparse Retriever:** BM25Okapi with clinical synonym expansion tokenization  
**Fusion Method:** Reciprocal Rank Fusion (RRF k=60, equal 0.5 weights) with patient applicability weighting  

## 1. Overall Performance vs Acceptance Targets

| Metric | Target | Benchmark Score | Status | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Precision@5** | $\ge 0.80$ | **0.8611** | **PASS** | Mean precision over 36 clinical queries |
| **Recall@5** | $\ge 0.75$ | **0.8307** | **PASS** | Mean recall over 36 clinical queries |
| **MRR (Mean Reciprocal Rank)** | $\ge 0.85$ | **0.9583** | **PASS** | First relevant hit reciprocal rank |
| **NDCG@5** | $\ge 0.80$ | **0.8672** | **PASS** | Normalized discounted cumulative gain |
| **Out-of-Scope Rejection Rate** | $100\%$ | **100.0\%** | **PASS** | 0 false positive retrievals out of 6 out-of-scope queries |

## 2. Performance by Clinical Category

| Category | Queries | Precision@5 | Recall@5 | MRR | NDCG@5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `bp_thresholds` | 6 | 0.9667 | 0.8690 | 0.8333 | 0.8754 |
| `combination_therapy` | 4 | 0.7042 | 0.7042 | 1.0000 | 0.7681 |
| `first_line_drugs` | 6 | 0.8417 | 0.8417 | 1.0000 | 0.8867 |
| `glycemic_targets` | 6 | 0.7611 | 0.7611 | 1.0000 | 0.8071 |
| `pregnancy` | 5 | 0.9600 | 0.9333 | 0.9000 | 0.9203 |
| `resistant_htn` | 5 | 0.9100 | 0.8350 | 1.0000 | 0.9067 |
| `target_organ_damage` | 4 | 0.8542 | 0.8542 | 1.0000 | 0.8993 |

## 3. Detailed Query-by-Query Results

| ID | Category | P@5 | R@5 | MRR | NDCG@5 | Retrieved Chunks | Expected Chunks | Disagreements Detected |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gold_01` | `bp_thresholds` | 0.80 | 0.50 | 1.00 | 0.87 | nice_htn_001_c0048, nice_htn_001_c0087, mohfw_htn_001_c0038, nice_htn_001_c0049, nice_htn_001_c0042 | nice_htn_001_c0048, who_htn_001_c0052, who_htn_001_c0019, icmr_htn_001_c0006, mohfw_htn_002_c0048, mohfw_htn_001_c0038, nice_htn_001_c0087, nice_htn_001_c0049 | Blood Pressure Target |
| `gold_02` | `bp_thresholds` | 1.00 | 0.71 | 1.00 | 1.00 | mohfw_htn_001_c0080, mohfw_htn_002_c0086, mohfw_htn_001_c0231, mohfw_htn_001_c0230, nice_htn_001_c0087 | nice_htn_001_c0049, nice_htn_001_c0087, mohfw_htn_001_c0231, mohfw_htn_002_c0086, mohfw_htn_001_c0080, icmr_htn_001_c0006, mohfw_htn_001_c0230 | Blood Pressure Target |
| `gold_03` | `bp_thresholds` | 1.00 | 1.00 | 0.50 | 0.73 | icmr_htn_001_c0006, mohfw_htn_002_c0065, mohfw_htn_001_c0062, mohfw_htn_001_c0209, mohfw_htn_002_c0037 | mohfw_htn_001_c0062, mohfw_htn_001_c0209, mohfw_htn_002_c0065 | None |
| `gold_04` | `bp_thresholds` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0006, icmr_t2dm_001_c0007, icmr_t2dm_001_c0003, icmr_htn_001_c0008, icmr_htn_001_c0003 | icmr_htn_001_c0006, icmr_t2dm_001_c0007 | None |
| `gold_05` | `bp_thresholds` | 1.00 | 1.00 | 0.50 | 0.65 | nice_htn_001_c0109, nice_htn_001_c0099, nice_htn_001_c0042, nice_htn_001_c0048, nice_htn_001_c0022 | nice_htn_001_c0048, nice_htn_001_c0099 | None |
| `gold_06` | `bp_thresholds` | 1.00 | 1.00 | 1.00 | 1.00 | nice_htn_001_c0019, nice_htn_001_c0046, nice_htn_001_c0015, nice_htn_001_c0017, nice_htn_001_c0014 | nice_htn_001_c0019, nice_htn_001_c0046 | None |
| `gold_07` | `first_line_drugs` | 0.75 | 0.75 | 1.00 | 0.80 | nice_htn_001_c0071, nice_htn_001_c0058, nice_htn_001_c0063, nice_htn_001_c0037, nice_htn_001_c0060 | nice_htn_001_c0058, nice_htn_001_c0061, nice_htn_001_c0071, nice_htn_001_c0037 | None |
| `gold_08` | `first_line_drugs` | 1.00 | 1.00 | 1.00 | 0.98 | nice_htn_001_c0058, nice_htn_001_c0040, nice_htn_001_c0037, nice_htn_001_c0053, nice_htn_001_c0061 | nice_htn_001_c0058, nice_htn_001_c0061, nice_htn_001_c0040, nice_htn_001_c0037 | None |
| `gold_09` | `first_line_drugs` | 0.75 | 0.75 | 1.00 | 0.83 | who_htn_001_c0017, who_htn_001_c0044, who_htn_001_c0018, who_htn_001_c0048, icmr_htn_001_c0010 | who_htn_001_c0017, who_htn_001_c0044, who_htn_001_c0045, who_htn_001_c0018 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_10` | `first_line_drugs` | 0.80 | 0.80 | 1.00 | 0.87 | mohfw_htn_001_c0062, mohfw_htn_002_c0065, mohfw_htn_001_c0209, mohfw_htn_002_c0044, mohfw_htn_002_c0029 | mohfw_htn_001_c0062, mohfw_htn_001_c0209, mohfw_htn_002_c0039, mohfw_htn_002_c0065, mohfw_htn_002_c0044 | None |
| `gold_11` | `first_line_drugs` | 0.75 | 0.75 | 1.00 | 0.83 | icmr_htn_001_c0010, icmr_htn_001_c0005, icmr_htn_001_c0012, who_htn_001_c0017, who_htn_001_c0044 | icmr_htn_001_c0010, icmr_htn_001_c0011, icmr_htn_001_c0012, icmr_htn_001_c0005 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_12` | `first_line_drugs` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0010, icmr_htn_001_c0012, mohfw_htn_002_c0006, icmr_t2dm_001_c0007, mohfw_htn_001_c0120 | icmr_htn_001_c0010, icmr_htn_001_c0012 | None |
| `gold_13` | `combination_therapy` | 0.75 | 0.75 | 1.00 | 0.75 | icmr_htn_001_c0010, icmr_t2dm_001_c0008, who_htn_001_c0049, who_htn_001_c0050, nice_htn_001_c0103 | icmr_htn_001_c0010, icmr_htn_001_c0011, who_htn_001_c0049, who_htn_001_c0050 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_14` | `combination_therapy` | 0.40 | 0.40 | 1.00 | 0.55 | nice_htn_001_c0063, nice_htn_001_c0069, nice_htn_001_c0074, nice_htn_001_c0071, nice_htn_001_c0073 | nice_htn_001_c0063, icmr_htn_001_c0010, mohfw_htn_002_c0056, mohfw_htn_001_c0058, nice_htn_001_c0069 | None |
| `gold_15` | `combination_therapy` | 1.00 | 1.00 | 1.00 | 1.00 | who_htn_001_c0048, who_htn_001_c0018, who_htn_001_c0050, who_htn_001_c0049, icmr_htn_001_c0010 | who_htn_001_c0018, who_htn_001_c0048, who_htn_001_c0049, who_htn_001_c0050 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_16` | `combination_therapy` | 0.67 | 0.67 | 1.00 | 0.77 | icmr_htn_001_c0012, icmr_htn_001_c0010, nice_t2dm_001_c0104, mohfw_htn_001_c0219, mohfw_htn_002_c0075 | icmr_htn_001_c0011, icmr_htn_001_c0010, icmr_htn_001_c0012 | None |
| `gold_17` | `target_organ_damage` | 0.67 | 0.67 | 1.00 | 0.77 | nice_htn_001_c0020, nice_htn_001_c0016, nice_htn_001_c0082, nice_htn_001_c0024, nice_htn_001_c0107 | nice_htn_001_c0020, nice_htn_001_c0028, nice_htn_001_c0016 | None |
| `gold_18` | `target_organ_damage` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0008, icmr_htn_001_c0003, icmr_t2dm_001_c0010, icmr_htn_001_c0004, icmr_htn_001_c0009 | icmr_htn_001_c0008 | None |
| `gold_19` | `target_organ_damage` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0009, icmr_htn_001_c0003, icmr_htn_001_c0008, icmr_htn_001_c0004, mohfw_htn_001_c0014 | icmr_htn_001_c0009 | None |
| `gold_20` | `target_organ_damage` | 0.75 | 0.75 | 1.00 | 0.83 | icmr_htn_001_c0009, mohfw_htn_001_c0090, mohfw_htn_001_c0241, mohfw_htn_002_c0144, mohfw_htn_001_c0278 | icmr_htn_001_c0009, mohfw_htn_001_c0245, mohfw_htn_001_c0241, mohfw_htn_001_c0090 | None |
| `gold_21` | `glycemic_targets` | 0.75 | 0.75 | 1.00 | 0.75 | icmr_t2dm_001_c0004, icmr_t2dm_001_c0009, icmr_t2dm_001_c0007, icmr_t2dm_001_c0005, icmr_t2dm_001_c0010 | icmr_t2dm_001_c0007, icmr_t2dm_001_c0008, icmr_t2dm_001_c0004, icmr_t2dm_001_c0005 | None |
| `gold_22` | `glycemic_targets` | 0.40 | 0.40 | 1.00 | 0.55 | nice_t2dm_001_c0029, nice_t2dm_001_c0032, nice_t2dm_001_c0037, nice_t2dm_001_c0035, nice_t2dm_001_c0034 | who_t2dm_001_c0016, who_t2dm_001_c0012, who_t2dm_001_c0019, nice_t2dm_001_c0029, nice_t2dm_001_c0032 | None |
| `gold_23` | `glycemic_targets` | 0.75 | 0.75 | 1.00 | 0.83 | mohfw_t2dm_001_c0020, mohfw_htn_002_c0133, mohfw_t2dm_001_c0010, mohfw_htn_001_c0271, mohfw_htn_002_c0122 | mohfw_t2dm_001_c0015, mohfw_t2dm_001_c0020, mohfw_htn_002_c0133, mohfw_t2dm_001_c0010 | None |
| `gold_24` | `glycemic_targets` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_t2dm_001_c0008, icmr_t2dm_001_c0005, icmr_t2dm_001_c0007, icmr_t2dm_001_c0010, nice_t2dm_001_c0029 | icmr_t2dm_001_c0008 | None |
| `gold_25` | `glycemic_targets` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_t2dm_001_c0009, icmr_t2dm_001_c0010, icmr_t2dm_001_c0008, icmr_t2dm_001_c0005, nice_t2dm_001_c0144 | icmr_t2dm_001_c0008, icmr_t2dm_001_c0009, icmr_t2dm_001_c0010 | None |
| `gold_26` | `glycemic_targets` | 0.67 | 0.67 | 1.00 | 0.70 | nice_t2dm_001_c0099, nice_t2dm_001_c0092, nice_t2dm_001_c0068, nice_t2dm_001_c0108, nice_t2dm_001_c0082 | nice_t2dm_001_c0072, nice_t2dm_001_c0068, nice_t2dm_001_c0099 | None |
| `gold_27` | `pregnancy` | 0.80 | 0.67 | 1.00 | 0.87 | who_htn_001_c0066, who_htn_001_c0075, nice_htn_001_c0054, icmr_htn_001_c0012, mohfw_htn_002_c0132 | icmr_htn_001_c0012, nice_htn_001_c0057, nice_htn_001_c0058, who_htn_001_c0066, who_htn_001_c0075, nice_htn_001_c0054 | None |
| `gold_28` | `pregnancy` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_t2dm_001_c0006, icmr_t2dm_001_c0005, icmr_t2dm_001_c0004, icmr_t2dm_001_c0010, icmr_htn_001_c0008 | icmr_t2dm_001_c0006 | None |
| `gold_29` | `pregnancy` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_t2dm_001_c0006, icmr_t2dm_001_c0004, icmr_t2dm_001_c0005, icmr_t2dm_001_c0010, icmr_t2dm_001_c0007 | icmr_t2dm_001_c0006 | None |
| `gold_30` | `pregnancy` | 1.00 | 1.00 | 0.50 | 0.73 | nice_htn_001_c0076, nice_htn_001_c0057, nice_htn_001_c0054, nice_htn_001_c0058, nice_htn_001_c0062 | nice_htn_001_c0057, nice_htn_001_c0058, nice_htn_001_c0054 | None |
| `gold_31` | `pregnancy` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0012, who_htn_001_c0066, who_htn_001_c0075, mohfw_htn_001_c0190, nice_htn_001_c0057 | icmr_htn_001_c0012, who_htn_001_c0066 | None |
| `gold_32` | `resistant_htn` | 1.00 | 0.62 | 1.00 | 1.00 | nice_htn_001_c0074, nice_htn_001_c0080, nice_htn_001_c0079, nice_htn_001_c0072, nice_htn_001_c0078 | nice_htn_001_c0074, nice_htn_001_c0076, nice_htn_001_c0077, nice_htn_001_c0078, nice_htn_001_c0080, nice_htn_001_c0105, nice_htn_001_c0079, nice_htn_001_c0072 | None |
| `gold_33` | `resistant_htn` | 1.00 | 1.00 | 1.00 | 0.88 | nice_htn_001_c0078, nice_htn_001_c0074, mohfw_htn_001_c0271, nice_htn_001_c0077, mohfw_htn_001_c0192 | nice_htn_001_c0078, nice_htn_001_c0077 | None |
| `gold_34` | `resistant_htn` | 0.75 | 0.75 | 1.00 | 0.79 | icmr_htn_001_c0011, icmr_htn_001_c0010, icmr_htn_001_c0009, icmr_htn_001_c0005, icmr_htn_001_c0012 | icmr_htn_001_c0011, icmr_htn_001_c0012, nice_htn_001_c0077, icmr_htn_001_c0010 | None |
| `gold_35` | `resistant_htn` | 0.80 | 0.80 | 1.00 | 0.87 | mohfw_htn_002_c0121, mohfw_htn_001_c0060, mohfw_htn_001_c0266, mohfw_htn_002_c0058, nice_htn_001_c0074 | mohfw_htn_001_c0060, mohfw_htn_001_c0201, mohfw_htn_002_c0058, mohfw_htn_002_c0121, mohfw_htn_001_c0266 | None |
| `gold_36` | `resistant_htn` | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0012, icmr_htn_001_c0011, nice_htn_001_c0077, nice_htn_001_c0105, mohfw_htn_002_c0047 | icmr_htn_001_c0012, icmr_htn_001_c0011 | None |
| `gold_37` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_38` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_39` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_40` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_41` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_42` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
