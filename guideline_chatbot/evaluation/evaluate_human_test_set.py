"""Independent evaluation runner for human-authored retrieval test set.

Evaluates an independent test set authored by human clinicians without
prior tuning, calculating standard Precision@5, bounded Precision@5,
Recall@5, MRR, and NDCG@5.
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any

from guideline_chatbot.chunking.schemas import GuidelineChunk
from guideline_chatbot.retrieval.embeddings import EmbeddingManager
from guideline_chatbot.retrieval.hybrid import HybridRetriever
from guideline_chatbot.retrieval.keyword_index import KeywordIndex
from guideline_chatbot.retrieval.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def compute_dcg(relevances: list[int], k: int = 5) -> float:
    """Compute Discounted Cumulative Gain at rank k."""
    dcg = 0.0
    for i, rel in enumerate(relevances[:k]):
        if rel > 0:
            dcg += (2**rel - 1) / math.log2(i + 2)
    return dcg


def compute_ndcg(relevances: list[int], total_relevant: int, k: int = 5) -> float:
    """Compute Normalized Discounted Cumulative Gain at rank k."""
    if total_relevant == 0:
        return 1.0 if not any(relevances[:k]) else 0.0
    actual_dcg = compute_dcg(relevances, k)
    ideal_rels = [1] * min(total_relevant, k)
    ideal_dcg = compute_dcg(ideal_rels, k)
    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0


def evaluate_human_test_set(
    test_set_path: Path,
    chunks_path: Path,
    chroma_dir: Path,
    output_report_path: Path | None = None,
) -> dict[str, Any]:
    """Run evaluation on the independent human test set.

    Args:
        test_set_path: Path to retrieval_test_set_human.json.
        chunks_path: Path to guideline_chunks.json.
        chroma_dir: Path to ChromaDB storage directory.
        output_report_path: Optional path to output markdown report.

    Returns:
        Evaluation summary dictionary.
    """
    if not test_set_path.is_file():
        raise FileNotFoundError(f"Human test set file not found: {test_set_path}")

    with open(test_set_path, encoding="utf-8") as f:
        entries: list[dict[str, Any]] = json.load(f)

    # Check for filled entries
    filled_entries = [
        e for e in entries if e.get("question", "").strip() and e.get("expected_documents_pages")
    ]

    if not filled_entries:
        logger.info(
            "Human test set is currently empty (%d templates pending human authoring).",
            len(entries),
        )
        summary = {
            "status": "pending_human_authoring",
            "total_templates": len(entries),
            "filled_entries": 0,
            "message": "Independent human test set is pending authoring. No evaluation performed.",
        }
        if output_report_path:
            output_report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_report_path, "w", encoding="utf-8") as f:
                f.write(
                    "# Independent Human Retrieval Test Set Report\n\n"
                    "**Status:** PENDING HUMAN AUTHORING\n\n"
                    f"Found {len(entries)} empty template entries in `{test_set_path}`. "
                    "Awaiting manual clinician questions and expected physical pages.\n"
                )
        return summary

    logger.info("Evaluating %d filled human test set queries...", len(filled_entries))

    # Load chunks and build retrieval index
    with open(chunks_path, encoding="utf-8") as f:
        chunks_raw = json.load(f)
    chunks = [GuidelineChunk.model_validate(c) for c in chunks_raw]

    embedding_manager = EmbeddingManager()
    vector_store = VectorStore(persist_dir=chroma_dir)

    keyword_index = KeywordIndex()
    keyword_index.build_index(chunks)

    retriever = HybridRetriever(
        vector_store=vector_store,
        keyword_index=keyword_index,
        embedding_manager=embedding_manager,
    )

    precisions_standard: list[float] = []
    precisions_bounded: list[float] = []
    recalls: list[float] = []
    reciprocal_ranks: list[float] = []
    ndcgs: list[float] = []

    for item in filled_entries:
        query = item["question"]
        expected_docs_pages: list[dict[str, Any]] = item.get("expected_documents_pages", [])
        patient_ctx = item.get("patient_context")

        retrieval_res = retriever.retrieve(query=query, top_k=5, patient_state=patient_ctx)
        hits = retrieval_res["hits"]

        # Check hits against expected doc and page ranges
        relevances: list[int] = []
        for hit in hits:
            h_meta = hit["metadata"]
            h_doc = h_meta.get("doc_id")
            h_page = h_meta.get("page_start", 0)

            is_rel = False
            for exp in expected_docs_pages:
                exp_doc = exp.get("doc_id")
                exp_pages = exp.get("pages", [])
                if h_doc == exp_doc and (not exp_pages or h_page in exp_pages):
                    is_rel = True
                    break
            relevances.append(1 if is_rel else 0)

        num_rel = sum(relevances)
        total_exp = len(expected_docs_pages)

        # Standard Precision@5: rel / 5
        prec_std = num_rel / 5.0
        # Bounded Precision@5: rel / min(5, total_expected)
        prec_bnd = num_rel / min(5, total_exp) if total_exp > 0 else 0.0
        # Recall@5: rel / total_expected
        rec = num_rel / total_exp if total_exp > 0 else 0.0

        # MRR
        rr = 0.0
        for rank_idx, rel_val in enumerate(relevances):
            if rel_val == 1:
                rr = 1.0 / (rank_idx + 1)
                break

        # NDCG@5
        ndcg_val = compute_ndcg(relevances, total_exp, k=5)

        precisions_standard.append(prec_std)
        precisions_bounded.append(prec_bnd)
        recalls.append(rec)
        reciprocal_ranks.append(rr)
        ndcgs.append(ndcg_val)

    mean_prec_std = sum(precisions_standard) / len(precisions_standard)
    mean_prec_bnd = sum(precisions_bounded) / len(precisions_bounded)
    mean_recall = sum(recalls) / len(recalls)
    mean_mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    mean_ndcg = sum(ndcgs) / len(ndcgs)

    summary = {
        "status": "evaluated",
        "total_queries": len(filled_entries),
        "mean_precision_at_5_standard": round(mean_prec_std, 4),
        "mean_precision_at_5_bounded": round(mean_prec_bnd, 4),
        "mean_recall_at_5": round(mean_recall, 4),
        "mrr": round(mean_mrr, 4),
        "ndcg_at_5": round(mean_ndcg, 4),
    }

    logger.info("Human Test Set Results: %s", summary)
    return summary


if __name__ == "__main__":
    test_path = Path("guideline_chatbot/evaluation/retrieval_test_set_human.json")
    c_path = Path("guideline_chatbot/data/processed/guideline_chunks.json")
    c_dir = Path("guideline_chatbot/data/chroma")
    rep_path = Path("guideline_chatbot/data/reports/human_test_set_evaluation_report.md")

    evaluate_human_test_set(test_path, c_path, c_dir, rep_path)
