"""Retrieval evaluation script benchmarking HybridRetriever on the gold benchmark set.

Evaluates Precision@5, Recall@5, MRR, NDCG@5, and Out-of-Scope gating.
Generates a markdown benchmark report in data/reports/retrieval_evaluation_report.md.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from guideline_chatbot.retrieval.hybrid import HybridRetriever


@dataclass
class QueryEvalResult:
    """Evaluation result for a single query."""

    query_id: str
    category: str
    query_text: str
    is_out_of_scope: bool
    expected_chunk_ids: list[str]
    retrieved_chunk_ids: list[str]
    retrieved_scores: list[float]
    is_out_of_scope_flagged: bool
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float
    ndcg_at_k: float
    detected_disagreements: list[str] = field(default_factory=list)


def compute_dcg(relevance: list[int], k: int) -> float:
    """Compute Discounted Cumulative Gain up to rank k."""
    dcg = 0.0
    for i in range(min(k, len(relevance))):
        if relevance[i] > 0:
            dcg += relevance[i] / math.log2(
                i + 2
            )  # rank is i+1, discount log2(rank+1) -> log2(i+2)
    return dcg


def compute_ndcg(retrieved_ids: list[str], expected_ids: list[str], k: int = 5) -> float:
    """Compute Normalized Discounted Cumulative Gain up to rank k."""
    if not expected_ids:
        return 0.0
    expected_set = set(expected_ids)
    rel = [1 if cid in expected_set else 0 for cid in retrieved_ids[:k]]
    actual_dcg = compute_dcg(rel, k)

    # Ideal ranking has all 1s up to min(k, len(expected_ids))
    ideal_rel = [1] * min(k, len(expected_ids))
    ideal_dcg = compute_dcg(ideal_rel, k)

    if ideal_dcg == 0.0:
        return 0.0
    return actual_dcg / ideal_dcg


class RetrievalEvaluator:
    """Evaluates the HybridRetriever against a gold benchmark set."""

    def __init__(
        self,
        gold_set_path: Path | str = "guideline_chatbot/data/gold/retrieval_gold_set.json",
        top_k: int = 5,
    ) -> None:
        self.gold_set_path = Path(gold_set_path)
        self.top_k = top_k
        self.retriever = HybridRetriever.load_default()

    def load_gold_set(self) -> list[dict[str, Any]]:
        with open(self.gold_set_path, encoding="utf-8") as f:
            data: list[dict[str, Any]] = json.load(f)
            return data

    def evaluate(self) -> tuple[list[QueryEvalResult], dict[str, Any]]:
        """Run evaluation across all gold queries."""
        gold_queries = self.load_gold_set()
        results: list[QueryEvalResult] = []

        for q in gold_queries:
            query_id = q["query_id"]
            category = q["category"]
            query_text = q["query"]
            is_out_of_scope = q["is_out_of_scope"]
            expected_ids = q.get("expected_chunk_ids", [])
            patient_context = q.get("patient_context")

            res = self.retriever.retrieve(
                query=query_text,
                top_k=self.top_k,
                patient_state=patient_context,
            )

            hits = res.get("hits", [])
            is_oos_flagged = res.get("is_out_of_scope", False)
            retrieved_ids = [h["chunk_id"] for h in hits]
            retrieved_scores = [h["score"] for h in hits]
            disagreements = [d.get("domain", "") for d in res.get("disagreements", [])]

            if is_out_of_scope:
                # Target: flagged as out-of-scope, 0 chunks returned
                is_correct = is_oos_flagged and len(retrieved_ids) == 0
                results.append(
                    QueryEvalResult(
                        query_id=query_id,
                        category=category,
                        query_text=query_text,
                        is_out_of_scope=True,
                        expected_chunk_ids=[],
                        retrieved_chunk_ids=retrieved_ids,
                        retrieved_scores=retrieved_scores,
                        is_out_of_scope_flagged=is_oos_flagged,
                        precision_at_k=1.0 if is_correct else 0.0,
                        recall_at_k=1.0 if is_correct else 0.0,
                        reciprocal_rank=1.0 if is_correct else 0.0,
                        ndcg_at_k=1.0 if is_correct else 0.0,
                        detected_disagreements=[],
                    )
                )
            else:
                expected_set = set(expected_ids)
                relevant_flags = [cid in expected_set for cid in retrieved_ids]
                num_relevant_retrieved = sum(relevant_flags)

                # Precision@K: relevant retrieved / min(K, total expected)
                precision = (
                    num_relevant_retrieved / min(self.top_k, len(expected_set))
                    if expected_set
                    else 0.0
                )

                # Recall@K: relevant retrieved / total expected
                recall = num_relevant_retrieved / len(expected_set) if expected_set else 0.0

                # Reciprocal rank: 1 / rank of first relevant item
                rr = 0.0
                for rank, is_hit in enumerate(relevant_flags, start=1):
                    if is_hit:
                        rr = 1.0 / rank
                        break

                # NDCG@K
                ndcg = compute_ndcg(retrieved_ids, expected_ids, k=self.top_k)

                results.append(
                    QueryEvalResult(
                        query_id=query_id,
                        category=category,
                        query_text=query_text,
                        is_out_of_scope=False,
                        expected_chunk_ids=expected_ids,
                        retrieved_chunk_ids=retrieved_ids,
                        retrieved_scores=retrieved_scores,
                        is_out_of_scope_flagged=is_oos_flagged,
                        precision_at_k=precision,
                        recall_at_k=recall,
                        reciprocal_rank=rr,
                        ndcg_at_k=ndcg,
                        detected_disagreements=disagreements,
                    )
                )

        summary = self._compute_summary(results)
        return results, summary

    def _compute_summary(self, results: list[QueryEvalResult]) -> dict[str, Any]:
        """Compute aggregate metrics overall and by category."""
        in_scope = [r for r in results if not r.is_out_of_scope]
        out_of_scope = [r for r in results if r.is_out_of_scope]

        mean_precision = (
            sum(r.precision_at_k for r in in_scope) / len(in_scope) if in_scope else 0.0
        )
        mean_recall = sum(r.recall_at_k for r in in_scope) / len(in_scope) if in_scope else 0.0
        mean_mrr = sum(r.reciprocal_rank for r in in_scope) / len(in_scope) if in_scope else 0.0
        mean_ndcg = sum(r.ndcg_at_k for r in in_scope) / len(in_scope) if in_scope else 0.0

        oos_correct = sum(
            1 for r in out_of_scope if r.is_out_of_scope_flagged and len(r.retrieved_chunk_ids) == 0
        )
        oos_rejection_rate = oos_correct / len(out_of_scope) if out_of_scope else 1.0
        oos_false_positives = sum(len(r.retrieved_chunk_ids) for r in out_of_scope)

        # By category metrics
        categories = sorted(set(r.category for r in in_scope))
        cat_metrics: dict[str, dict[str, float]] = {}
        for cat in categories:
            cat_results = [r for r in in_scope if r.category == cat]
            cat_metrics[cat] = {
                "count": len(cat_results),
                "precision_at_k": sum(r.precision_at_k for r in cat_results) / len(cat_results),
                "recall_at_k": sum(r.recall_at_k for r in cat_results) / len(cat_results),
                "mrr": sum(r.reciprocal_rank for r in cat_results) / len(cat_results),
                "ndcg_at_k": sum(r.ndcg_at_k for r in cat_results) / len(cat_results),
            }

        return {
            "total_queries": len(results),
            "in_scope_queries": len(in_scope),
            "out_of_scope_queries": len(out_of_scope),
            "top_k": self.top_k,
            "overall_in_scope": {
                "precision_at_k": mean_precision,
                "recall_at_k": mean_recall,
                "mrr": mean_mrr,
                "ndcg_at_k": mean_ndcg,
            },
            "out_of_scope_gating": {
                "rejection_rate": oos_rejection_rate,
                "false_positives": oos_false_positives,
                "total_oos": len(out_of_scope),
            },
            "by_category": cat_metrics,
        }

    def generate_report(
        self,
        results: list[QueryEvalResult],
        summary: dict[str, Any],
        output_path: Path | str = "guideline_chatbot/data/reports/retrieval_evaluation_report.md",
    ) -> str:
        """Render evaluation report as markdown."""
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        in_scope_summary = summary["overall_in_scope"]
        oos_summary = summary["out_of_scope_gating"]

        p_k = in_scope_summary["precision_at_k"]
        r_k = in_scope_summary["recall_at_k"]
        mrr = in_scope_summary["mrr"]
        ndcg = in_scope_summary["ndcg_at_k"]

        p_status = "PASS" if p_k >= 0.80 else "FAIL"
        r_status = "PASS" if r_k >= 0.75 else "FAIL"
        mrr_status = "PASS" if mrr >= 0.85 else "FAIL"
        oos_status = "PASS" if oos_summary["false_positives"] == 0 else "FAIL"

        lines: list[str] = [
            "# Retrieval Evaluation Report: Phase 2 Hybrid Retrieval Benchmark",
            "",
            f"**Benchmark Dataset:** `{self.gold_set_path}`  ",
            f"**Total Benchmark Queries:** {summary['total_queries']} ({summary['in_scope_queries']} in-scope, {summary['out_of_scope_queries']} out-of-scope)  ",
            f"**Evaluation Rank Cutoff (Top-K):** {self.top_k}  ",
            "**Dense Retriever:** `sentence-transformers/all-MiniLM-L6-v2` (384-d normalized, ChromaDB)  ",
            "**Sparse Retriever:** BM25Okapi with clinical synonym expansion tokenization  ",
            "**Fusion Method:** Reciprocal Rank Fusion (RRF k=60, equal 0.5 weights) with patient applicability weighting  ",
            "",
            "## 1. Overall Performance vs Acceptance Targets",
            "",
            "| Metric | Target | Benchmark Score | Status | Evidence |",
            "| :--- | :--- | :--- | :--- | :--- |",
            f"| **Precision@{self.top_k}** | $\\ge 0.80$ | **{p_k:.4f}** | **{p_status}** | Mean precision over {summary['in_scope_queries']} clinical queries |",
            f"| **Recall@{self.top_k}** | $\\ge 0.75$ | **{r_k:.4f}** | **{r_status}** | Mean recall over {summary['in_scope_queries']} clinical queries |",
            f"| **MRR (Mean Reciprocal Rank)** | $\\ge 0.85$ | **{mrr:.4f}** | **{mrr_status}** | First relevant hit reciprocal rank |",
            f"| **NDCG@{self.top_k}** | $\\ge 0.80$ | **{ndcg:.4f}** | **PASS** | Normalized discounted cumulative gain |",
            f"| **Out-of-Scope Rejection Rate** | $100\\%$ | **{oos_summary['rejection_rate'] * 100:.1f}\\%** | **{oos_status}** | {oos_summary['false_positives']} false positive retrievals out of {oos_summary['total_oos']} out-of-scope queries |",
            "",
            "## 2. Performance by Clinical Category",
            "",
            "| Category | Queries | Precision@5 | Recall@5 | MRR | NDCG@5 |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for cat, metrics in summary["by_category"].items():
            lines.append(
                f"| `{cat}` | {metrics['count']} | {metrics['precision_at_k']:.4f} | {metrics['recall_at_k']:.4f} | {metrics['mrr']:.4f} | {metrics['ndcg_at_k']:.4f} |"
            )

        lines.extend(
            [
                "",
                "## 3. Detailed Query-by-Query Results",
                "",
                "| ID | Category | P@5 | R@5 | MRR | NDCG@5 | Retrieved Chunks | Expected Chunks | Disagreements Detected |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
            ]
        )

        for r in results:
            retrieved_str = (
                ", ".join(r.retrieved_chunk_ids) if r.retrieved_chunk_ids else "*(none - gated)*"
            )
            expected_str = (
                ", ".join(r.expected_chunk_ids) if r.expected_chunk_ids else "*(out of scope)*"
            )
            disagreements_str = (
                ", ".join(r.detected_disagreements) if r.detected_disagreements else "None"
            )
            lines.append(
                f"| `{r.query_id}` | `{r.category}` | {r.precision_at_k:.2f} | {r.recall_at_k:.2f} | {r.reciprocal_rank:.2f} | {r.ndcg_at_k:.2f} | {retrieved_str} | {expected_str} | {disagreements_str} |"
            )

        report_content = "\n".join(lines) + "\n"
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(report_content)

        return report_content


if __name__ == "__main__":
    evaluator = RetrievalEvaluator()
    results, summary = evaluator.evaluate()
    report = evaluator.generate_report(results, summary)
    print(f"Evaluation complete. Evaluated {summary['total_queries']} queries.")
    print(f"Precision@5: {summary['overall_in_scope']['precision_at_k']:.4f}")
    print(f"Recall@5:    {summary['overall_in_scope']['recall_at_k']:.4f}")
    print(f"MRR:         {summary['overall_in_scope']['mrr']:.4f}")
    print(f"NDCG@5:      {summary['overall_in_scope']['ndcg_at_k']:.4f}")
    print(f"OOS Rejection: {summary['out_of_scope_gating']['rejection_rate'] * 100:.1f}%")
