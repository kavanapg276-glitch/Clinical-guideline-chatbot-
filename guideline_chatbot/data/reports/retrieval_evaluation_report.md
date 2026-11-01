# Retrieval Evaluation Report: Phase 2 Hybrid Retrieval Benchmark

> [!IMPORTANT]
> **Development Set Disclosure:** The gold query benchmark is a developmental set, not independent evidence. Ground-truth expected chunks were derived from guideline review and system development queries, and the retriever was tuned against this set. For independent evaluation, refer to the un-tuned human test set in `retrieval_test_set_human.json` (evaluated via `evaluate_human_test_set.py`).

**Benchmark Dataset:** `guideline_chatbot\data\gold\retrieval_gold_set.json`  
**Total Benchmark Queries:** 54 (42 in-scope, 12 out-of-scope)  
**Evaluation Rank Cutoff (Top-K):** 5  
**Dense Retriever:** `sentence-transformers/all-MiniLM-L6-v2` (384-d normalized, ChromaDB)  
**Sparse Retriever:** BM25Okapi with clinical tokenization  
**Fusion Method:** Reciprocal Rank Fusion (RRF k=60, equal 0.5 weights) with metadata-driven patient applicability  

## 1. Comparative Performance: Original 42-Query Set vs. Expanded 54-Query Set

| Metric | Definition | Original 42-Query Set (36 in-scope, 6 OOS) | Expanded 54-Query Set (42 in-scope, 12 OOS) |
| :--- | :--- | :--- | :--- |
| **Standard Precision@5** | Relevant chunks retrieved / 5 | **0.2611** | **0.2524** |
| **Bounded Precision@5** | Relevant chunks retrieved / min(5, \|expected\|) | **0.4250** | **0.4714** |
| **Recall@5** | Relevant chunks retrieved / \|expected\| | **0.4121** | **0.4604** |
| **MRR (Mean Reciprocal Rank)** | Reciprocal rank of 1st relevant chunk | **0.5093** | **0.5278** |
| **NDCG@5** | Normalized discounted cumulative gain | **0.3830** | **0.4189** |
| **Out-of-Scope Rejection Rate** | Correctly rejected / total out-of-scope | **100.0\%** (0 FP / 6 OOS) | **50.0\%** (30 FP / 12 OOS) |

## 2. Performance by Clinical Category (Expanded Set)

| Category | Queries | Standard P@5 | Bounded P@5 | Recall@5 | MRR | NDCG@5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `bp_thresholds` | 7 | 0.2286 | 0.4238 | 0.3886 | 0.4762 | 0.4014 |
| `combination_therapy` | 4 | 0.4000 | 0.5208 | 0.5208 | 0.6250 | 0.5014 |
| `contraindications` | 1 | 0.2000 | 0.5000 | 0.5000 | 0.5000 | 0.3869 |
| `diagnostic_criteria` | 1 | 0.2000 | 1.0000 | 1.0000 | 0.3333 | 0.5000 |
| `drug_selection` | 1 | 0.4000 | 1.0000 | 1.0000 | 1.0000 | 0.9197 |
| `first_line_drugs` | 6 | 0.2333 | 0.2667 | 0.2667 | 0.5000 | 0.3104 |
| `glycemic_targets` | 6 | 0.2333 | 0.4444 | 0.4444 | 0.5556 | 0.4129 |
| `monitoring` | 1 | 0.2000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| `pregnancy` | 5 | 0.2400 | 0.6467 | 0.6333 | 0.5333 | 0.4573 |
| `resistant_htn` | 5 | 0.3600 | 0.4500 | 0.4200 | 0.7000 | 0.4634 |
| `screening` | 1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `target_organ_damage` | 4 | 0.1500 | 0.3750 | 0.3750 | 0.2500 | 0.2571 |

## 3. Detailed Query-by-Query Results (All 54 Queries)

| ID | Category | Std P@5 | Bnd P@5 | R@5 | MRR | NDCG@5 | Retrieved Chunks | Expected Chunks | Disagreements Detected |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gold_01` | `bp_thresholds` | 0.20 | 0.20 | 0.12 | 0.33 | 0.17 | nice_htn_001_c0046, nice_htn_001_c0084, mohfw_htn_001_c0038, nice_htn_001_c0047, mohfw_htn_001_c0175 | nice_htn_001_c0048, who_htn_001_c0052, who_htn_001_c0019, icmr_htn_001_c0006, mohfw_htn_002_c0048, mohfw_htn_001_c0038, nice_htn_001_c0087, nice_htn_001_c0049 | Blood Pressure Target |
| `gold_02` | `bp_thresholds` | 0.60 | 0.60 | 0.43 | 1.00 | 0.72 | mohfw_htn_001_c0080, mohfw_htn_002_c0086, mohfw_htn_001_c0230, mohfw_htn_001_c0229, nice_htn_001_c0084 | nice_htn_001_c0049, nice_htn_001_c0087, mohfw_htn_001_c0231, mohfw_htn_002_c0086, mohfw_htn_001_c0080, icmr_htn_001_c0006, mohfw_htn_001_c0230 | Blood Pressure Target |
| `gold_03` | `bp_thresholds` | 0.40 | 0.67 | 0.67 | 0.50 | 0.53 | icmr_htn_001_c0007, mohfw_htn_002_c0065, mohfw_htn_001_c0062, mohfw_htn_002_c0037, mohfw_htn_001_c0208 | mohfw_htn_001_c0062, mohfw_htn_001_c0209, mohfw_htn_002_c0065 | None |
| `gold_04` | `bp_thresholds` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | icmr_htn_001_c0007, icmr_t2dm_001_c0008, icmr_t2dm_001_c0004, icmr_htn_001_c0009, icmr_htn_001_c0008 | icmr_htn_001_c0006, icmr_t2dm_001_c0007 | Blood Pressure Target in Diabetes (Within-Source ICMR Disagreement) |
| `gold_05` | `bp_thresholds` | 0.20 | 0.50 | 0.50 | 0.50 | 0.39 | nice_htn_001_c0100, nice_htn_001_c0099, nice_htn_001_c0040, nice_htn_001_c0046, nice_htn_001_c0021 | nice_htn_001_c0048, nice_htn_001_c0099 | None |
| `gold_06` | `bp_thresholds` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0018, nice_htn_001_c0044, nice_htn_001_c0014, nice_htn_001_c0016, nice_htn_001_c0013 | nice_htn_001_c0019, nice_htn_001_c0046 | None |
| `gold_07` | `first_line_drugs` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0068, nice_htn_001_c0055, nice_htn_001_c0060, nice_htn_001_c0093, nice_htn_001_c0094 | nice_htn_001_c0058, nice_htn_001_c0061, nice_htn_001_c0071, nice_htn_001_c0037 | None |
| `gold_08` | `first_line_drugs` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0055, nice_htn_001_c0039, nice_htn_001_c0038, nice_htn_001_c0036, nice_htn_001_c0068 | nice_htn_001_c0058, nice_htn_001_c0061, nice_htn_001_c0040, nice_htn_001_c0037 | None |
| `gold_09` | `first_line_drugs` | 0.60 | 0.75 | 0.75 | 1.00 | 0.79 | who_htn_001_c0017, who_htn_001_c0044, who_htn_001_c0048, icmr_htn_001_c0011, who_htn_001_c0018 | who_htn_001_c0017, who_htn_001_c0044, who_htn_001_c0045, who_htn_001_c0018 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_10` | `first_line_drugs` | 0.60 | 0.60 | 0.60 | 1.00 | 0.68 | mohfw_htn_001_c0062, mohfw_htn_002_c0065, mohfw_htn_001_c0208, mohfw_htn_002_c0029, mohfw_htn_002_c0044 | mohfw_htn_001_c0062, mohfw_htn_001_c0209, mohfw_htn_002_c0039, mohfw_htn_002_c0065, mohfw_htn_002_c0044 | None |
| `gold_11` | `first_line_drugs` | 0.20 | 0.25 | 0.25 | 1.00 | 0.39 | icmr_htn_001_c0011, icmr_htn_001_c0006, icmr_htn_001_c0013, who_htn_001_c0017, who_htn_001_c0044 | icmr_htn_001_c0010, icmr_htn_001_c0011, icmr_htn_001_c0012, icmr_htn_001_c0005 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_12` | `first_line_drugs` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | icmr_htn_001_c0011, icmr_htn_001_c0013, mohfw_htn_002_c0006, icmr_t2dm_001_c0008, mohfw_htn_001_c0183 | icmr_htn_001_c0010, icmr_htn_001_c0012 | None |
| `gold_13` | `combination_therapy` | 0.60 | 0.75 | 0.75 | 1.00 | 0.71 | icmr_htn_001_c0011, icmr_t2dm_001_c0003, icmr_t2dm_001_c0009, who_htn_001_c0049, who_htn_001_c0050 | icmr_htn_001_c0010, icmr_htn_001_c0011, who_htn_001_c0049, who_htn_001_c0050 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_14` | `combination_therapy` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0060, nice_htn_001_c0066, nice_htn_001_c0071, nice_htn_001_c0068, nice_htn_001_c0070 | nice_htn_001_c0063, icmr_htn_001_c0010, mohfw_htn_002_c0056, mohfw_htn_001_c0058, nice_htn_001_c0069 | None |
| `gold_15` | `combination_therapy` | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 | who_htn_001_c0048, who_htn_001_c0018, who_htn_001_c0050, who_htn_001_c0049, icmr_htn_001_c0011 | who_htn_001_c0018, who_htn_001_c0048, who_htn_001_c0049, who_htn_001_c0050 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_16` | `combination_therapy` | 0.20 | 0.33 | 0.33 | 0.50 | 0.30 | icmr_htn_001_c0013, icmr_htn_001_c0011, nice_t2dm_001_c0117, mohfw_htn_001_c0218, mohfw_htn_002_c0075 | icmr_htn_001_c0011, icmr_htn_001_c0010, icmr_htn_001_c0012 | None |
| `gold_17` | `target_organ_damage` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0019, nice_htn_001_c0015, nice_htn_001_c0079, nice_htn_001_c0113, nice_htn_001_c0023 | nice_htn_001_c0020, nice_htn_001_c0028, nice_htn_001_c0016 | None |
| `gold_18` | `target_organ_damage` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | icmr_htn_001_c0009, icmr_htn_001_c0003, icmr_t2dm_001_c0011, icmr_htn_001_c0005, icmr_htn_001_c0010 | icmr_htn_001_c0008 | None |
| `gold_19` | `target_organ_damage` | 0.20 | 1.00 | 1.00 | 0.50 | 0.63 | icmr_htn_001_c0010, icmr_htn_001_c0009, icmr_htn_001_c0005, mohfw_htn_001_c0014, mohfw_htn_001_c0234 | icmr_htn_001_c0009 | None |
| `gold_20` | `target_organ_damage` | 0.40 | 0.50 | 0.50 | 0.50 | 0.40 | icmr_htn_001_c0010, mohfw_htn_001_c0090, mohfw_htn_001_c0240, mohfw_htn_001_c0277, mohfw_htn_001_c0245 | icmr_htn_001_c0009, mohfw_htn_001_c0245, mohfw_htn_001_c0241, mohfw_htn_001_c0090 | None |
| `gold_21` | `glycemic_targets` | 0.40 | 0.50 | 0.50 | 1.00 | 0.64 | icmr_t2dm_001_c0005, icmr_t2dm_001_c0008, icmr_t2dm_001_c0006, icmr_t2dm_001_c0010, icmr_t2dm_001_c0011 | icmr_t2dm_001_c0007, icmr_t2dm_001_c0008, icmr_t2dm_001_c0004, icmr_t2dm_001_c0005 | None |
| `gold_22` | `glycemic_targets` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_t2dm_001_c0028, nice_t2dm_001_c0031, nice_t2dm_001_c0036, nice_t2dm_001_c0034, nice_t2dm_001_c0033 | who_t2dm_001_c0016, who_t2dm_001_c0012, who_t2dm_001_c0019, nice_t2dm_001_c0029, nice_t2dm_001_c0032 | None |
| `gold_23` | `glycemic_targets` | 0.40 | 0.50 | 0.50 | 1.00 | 0.64 | mohfw_t2dm_001_c0020, mohfw_t2dm_001_c0010, mohfw_htn_002_c0122, mohfw_htn_001_c0270, mohfw_htn_001_c0266 | mohfw_t2dm_001_c0015, mohfw_t2dm_001_c0020, mohfw_htn_002_c0133, mohfw_t2dm_001_c0010 | None |
| `gold_24` | `glycemic_targets` | 0.20 | 1.00 | 1.00 | 0.33 | 0.50 | icmr_t2dm_001_c0009, icmr_t2dm_001_c0006, icmr_t2dm_001_c0008, icmr_t2dm_001_c0011, nice_t2dm_001_c0028 | icmr_t2dm_001_c0008 | None |
| `gold_25` | `glycemic_targets` | 0.40 | 0.67 | 0.67 | 1.00 | 0.70 | icmr_t2dm_001_c0010, icmr_t2dm_001_c0011, icmr_t2dm_001_c0009, nice_t2dm_001_c0179, nice_t2dm_001_c0180 | icmr_t2dm_001_c0008, icmr_t2dm_001_c0009, icmr_t2dm_001_c0010 | None |
| `gold_26` | `glycemic_targets` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_t2dm_001_c0111, nice_t2dm_001_c0077, nice_t2dm_001_c0103, nice_t2dm_001_c0092, nice_t2dm_001_c0118 | nice_t2dm_001_c0072, nice_t2dm_001_c0068, nice_t2dm_001_c0099 | None |
| `gold_27` | `pregnancy` | 0.40 | 0.40 | 0.33 | 1.00 | 0.55 | who_htn_001_c0066, who_htn_001_c0075, icmr_htn_001_c0013, nice_htn_001_c0059, nice_htn_001_c0055 | icmr_htn_001_c0012, nice_htn_001_c0057, nice_htn_001_c0058, who_htn_001_c0066, who_htn_001_c0075, nice_htn_001_c0054 | None |
| `gold_28` | `pregnancy` | 0.20 | 1.00 | 1.00 | 0.50 | 0.63 | icmr_t2dm_001_c0007, icmr_t2dm_001_c0006, icmr_t2dm_001_c0005, icmr_t2dm_001_c0011, icmr_htn_001_c0009 | icmr_t2dm_001_c0006 | None |
| `gold_29` | `pregnancy` | 0.20 | 1.00 | 1.00 | 0.33 | 0.50 | icmr_t2dm_001_c0007, icmr_t2dm_001_c0005, icmr_t2dm_001_c0006, icmr_t2dm_001_c0011, icmr_t2dm_001_c0008 | icmr_t2dm_001_c0006 | None |
| `gold_30` | `pregnancy` | 0.20 | 0.33 | 0.33 | 0.50 | 0.30 | nice_htn_001_c0073, nice_htn_001_c0054, nice_htn_001_c0051, nice_htn_001_c0055, nice_htn_001_c0059 | nice_htn_001_c0057, nice_htn_001_c0058, nice_htn_001_c0054 | None |
| `gold_31` | `pregnancy` | 0.20 | 0.50 | 0.50 | 0.33 | 0.31 | icmr_htn_001_c0013, icmr_htn_001_c0011, who_htn_001_c0066, mohfw_htn_002_c0047, nice_htn_001_c0054 | icmr_htn_001_c0012, who_htn_001_c0066 | None |
| `gold_32` | `resistant_htn` | 0.40 | 0.40 | 0.25 | 1.00 | 0.49 | nice_htn_001_c0077, nice_htn_001_c0071, nice_htn_001_c0069, nice_htn_001_c0076, nice_htn_001_c0070 | nice_htn_001_c0074, nice_htn_001_c0076, nice_htn_001_c0077, nice_htn_001_c0078, nice_htn_001_c0080, nice_htn_001_c0105, nice_htn_001_c0079, nice_htn_001_c0072 | None |
| `gold_33` | `resistant_htn` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0075, nice_htn_001_c0071, mohfw_htn_001_c0270, nice_htn_001_c0074, mohfw_htn_001_c0191 | nice_htn_001_c0078, nice_htn_001_c0077 | None |
| `gold_34` | `resistant_htn` | 0.60 | 0.75 | 0.75 | 1.00 | 0.80 | icmr_htn_001_c0012, icmr_htn_001_c0011, icmr_htn_001_c0006, icmr_htn_001_c0010, icmr_htn_001_c0013 | icmr_htn_001_c0011, icmr_htn_001_c0012, nice_htn_001_c0077, icmr_htn_001_c0010 | None |
| `gold_35` | `resistant_htn` | 0.60 | 0.60 | 0.60 | 1.00 | 0.64 | mohfw_htn_002_c0121, mohfw_htn_001_c0001, mohfw_htn_001_c0060, mohfw_htn_001_c0265, mohfw_htn_002_c0058 | mohfw_htn_001_c0060, mohfw_htn_001_c0201, mohfw_htn_002_c0058, mohfw_htn_002_c0121, mohfw_htn_001_c0266 | None |
| `gold_36` | `resistant_htn` | 0.20 | 0.50 | 0.50 | 0.50 | 0.39 | icmr_htn_001_c0013, icmr_htn_001_c0012, nice_htn_001_c0074, mohfw_htn_002_c0047, nice_htn_001_c0110 | icmr_htn_001_c0012, icmr_htn_001_c0011 | None |
| `gold_37` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_38` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_39` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_40` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_41` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_42` | `out_of_scope` | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | *(none - gated)* | *(out of scope)* | None |
| `gold_43` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | who_htn_001_c0023, who_htn_001_c0033, mohfw_htn_002_c0058, who_htn_001_c0013, mohfw_htn_001_c0051 | *(out of scope)* | None |
| `gold_44` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | who_htn_001_c0066, who_htn_001_c0065, mohfw_htn_001_c0090, who_htn_001_c0048, mohfw_htn_001_c0072 | *(out of scope)* | None |
| `gold_45` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | mohfw_htn_002_c0103, mohfw_htn_001_c0067, mohfw_htn_002_c0070, mohfw_htn_001_c0097, mohfw_htn_001_c0247 | *(out of scope)* | None |
| `gold_46` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_t2dm_001_c0188, nice_t2dm_001_c0187, mohfw_t2dm_001_c0017, nice_t2dm_001_c0175, nice_t2dm_001_c0057 | *(out of scope)* | None |
| `gold_47` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | nice_htn_001_c0075, nice_htn_001_c0072, nice_htn_001_c0003, icmr_htn_001_c0011, nice_t2dm_001_c0206 | *(out of scope)* | None |
| `gold_48` | `out_of_scope` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | mohfw_htn_002_c0141, mohfw_htn_001_c0234, mohfw_htn_002_c0090, mohfw_htn_001_c0084, mohfw_htn_002_c0123 | *(out of scope)* | None |
| `gold_49` | `bp_thresholds` | 0.20 | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0005, icmr_htn_001_c0003, icmr_htn_001_c0009, icmr_htn_001_c0007, icmr_htn_001_c0010 | icmr_htn_001_c0005 | None |
| `gold_50` | `screening` | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | icmr_htn_001_c0007, icmr_htn_001_c0003, icmr_htn_001_c0005, icmr_htn_001_c0009, icmr_htn_001_c0004 | icmr_t2dm_001_c0007 | None |
| `gold_51` | `drug_selection` | 0.40 | 1.00 | 1.00 | 1.00 | 0.92 | who_htn_001_c0048, who_htn_001_c0050, icmr_htn_001_c0011, who_htn_001_c0018, who_htn_001_c0049 | icmr_htn_001_c0011, who_htn_001_c0048 | Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC) |
| `gold_52` | `monitoring` | 0.20 | 1.00 | 1.00 | 1.00 | 1.00 | icmr_htn_001_c0007, icmr_htn_001_c0003, icmr_htn_001_c0005, icmr_htn_001_c0009, mohfw_htn_002_c0085 | icmr_htn_001_c0007 | None |
| `gold_53` | `contraindications` | 0.20 | 0.50 | 0.50 | 0.50 | 0.39 | nice_htn_001_c0066, icmr_htn_001_c0011, nice_htn_001_c0071, nice_htn_001_c0060, nice_htn_001_c0055 | icmr_htn_001_c0011, mohfw_htn_001_c0202 | None |
| `gold_54` | `diagnostic_criteria` | 0.20 | 1.00 | 1.00 | 0.33 | 0.50 | icmr_t2dm_001_c0005, icmr_t2dm_001_c0010, icmr_t2dm_001_c0006, icmr_t2dm_001_c0011, icmr_htn_001_c0009 | icmr_t2dm_001_c0006 | None |
