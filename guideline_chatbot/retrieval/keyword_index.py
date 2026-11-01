"""BM25 sparse keyword retriever with clinical synonym tokenization.

Expands medical acronyms (HTN, T2DM, ACEi, ARB, CCB, eGFR, HbA1c, SBP, DBP, ICMR, NICE, WHO, MoHFW)
to ensure exact lexical match parity with standard clinical phrasing.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from rank_bm25 import BM25Okapi

from guideline_chatbot.chunking.schemas import GuidelineChunk

logger = logging.getLogger(__name__)

# Common English stop words that should not inflate sparse keyword scores
STOP_WORDS: set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}

# Medical synonym and acronym expansion table
CLINICAL_SYNONYMS: dict[str, list[str]] = {
    "htn": ["hypertension", "blood pressure", "high blood pressure"],
    "t2dm": ["type 2 diabetes", "diabetes mellitus", "t2d"],
    "t1dm": ["type 1 diabetes", "t1d"],
    "acei": ["ace inhibitor", "angiotensin-converting enzyme inhibitor", "ramipril", "enalapril"],
    "arb": ["angiotensin receptor blocker", "telmisartan", "losartan", "olmesartan"],
    "ccb": ["calcium channel blocker", "amlodipine", "dihydropyridine"],
    "egfr": ["estimated glomerular filtration rate", "renal function", "kidney", "crcl"],
    "hba1c": ["glycated haemoglobin", "glycated hemoglobin", "a1c", "glycemic control"],
    "sbp": ["systolic blood pressure", "systolic bp"],
    "dbp": ["diastolic blood pressure", "diastolic bp"],
    "bp": ["blood pressure"],
    "ckd": ["chronic kidney disease", "renal impairment"],
    "cvd": ["cardiovascular disease", "ascvd", "coronary artery disease"],
    "cad": ["coronary artery disease", "angina", "myocardial infarction"],
    "mra": ["mineralocorticoid receptor antagonist", "spironolactone"],
    "sglt2i": ["sglt2 inhibitor", "dapagliflozin", "empagliflozin"],
    "glp1ra": ["glp-1 receptor agonist", "semaglutide", "liraglutide"],
    "dpp4i": ["dpp-4 inhibitor", "sitagliptin", "linagliptin"],
    "su": ["sulfonylurea", "glimepiride", "gliclazide"],
    "fpg": ["fasting plasma glucose", "fasting blood sugar"],
    "ogtt": ["oral glucose tolerance test"],
    "fdc": ["fixed-dose combination", "single-pill combination", "spc"],
    "spironolactone": ["spironolactone", "mra", "mineralocorticoid"],
    "breastfeeding": ["breastfeeding", "lactation", "nursing"],
    "icmr": ["icmr", "stw", "standard treatment workflow"],
    "nice": ["nice", "ng136", "ng28"],
    "who": ["who", "hearts", "hearts-d"],
    "mohfw": ["mohfw", "stg", "standard treatment guidelines"],
}


def clinical_tokenize(text: str) -> list[str]:
    """Tokenize clinical text with lowercasing, stopword removal, and synonym expansion."""
    raw_tokens = re.findall(r"\b[A-Za-z0-9_/%<>=.-]+\b", text.lower())
    expanded_tokens: list[str] = []

    for tok in raw_tokens:
        if tok in STOP_WORDS:
            continue
        expanded_tokens.append(tok)
        # Check acronym / synonym expansion
        if tok in CLINICAL_SYNONYMS:
            for syn in CLINICAL_SYNONYMS[tok]:
                expanded_tokens.extend([w for w in syn.split() if w not in STOP_WORDS])

    return expanded_tokens


class KeywordIndex:
    """In-memory BM25 sparse keyword index over guideline chunks."""

    def __init__(self) -> None:
        self.chunks: list[GuidelineChunk] = []
        self.chunk_ids: list[str] = []
        self.bm25: BM25Okapi | None = None
        self.corpus_tokens: list[list[str]] = []

    def build_index(self, chunks: list[GuidelineChunk]) -> int:
        """Build BM25 index over chunks flagged for retrieval.

        Args:
            chunks: List of GuidelineChunk objects.

        Returns:
            Number of indexed chunks.
        """
        # Exclude non-indexable noise (references, methods, flowcharts)
        self.chunks = [c for c in chunks if c.indexed_for_retrieval]
        self.chunk_ids = [c.chunk_id for c in self.chunks]

        logger.info(
            "Building BM25 index over %d indexable chunks...",
            len(self.chunks),
        )

        self.corpus_tokens = [
            clinical_tokenize(f"{c.issuing_organization} {c.document_name} {c.heading} {c.text}")
            for c in self.chunks
        ]
        self.bm25 = BM25Okapi(self.corpus_tokens)
        return len(self.chunks)

    def query_sparse(
        self,
        query_text: str,
        top_k: int = 10,
        where_filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve top-k chunks matching the sparse query with clinical tokenization.

        Args:
            query_text: Clinical query string.
            top_k: Number of candidates to return.
            where_filter: Optional filter dict (e.g. {'condition': 'hypertension'}).

        Returns:
            List of hit dicts: {chunk_id, text, score, metadata}.
        """
        if not self.bm25 or not self.chunks:
            return []

        tokens = clinical_tokenize(query_text)
        if not tokens:
            return []

        raw_scores = self.bm25.get_scores(tokens)

        # Pair scores with chunk indices
        scored_items: list[tuple[float, int]] = []
        for idx, score in enumerate(raw_scores):
            if score > 0.0:
                scored_items.append((float(score), idx))

        scored_items.sort(key=lambda x: x[0], reverse=True)

        results: list[dict[str, Any]] = []
        for score, idx in scored_items:
            chunk = self.chunks[idx]

            # Optional metadata filtering
            if where_filter:
                match = True
                if "$or" in where_filter:
                    match = any(
                        all(
                            (
                                getattr(chunk, sub_k, None) in sub_v.get("$in", [])
                                if isinstance(sub_v, dict) and "$in" in sub_v
                                else getattr(chunk, sub_k, None) == sub_v
                            )
                            for sub_k, sub_v in sub_dict.items()
                        )
                        for sub_dict in where_filter["$or"]
                    )
                else:
                    for k, v in where_filter.items():
                        if isinstance(v, dict) and "$in" in v:
                            if getattr(chunk, k, None) not in v["$in"]:
                                match = False
                                break
                        elif getattr(chunk, k, None) != v:
                            match = False
                            break
                if not match:
                    continue

            results.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "score": round(score, 4),
                    "metadata": {
                        "document_name": chunk.document_name,
                        "heading": chunk.heading,
                        "page_start": chunk.page_start,
                        "chunk_type": chunk.chunk_type,
                        "issuing_organization": chunk.issuing_organization,
                        "jurisdiction": chunk.jurisdiction,
                        "population_tags": ",".join(chunk.population_tags),
                        "drug_class_tags": ",".join(chunk.drug_class_tags),
                        "condition": chunk.condition,
                    },
                }
            )

            if len(results) >= top_k:
                break

        return results
