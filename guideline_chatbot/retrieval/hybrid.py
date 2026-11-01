"""Hybrid retrieval layer combining dense semantic vector search and sparse BM25 keyword search.

Applies Reciprocal Rank Fusion (RRF), patient-aware applicability re-ranking,
cross-guideline clinical disagreement detection, and out-of-scope abstention gating.
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Any

from guideline_chatbot.retrieval.embeddings import EmbeddingManager
from guideline_chatbot.retrieval.keyword_index import KeywordIndex
from guideline_chatbot.retrieval.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Domain-specific clinical gating keywords for Hypertension and Type 2 Diabetes decision support
IN_SCOPE_TERMS = re.compile(
    r"\b(?:hypertension|hypertensive|blood\s+pressure|bp|sbp|dbp|abpm|hbpm|target\s+bp|"
    r"diabetes|diabetic|t2dm|t1dm|hba1c|glycated|glycaemic|glycemic|blood\s+sugar|fasting\s+glucose|"
    r"postprandial|fpg|ogtt|metformin|insulin|amlodipine|ramipril|losartan|telmisartan|enalapril|"
    r"lisinopril|chlorthalidone|hydrochlorothiazide|indapamide|carvedilol|atenolol|bisoprolol|"
    r"metoprolol|spironolactone|eplerenone|dapagliflozin|empagliflozin|canagliflozin|sitagliptin|"
    r"linagliptin|vildagliptin|semaglutide|liraglutide|glimepiride|gliclazide|glipizide|"
    r"antihypertensive|antidiabetic|ace[- ]?inhibitors?|acei|arbs?|ccbs?|calcium\s+channel\s+blockers?|"
    r"thiazides?|beta[- ]?blockers?|mineralocorticoid|mra|sglt2i?|glp-?1|dpp-?4|sulfonylureas?|pre-eclampsia|"
    r"gestational\s+diabetes|gdm|diabetic\s+kidney\s+disease|resistant\s+hypertension|"
    r"attacc|aattcc|monotherapy|combination\s+therapy)\b",
    re.IGNORECASE,
)


class ClinicalIntent(str, Enum):
    """Categorized clinical query intent for precision guideline retrieval and ranking."""

    TARGET = "target"
    FIRST_LINE_DRUG = "first_line_drug"
    CONTRAINDICATION_SAFETY = "contraindication_safety"
    THRESHOLD_DIAGNOSIS = "threshold_diagnosis"
    GENERAL = "general"


def detect_clinical_intent(
    query: str, patient_state: dict[str, Any] | None = None
) -> ClinicalIntent:
    """Classify clinical query intent to guide intent-aware retrieval boosting and demotion.

    Args:
        query: User clinical query.
        patient_state: Optional structured patient context.

    Returns:
        ClinicalIntent indicating primary clinical intent.
    """
    q_lower = query.lower()

    # 1. Contraindication / Pregnancy Safety Intent
    is_preg = False
    if patient_state:
        is_preg = bool(
            patient_state.get("is_pregnant") or "pregnancy" in patient_state.get("conditions", [])
        )
    if is_preg or re.search(
        r"\b(?:pregnant|pregnancy|gestation|trimester|can\s+i\s+take|safe\s+(?:to\s+take|in)|"
        r"contraindicat|avoid|teratogen|breastfeeding|lactat|allergi|adverse)\b",
        q_lower,
    ):
        return ClinicalIntent.CONTRAINDICATION_SAFETY

    # 2. First-line / Initial Pharmacotherapy Intent
    if re.search(
        r"\b(?:which\s+drug|what\s+drug|first[- ]line|drug\s+class\s+first|initial\s+(?:drug|therapy|medication)|"
        r"start\s+with|step\s*1|first\s+choice|choice\s+of\s+drug|prefer(?:red)?\s+(?:drug|agent))\b",
        q_lower,
    ):
        return ClinicalIntent.FIRST_LINE_DRUG

    # 3. Treatment Target Intent
    if re.search(
        r"\b(?:target|goal|aim|reduce\s+to|below\s+1[345]0|<1[345]0|bp\s+target|control\s+target)\b",
        q_lower,
    ):
        return ClinicalIntent.TARGET

    # 4. Diagnostic Threshold / Staging Intent
    if re.search(
        r"\b(?:threshold|diagnos|stage\s*[12]|grade\s*[123]|cutoff|cut-off)\b",
        q_lower,
    ):
        return ClinicalIntent.THRESHOLD_DIAGNOSIS

    return ClinicalIntent.GENERAL


class HybridRetriever:
    """Combines ChromaDB dense semantic search with BM25 sparse keyword search."""

    @classmethod
    def load_default(
        cls,
        chunks_path: str = "guideline_chatbot/data/processed/guideline_chunks.json",
        chroma_dir: str = "chroma",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> HybridRetriever:
        """Convenience loader initializing the complete default hybrid retrieval system."""
        from guideline_chatbot.retrieval.index_pipeline import build_retrieval_system

        retriever, _ = build_retrieval_system(
            chunks_path=chunks_path,
            chroma_dir=chroma_dir,
            model_name=model_name,
            rebuild=False,
        )
        return retriever

    def __init__(
        self,
        vector_store: VectorStore,
        keyword_index: KeywordIndex,
        embedding_manager: EmbeddingManager,
        dense_weight: float = 0.5,
        sparse_weight: float = 0.5,
        rrf_k: int = 60,
        use_reranker: bool = False,
    ) -> None:
        self.vector_store = vector_store
        self.keyword_index = keyword_index
        self.embedding_manager = embedding_manager
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight
        self.rrf_k = rrf_k
        self.use_reranker = use_reranker

    def compute_patient_applicability(
        self,
        meta: dict[str, Any],
        patient_state: dict[str, Any] | None,
    ) -> tuple[str, float]:
        """Compute patient-aware applicability flag and scoring multiplier.

        Args:
            meta: Chunk metadata dictionary.
            patient_state: Optional patient state dictionary containing:
                age, conditions, medications, vitals, is_pregnant.

        Returns:
            Tuple of (applicability_flag, score_multiplier).
            applicability_flag: "matches" | "unknown" | "conflicts"
        """
        if not patient_state:
            return "unknown", 1.0

        pop_tags = [
            t.strip().lower() for t in meta.get("population_tags", "").split(",") if t.strip()
        ]

        patient_age = patient_state.get("age")
        patient_conditions = [c.lower() for c in patient_state.get("conditions", [])]
        is_pregnant = patient_state.get("is_pregnant", False) or ("pregnancy" in patient_conditions)

        # 1. Metadata-Driven Exception & Contraindication Conflict Check
        # Checks if chunk's explicit exceptions/contraindications mention patient context
        exceptions_text = str(meta.get("exceptions", "") or "").lower()
        applicability_text = str(meta.get("applicability_conditions", "") or "").lower()

        if exceptions_text:
            if is_pregnant and re.search(r"\bpregnan", exceptions_text):
                return "conflicts", 0.2
            if any(
                "ckd" in c or "renal" in c or "kidney" in c for c in patient_conditions
            ) and re.search(r"\b(?:renal|kidney|egfr|crcl)\b", exceptions_text):
                return "conflicts", 0.3
            if any("asthma" in c for c in patient_conditions) and re.search(
                r"\basthma\b", exceptions_text
            ):
                return "conflicts", 0.3
            if any("heart failure" in c or "chf" in c for c in patient_conditions) and re.search(
                r"\bheart\s+failure\b", exceptions_text
            ):
                return "conflicts", 0.3

        # 2. Metadata-Driven Population Tag Conflicts
        if patient_age is not None:
            if patient_age >= 80 and "young_adults" in pop_tags:
                return "conflicts", 0.4
            if patient_age < 45 and "elderly" in pop_tags:
                return "conflicts", 0.4

        # 3. Metadata-Driven Applicability & Population Tag Matches
        matches_found = 0
        if is_pregnant and "pregnancy" in pop_tags:
            matches_found += 1
        if (
            any("ckd" in c or "renal" in c or "kidney" in c for c in patient_conditions)
            and "chronic_kidney_disease" in pop_tags
        ):
            matches_found += 1
        if (
            any("diabetes" in c or "t2dm" in c for c in patient_conditions)
            and "type_2_diabetes" in pop_tags
        ):
            matches_found += 1
        if (
            any(
                "cvd" in c or "cad" in c or "heart failure" in c or "stroke" in c
                for c in patient_conditions
            )
            and "cardiovascular_disease" in pop_tags
        ):
            matches_found += 1
        if patient_age is not None and (
            (patient_age >= 65 and "elderly" in pop_tags)
            or (patient_age < 55 and "young_adults" in pop_tags)
        ):
            matches_found += 1

        if matches_found > 0:
            return "matches", 1.2

        if applicability_text:
            if (
                any("diabetes" in c for c in patient_conditions)
                and "diabetes" in applicability_text
            ):
                return "matches", 1.15
            if any("ckd" in c for c in patient_conditions) and (
                "ckd" in applicability_text or "kidney" in applicability_text
            ):
                return "matches", 1.15

        return "unknown", 1.0

    def detect_clinical_disagreements(
        self,
        hits: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Identify if top retrieved hits disagree on targets or protocols (cross-jurisdiction or within-source).

        Returns:
            List of detected disagreement items with divergent source metadata.
        """
        disagreements: list[dict[str, Any]] = []
        if len(hits) < 2:
            return disagreements

        # 1. Check for within-source ICMR Blood Pressure target disagreement (HTN poster vs T2DM poster)
        icmr_htn_target = next(
            (
                h
                for h in hits
                if h["metadata"].get("doc_id") == "icmr_htn_001"
                and "blood pressure control targets" in h["text"].lower()
            ),
            None,
        )
        icmr_t2dm_target = next(
            (
                h
                for h in hits
                if h["metadata"].get("doc_id") == "icmr_t2dm_001"
                and "metabolic targets" in h["text"].lower()
            ),
            None,
        )
        if icmr_htn_target and icmr_t2dm_target:
            disagreements.append(
                {
                    "domain": "Blood Pressure Target in Diabetes (Within-Source ICMR Disagreement)",
                    "description": (
                        "ICMR Hypertension STW specifies target < 130/80 mmHg in diabetes, "
                        "whereas ICMR Type 2 Diabetes STW specifies target < 140/90 mmHg (< 130/80 in CKD)."
                    ),
                    "divergent_sources": [
                        {
                            "issuing_organization": "ICMR",
                            "document_name": "ICMR STW Hypertension in Adults",
                            "chunk_id": icmr_htn_target["chunk_id"],
                            "page_start": 1,
                        },
                        {
                            "issuing_organization": "ICMR",
                            "document_name": "ICMR STW Diabetes Mellitus Type 2",
                            "chunk_id": icmr_t2dm_target["chunk_id"],
                            "page_start": 1,
                        },
                    ],
                }
            )

        # 2. Group hits by issuing organization / jurisdiction for cross-guideline disagreements
        jurisdictions = {
            h["metadata"].get("jurisdiction") for h in hits if h["metadata"].get("jurisdiction")
        }
        if len(jurisdictions) < 2:
            return disagreements

        # Check for Blood Pressure target disagreements
        target_hits = [
            h
            for h in hits
            if "target" in h["text"].lower() and "blood pressure" in h["text"].lower()
        ]
        if len(target_hits) >= 2:
            orgs = {h["metadata"].get("issuing_organization") for h in target_hits}
            if len(orgs) >= 2:
                disagreements.append(
                    {
                        "domain": "Blood Pressure Target",
                        "description": "Cross-guideline variation detected in blood pressure targets.",
                        "divergent_sources": [
                            {
                                "issuing_organization": h["metadata"].get("issuing_organization"),
                                "document_name": h["metadata"].get("document_name"),
                                "chunk_id": h["chunk_id"],
                                "page_start": h["metadata"].get("page_start"),
                                "recommendation_year": h["metadata"].get("recommendation_year"),
                            }
                            for h in target_hits[:3]
                        ],
                    }
                )

        # Check for First-Line Initial Pharmacotherapy Strategy (Monotherapy vs Dual SPC)
        strategy_hits = [
            h
            for h in hits
            if any(
                k in h["text"].lower()
                for k in ["combination therapy", "monotherapy", "initial treatment", "first-line"]
            )
        ]
        if len(strategy_hits) >= 2:
            orgs = {h["metadata"].get("issuing_organization") for h in strategy_hits}
            if len(orgs) >= 2:
                disagreements.append(
                    {
                        "domain": "Initial Pharmacotherapy Strategy (Monotherapy vs Dual FDC)",
                        "description": "ICMR/WHO suggest dual combination / FDC by default; NICE/MoHFW specify stepwise monotherapy at Step 1.",
                        "divergent_sources": [
                            {
                                "issuing_organization": h["metadata"].get("issuing_organization"),
                                "document_name": h["metadata"].get("document_name"),
                                "chunk_id": h["chunk_id"],
                                "page_start": h["metadata"].get("page_start"),
                            }
                            for h in strategy_hits[:3]
                        ],
                    }
                )

        return disagreements

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        patient_state: dict[str, Any] | None = None,
        where_filter: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform hybrid retrieval with RRF, patient applicability, and disagreement detection.

        Args:
            query: Clinical query string.
            top_k: Number of final results to return.
            patient_state: Optional structured patient context.
            where_filter: Optional metadata filter.

        Returns:
            Dict containing:
                - "hits": list of top ranked chunk objects
                - "disagreements": list of detected cross-source disagreements
                - "is_out_of_scope": boolean indicating out-of-scope query
        """
        # Step 1: Out-of-scope domain gating check & multi-turn query contextualization
        has_clinical_keywords = bool(IN_SCOPE_TERMS.search(query))
        search_query = query

        # Resolve condition filter: patients with both conditions retrieve hypertension, type_2_diabetes, and both
        resolved_filter = where_filter
        if patient_state and patient_state.get("conditions"):
            p_conds = [c.lower() for c in patient_state["conditions"]]
            has_htn = any(
                "hypertension" in c or "htn" in c or "blood pressure" in c for c in p_conds
            )
            has_dm = any("diabetes" in c or "t2dm" in c for c in p_conds)
            if has_htn and has_dm:
                if not resolved_filter:
                    resolved_filter = {
                        "condition": {"$in": ["hypertension", "type_2_diabetes", "both"]}
                    }
                elif "condition" in resolved_filter:
                    resolved_filter = dict(resolved_filter)
                    resolved_filter["condition"] = {
                        "$in": ["hypertension", "type_2_diabetes", "both"]
                    }

        if resolved_filter and "condition" in resolved_filter:
            cond_val = resolved_filter["condition"]
            if cond_val == "both":
                resolved_filter = dict(resolved_filter)
                resolved_filter["condition"] = {"$in": ["hypertension", "type_2_diabetes", "both"]}
            elif cond_val == "hypertension":
                resolved_filter = dict(resolved_filter)
                resolved_filter["condition"] = {"$in": ["hypertension", "both"]}
            elif cond_val == "type_2_diabetes":
                resolved_filter = dict(resolved_filter)
                resolved_filter["condition"] = {"$in": ["type_2_diabetes", "both"]}

        if not has_clinical_keywords and patient_state and patient_state.get("conditions"):
            # Contextualize follow-up questions using established patient conditions
            context_conds = [
                c.replace("_", " ")
                for c in patient_state["conditions"]
                if c in {"hypertension", "type_2_diabetes", "chronic_kidney_disease"}
            ]
            if context_conds:
                search_query = f"{' '.join(context_conds)} {query}"
                has_clinical_keywords = True

        # Step 1.5: Clinical query intent classification & query augmentation
        intent = detect_clinical_intent(query, patient_state)
        dense_query = search_query
        sparse_query = search_query

        if intent == ClinicalIntent.TARGET:
            sparse_query = f"{search_query} target clinic blood pressure below 140/90 150/90 130/80 control goal"
            dense_query = f"{search_query} blood pressure target goal for control"
        elif intent == ClinicalIntent.FIRST_LINE_DRUG:
            sparse_query = (
                f"{search_query} first-line initial drug step 1 preferred drug class therapy"
            )
            has_dm = False
            if patient_state and patient_state.get("conditions"):
                has_dm = any("diabetes" in c or "t2dm" in c for c in patient_state["conditions"])
            if "diabetes" in search_query.lower() or has_dm:
                sparse_query += " ace inhibitor arb type 2 diabetes microalbuminuria offer"
                dense_query = f"{search_query} first-line drug choice for hypertension in type 2 diabetes ACE inhibitor ARB"
        elif intent == ClinicalIntent.CONTRAINDICATION_SAFETY:
            sparse_query = f"{search_query} contraindicated contraindication avoid not for use pregnancy safety teratogenic mhra"
            dense_query = f"{search_query} pregnancy contraindications antihypertensive safety ACE inhibitor enalapril"

        # Step 1.5: Clinical query intent classification & query augmentation
        intent = detect_clinical_intent(query, patient_state)
        dense_query = search_query
        sparse_query = search_query

        if intent == ClinicalIntent.TARGET:
            sparse_query = f"{search_query} target clinic blood pressure below 140/90 150/90 130/80 control goal"
            dense_query = f"{search_query} blood pressure target goal for control"
        elif intent == ClinicalIntent.FIRST_LINE_DRUG:
            sparse_query = (
                f"{search_query} first-line initial drug step 1 preferred drug class therapy"
            )
            has_dm = False
            if patient_state and patient_state.get("conditions"):
                has_dm = any("diabetes" in c or "t2dm" in c for c in patient_state["conditions"])
            if "diabetes" in search_query.lower() or has_dm:
                sparse_query += " ace inhibitor arb type 2 diabetes microalbuminuria offer"
                dense_query = f"{search_query} first-line drug choice for hypertension in type 2 diabetes ACE inhibitor ARB"
        elif intent == ClinicalIntent.CONTRAINDICATION_SAFETY:
            sparse_query = f"{search_query} contraindicated contraindication avoid not for use pregnancy safety teratogenic mhra"
            dense_query = f"{search_query} pregnancy contraindications antihypertensive safety ACE inhibitor enalapril"

        # Retrieve top candidates from each retriever for fusion
        fetch_k = max(80, top_k * 12)

        dense_hits = self.vector_store.query_dense(
            query_text=dense_query,
            embedding_manager=self.embedding_manager,
            top_k=fetch_k,
            where_filter=resolved_filter,
        )

        sparse_hits = self.keyword_index.query_sparse(
            query_text=sparse_query,
            top_k=fetch_k,
            where_filter=resolved_filter,
        )

        best_dense = dense_hits[0]["score"] if dense_hits else 0.0

        # Gating: out of scope if no clinical domain keywords AND low dense similarity,
        # or completely irrelevant query
        if (not has_clinical_keywords and best_dense < 0.46) or (
            best_dense < 0.32 and not sparse_hits
        ):
            logger.info(
                "Query '%s' classified as out-of-scope (keywords=%s, dense=%.3f)",
                query,
                has_clinical_keywords,
                best_dense,
            )
            return {
                "hits": [],
                "disagreements": [],
                "is_out_of_scope": True,
            }

        # Step 2: Reciprocal Rank Fusion (RRF)
        rrf_scores: dict[str, float] = {}
        all_items: dict[str, dict[str, Any]] = {}

        for rank, hit in enumerate(dense_hits):
            cid = hit["chunk_id"]
            all_items[cid] = hit
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + self.dense_weight / (self.rrf_k + rank + 1)

        for rank, hit in enumerate(sparse_hits):
            cid = hit["chunk_id"]
            if cid not in all_items:
                all_items[cid] = hit
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + self.sparse_weight / (
                self.rrf_k + rank + 1
            )

        # Step 2.5: Guideline source affinity check
        query_lower = query.lower()
        target_org = None
        if re.search(r"\bicmr\b|\bstw\b", query_lower):
            target_org = "ICMR"
        elif re.search(r"\bnice\b|\bng136\b|\bng28\b", query_lower):
            target_org = "NICE"
        elif re.search(r"\bwho\b|\bhearts\b", query_lower):
            target_org = "WHO"
        elif re.search(r"\bmohfw\b|\bstg\b", query_lower):
            target_org = "MoHFW"

        # Step 3: Patient-Aware & Clinical Intent Applicability Scoring
        scored_candidates: list[dict[str, Any]] = []
        patient_age = patient_state.get("age") if patient_state else None
        patient_conds = (
            [c.lower() for c in patient_state.get("conditions", [])] if patient_state else []
        )

        for cid, rrf_score in rrf_scores.items():
            hit_data = all_items[cid]
            meta = hit_data["metadata"]
            heading_lower = (meta.get("heading") or "").lower()
            text_lower = hit_data["text"].lower()
            chunk_type = meta.get("chunk_type", "")

            app_flag, multiplier = self.compute_patient_applicability(meta, patient_state)
            if target_org and target_org.lower() in meta.get("issuing_organization", "").lower():
                multiplier *= 1.45

            # Step 3.1: Universal Noise Demotion (Screening, Methods, Implementation Tools)
            if any(
                h in heading_lower
                for h in [
                    "agree ii",
                    "implementation tools",
                    "screening pathway",
                    "rescreening",
                    "cuff size",
                    "smoking in previous",
                    "interval of at least 1 minute",
                    "prevention",
                ]
            ):
                multiplier *= 0.05
            if chunk_type in ["methods", "screening"]:
                multiplier *= 0.1

            # Step 3.2: Clinical Intent Specific Re-ranking Multipliers
            if intent == ClinicalIntent.TARGET:
                if (
                    re.search(
                        r"\b(?:target|below\s+1[345]0|<1[345]0|reduce\s+clinic\s+blood\s+pressure|target\s+for\s+control)\b",
                        text_lower,
                    )
                    or "target" in heading_lower
                ):
                    multiplier *= 1.8
                if patient_age is not None:
                    if patient_age >= 80:
                        if re.search(
                            r"\b(?:80\s+and\s+over|aged\s+80|above\s+80|150/90)\b", text_lower
                        ):
                            multiplier *= 3.0
                        if re.search(
                            r"\b(?:under\s+80|less\s+than\s+80|<140/90|aged\s+under\s+\d+)\b",
                            text_lower,
                        ) and not re.search(r"80\s+and\s+over", text_lower):
                            multiplier *= 0.1
                    elif patient_age < 80:
                        if re.search(
                            r"\b(?:under\s+80|less\s+than\s+80|<140/90|below\s+140/90)\b",
                            text_lower,
                        ):
                            multiplier *= 2.0
                        if re.search(r"\b(?:80\s+and\s+over|aged\s+80)\b", text_lower):
                            multiplier *= 0.1

            elif intent == ClinicalIntent.FIRST_LINE_DRUG:
                is_dm = "diabetes" in query_lower or any(
                    "diabetes" in c or "t2dm" in c for c in patient_conds
                )
                if is_dm:
                    if re.search(
                        r"\b(?:step\s*1|first[- ]line|preferred)\b", text_lower
                    ) and re.search(r"\b(?:ace\s+inhibitor|arb|angiotensin)\b", text_lower):
                        multiplier *= 3.5
                    elif (
                        re.search(r"\b(?:ace\s+inhibitor|arb)\b", text_lower)
                        and "diabetes" in text_lower
                    ):
                        multiplier *= 2.2
                if re.search(r"initiated in patients with grade 2 hypertension on", heading_lower):
                    multiplier *= 0.1

            elif intent == ClinicalIntent.CONTRAINDICATION_SAFETY:
                is_preg_ctx = (
                    (patient_state and patient_state.get("is_pregnant"))
                    or "pregnant" in query_lower
                    or "pregnancy" in query_lower
                )
                if is_preg_ctx:
                    exc_text = (meta.get("exceptions") or "").lower()
                    has_preg_text = bool(
                        re.search(r"\b(?:pregnant|pregnancy|teratogenic|mhra)\b", text_lower)
                        or "pregnancy" in exc_text
                    )
                    if not has_preg_text:
                        multiplier *= 0.05
                    else:
                        if (
                            re.search(
                                r"\b(?:contraindicated|contraindication|not\s+for\s+use|avoid|teratogenic|harm|safety\s+advice|stop)\b",
                                text_lower,
                            )
                            or "pregnancy" in exc_text
                        ):
                            multiplier *= 3.5
                        else:
                            multiplier *= 2.0

            # Step 3.1: Universal Noise Demotion (Screening, Methods, Implementation Tools)
            if any(
                h in heading_lower
                for h in [
                    "agree ii",
                    "implementation tools",
                    "screening pathway",
                    "rescreening",
                    "cuff size",
                    "smoking in previous",
                    "interval of at least 1 minute",
                    "prevention",
                ]
            ):
                multiplier *= 0.05
            if chunk_type in ["methods", "screening"]:
                multiplier *= 0.1

            # Step 3.2: Clinical Intent Specific Re-ranking Multipliers
            if intent == ClinicalIntent.TARGET:
                if (
                    re.search(
                        r"\b(?:target|below\s+1[345]0|<1[345]0|reduce\s+clinic\s+blood\s+pressure|target\s+for\s+control)\b",
                        text_lower,
                    )
                    or "target" in heading_lower
                ):
                    multiplier *= 1.8
                if patient_age is not None:
                    if patient_age >= 80:
                        if re.search(
                            r"\b(?:80\s+and\s+over|aged\s+80|above\s+80|150/90)\b", text_lower
                        ):
                            multiplier *= 3.0
                        if re.search(
                            r"\b(?:under\s+80|less\s+than\s+80|<140/90|aged\s+under\s+\d+)\b",
                            text_lower,
                        ) and not re.search(r"80\s+and\s+over", text_lower):
                            multiplier *= 0.1
                    elif patient_age < 80:
                        if re.search(
                            r"\b(?:under\s+80|less\s+than\s+80|<140/90|below\s+140/90)\b",
                            text_lower,
                        ):
                            multiplier *= 2.0
                        if re.search(r"\b(?:80\s+and\s+over|aged\s+80)\b", text_lower):
                            multiplier *= 0.1

            elif intent == ClinicalIntent.FIRST_LINE_DRUG:
                is_dm = "diabetes" in query_lower or any(
                    "diabetes" in c or "t2dm" in c for c in patient_conds
                )
                if is_dm:
                    if re.search(
                        r"\b(?:step\s*1|first[- ]line|preferred)\b", text_lower
                    ) and re.search(r"\b(?:ace\s+inhibitor|arb|angiotensin)\b", text_lower):
                        multiplier *= 3.5
                    elif (
                        re.search(r"\b(?:ace\s+inhibitor|arb)\b", text_lower)
                        and "diabetes" in text_lower
                    ):
                        multiplier *= 2.2
                if re.search(r"initiated in patients with grade 2 hypertension on", heading_lower):
                    multiplier *= 0.1

            elif intent == ClinicalIntent.CONTRAINDICATION_SAFETY:
                is_preg_ctx = (
                    (patient_state and patient_state.get("is_pregnant"))
                    or "pregnant" in query_lower
                    or "pregnancy" in query_lower
                )
                if is_preg_ctx:
                    exc_text = (meta.get("exceptions") or "").lower()
                    has_preg_text = bool(
                        re.search(r"\b(?:pregnant|pregnancy|teratogenic|mhra)\b", text_lower)
                        or "pregnancy" in exc_text
                    )
                    if not has_preg_text:
                        multiplier *= 0.05
                    else:
                        if (
                            re.search(
                                r"\b(?:contraindicated|contraindication|not\s+for\s+use|avoid|teratogenic|harm|safety\s+advice|stop)\b",
                                text_lower,
                            )
                            or "pregnancy" in exc_text
                        ):
                            multiplier *= 3.5
                        else:
                            multiplier *= 2.0

            final_score = rrf_score * multiplier

            scored_candidates.append(
                {
                    "chunk_id": cid,
                    "text": hit_data["text"],
                    "score": round(final_score, 5),
                    "rrf_score": round(rrf_score, 5),
                    "applicability": app_flag,
                    "metadata": meta,
                }
            )

        # Sort by final patient-weighted score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        final_hits = scored_candidates[:top_k]

        # Step 4: Disagreement Detection
        disagreements = self.detect_clinical_disagreements(final_hits)

        return {
            "hits": final_hits,
            "disagreements": disagreements,
            "is_out_of_scope": False,
        }
