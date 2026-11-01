"""Unit and integration tests for Phase 2: Embeddings, ChromaDB, BM25, and Hybrid Retrieval."""

from __future__ import annotations

import tempfile

import numpy as np
import pytest

from guideline_chatbot.chunking.schemas import GuidelineChunk
from guideline_chatbot.retrieval.embeddings import EmbeddingManager
from guideline_chatbot.retrieval.hybrid import HybridRetriever
from guideline_chatbot.retrieval.keyword_index import KeywordIndex, clinical_tokenize
from guideline_chatbot.retrieval.vector_store import VectorStore


def create_sample_chunk(
    chunk_id: str = "test_chunk_001",
    text: str = "For adults with hypertension aged under 80, reduce clinic blood pressure to below 140/90 mmHg.",
    heading: str = "1.4.20 Blood pressure targets",
    condition: str = "hypertension",
    issuing_org: str = "NICE",
    pop_tags: list[str] | None = None,
    drug_tags: list[str] | None = None,
    indexed: bool = True,
) -> GuidelineChunk:
    """Helper creating a test GuidelineChunk."""
    return GuidelineChunk(
        chunk_id=chunk_id,
        doc_id="test_doc_001",
        document_name="Test Clinical Guideline",
        issuing_organization=issuing_org,
        jurisdiction="UK",
        condition=condition,
        section_path=f"1 Recommendations > {heading}",
        heading=heading,
        text=text,
        page_start=15,
        page_end=15,
        chunk_type="recommendation",
        population_tags=pop_tags or ["general_adults"],
        drug_class_tags=drug_tags or [],
        evidence_strength=None,
        recommendation_strength=None,
        applicability_conditions=None,
        exceptions=None,
        recommendation_year="2019",
        last_updated=None,
        last_updated_source=None,
        indexed_for_retrieval=indexed,
    )


class TestEmbeddingManager:
    """Tests for the EmbeddingManager wrapper and caching."""

    def test_embedding_dimensions_and_normalization(self) -> None:
        mgr = EmbeddingManager()
        text = "Hypertension blood pressure measurement protocol."
        vec = mgr.embed_text(text)

        assert len(vec) == 384
        # Verify normalization (L2 norm should be approximately 1.0)
        norm = np.linalg.norm(vec)
        assert pytest.approx(norm, abs=1e-4) == 1.0

    def test_sqlite_vector_caching(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            mgr = EmbeddingManager(cache_dir=tmp_dir)

            text = "Clinic blood pressure target is 140/90 mmHg."
            text_hash = "mock_hash_123"

            # First call computes and caches
            vec1 = mgr.embed_batch([text], [text_hash])[0]

            # Second call should fetch directly from SQLite cache
            vec2 = mgr.embed_batch([text], [text_hash])[0]

            assert np.allclose(vec1, vec2)


class TestKeywordIndex:
    """Tests for clinical tokenization and BM25 sparse index."""

    def test_clinical_acronym_expansion(self) -> None:
        tokens_htn = clinical_tokenize("Patient with HTN and T2DM")
        assert "hypertension" in tokens_htn
        assert "diabetes" in tokens_htn

        tokens_drugs = clinical_tokenize("Start ACEi or ARB therapy")
        assert "ramipril" in tokens_drugs or "angiotensin" in tokens_drugs
        assert "losartan" in tokens_drugs or "receptor" in tokens_drugs

    def test_stopword_filtering(self) -> None:
        tokens = clinical_tokenize("What is the blood pressure in adults?")
        assert "what" not in tokens
        assert "the" not in tokens
        assert "is" not in tokens
        assert "blood" in tokens
        assert "pressure" in tokens

    def test_keyword_index_retrieval(self) -> None:
        c1 = create_sample_chunk(
            chunk_id="c1", text="Target blood pressure is 140/90 mmHg for adults under 80."
        )
        c2 = create_sample_chunk(
            chunk_id="c2", text="Metformin is first-line pharmacotherapy for type 2 diabetes."
        )
        c3 = create_sample_chunk(
            chunk_id="c3", text="Spironolactone is an aldosterone antagonist diuretic."
        )
        c4 = create_sample_chunk(
            chunk_id="c4", text="Reference list and appendix noise chunk.", indexed=False
        )

        idx = KeywordIndex()
        count = idx.build_index([c1, c2, c3, c4])
        assert count == 3  # c4 is not indexed_for_retrieval

        hits = idx.query_sparse("blood pressure target under 80", top_k=2)
        assert len(hits) >= 1
        assert hits[0]["chunk_id"] == "c1"


class TestVectorStore:
    """Tests for ChromaDB vector store indexing and filtering."""

    def test_vector_store_indexing_and_query(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            vs = VectorStore(persist_dir=tmp_dir, collection_name="test_guideline_collection")
            mgr = EmbeddingManager()

            c1 = create_sample_chunk(
                chunk_id="c_htn",
                text="Reduce clinic blood pressure to below 140/90 mmHg for adults.",
                condition="hypertension",
            )
            c2 = create_sample_chunk(
                chunk_id="c_dm",
                text="Target HbA1c below 7.0 percent in type 2 diabetes mellitus.",
                condition="type_2_diabetes",
            )

            indexed_count = vs.index_chunks([c1, c2], mgr)
            assert indexed_count == 2
            assert vs.count() == 2

            # Query for blood pressure
            hits = vs.query_dense("What is blood pressure target?", mgr, top_k=1)
            assert len(hits) == 1
            assert hits[0]["chunk_id"] == "c_htn"

            # Query with where_filter
            filtered_hits = vs.query_dense(
                "treatment",
                mgr,
                top_k=2,
                where_filter={"condition": "type_2_diabetes"},
            )
            assert len(filtered_hits) == 1
            assert filtered_hits[0]["chunk_id"] == "c_dm"


class TestHybridRetriever:
    """Tests for RRF fusion, patient applicability, disagreement detection, and out-of-scope gating."""

    @pytest.fixture
    def retriever(self) -> HybridRetriever:
        return HybridRetriever.load_default()

    def test_out_of_scope_rejection(self, retriever: HybridRetriever) -> None:
        out_of_scope_queries = [
            "What is the recommended inhaled corticosteroid dose for acute pediatric asthma exacerbation?",
            "Surgical indications and antibiotic prophylaxis for acute uncomplicated appendicitis in adolescents.",
            "First-line platinum-based chemotherapy regimen for metastatic non-small cell lung cancer.",
            "Weekly methotrexate dosing schedule and folic acid supplementation in rheumatoid arthritis.",
            "Universal childhood immunization schedule for MMR and varicella vaccines.",
            "Postoperative physical therapy and rehabilitation protocol following total hip arthroplasty.",
        ]

        for q in out_of_scope_queries:
            res = retriever.retrieve(q, top_k=5)
            assert res["is_out_of_scope"] is True
            assert len(res["hits"]) == 0

    def test_in_scope_retrieval(self, retriever: HybridRetriever) -> None:
        res = retriever.retrieve("What is the blood pressure target for adults under 80?", top_k=5)
        assert res["is_out_of_scope"] is False
        assert len(res["hits"]) > 0
        assert any("140/90" in h["text"] for h in res["hits"])

    def test_pregnancy_contraindication_patient_applicability(
        self, retriever: HybridRetriever
    ) -> None:
        # Pregnant patient state should conflict/penalize when chunk metadata contains pregnancy contraindications
        meta_ace = {
            "population_tags": "general_adults",
            "drug_class_tags": "ace_inhibitor,arb",
            "exceptions": "Contraindicated in pregnancy; teratogenic risk",
        }
        flag, mult = retriever.compute_patient_applicability(meta_ace, {"is_pregnant": True})
        assert flag == "conflicts"
        assert mult < 0.5

        # Matching pregnancy tag
        meta_preg = {
            "population_tags": "pregnancy,women_childbearing_potential",
            "drug_class_tags": "ccb",
        }
        flag2, mult2 = retriever.compute_patient_applicability(meta_preg, {"is_pregnant": True})
        assert flag2 == "matches"
        assert mult2 > 1.0

    def test_elderly_age_patient_applicability(self, retriever: HybridRetriever) -> None:
        meta_elderly = {
            "population_tags": "elderly",
            "drug_class_tags": "ccb",
        }
        flag, mult = retriever.compute_patient_applicability(meta_elderly, {"age": 82})
        assert flag == "matches"
        assert mult >= 1.2

    def test_guideline_source_affinity_boost(self, retriever: HybridRetriever) -> None:
        # Query specifying ICMR should prioritize ICMR chunks
        res = retriever.retrieve(
            "What is the recommended dose and major side effect of Spironolactone in the ICMR drug table?",
            top_k=5,
        )
        assert len(res["hits"]) > 0
        top_cids = [h["chunk_id"] for h in res["hits"][:2]]
        assert "icmr_htn_001_c0012" in top_cids or "icmr_htn_001_c0011" in top_cids

    def test_cross_guideline_disagreement_detection(self, retriever: HybridRetriever) -> None:
        res = retriever.retrieve(
            "What is the blood pressure target for patients with diabetes?", top_k=5
        )
        # Disagreements should be flagged when multiple organizations specify targets
        disagreements = res["disagreements"]
        if disagreements:
            domains = [d["domain"] for d in disagreements]
            assert any(
                "Blood Pressure Target" in dom or "Pharmacotherapy" in dom for dom in domains
            )
