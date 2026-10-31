"""Unit tests for Phase 1: PDF Extraction, Cleaning, and Recommendation-Aware Chunking.

Verifies:
1. Extraction preserves 1-based page numbers and respects relevant_page_ranges.
2. Cleaning strips running headers, footers, and boilerplate without corrupting clinical text.
3. Chunker satisfies the GuidelineChunk schema with all 22 required metadata fields.
4. 100% of chunks have valid page provenance and non-empty text/hashes.
5. Transcribed flowchart nodes are strictly excluded from retrieval chunks.
6. Clinical entity tagging correctly detects populations and drug classes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from guideline_chatbot.chunking.recommendation_chunker import (
    classify_chunk_type,
    extract_applicability_conditions,
    extract_drug_class_tags,
    extract_evidence_strength,
    extract_exceptions,
    extract_population_tags,
    extract_recommendation_strength,
    resolve_chunk_condition,
)
from guideline_chatbot.chunking.schemas import CHUNK_METADATA_FIELDS
from guideline_chatbot.ingestion.clean import clean_text, normalize_unicode_symbols
from guideline_chatbot.ingestion.extract_pdf import extract_pdf_pages, parse_page_ranges


@pytest.fixture(scope="module")
def project_root() -> Path:
    """Return the absolute path to the capstone root directory."""
    return Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="module")
def processed_chunks(project_root: Path) -> list[dict[str, Any]]:
    """Load the generated guideline chunks from guideline_chunks.json."""
    chunks_path = (
        project_root / "guideline_chatbot" / "data" / "processed" / "guideline_chunks.json"
    )
    assert chunks_path.is_file(), f"guideline_chunks.json does not exist at {chunks_path}"
    with open(chunks_path, encoding="utf-8") as f:
        data: list[dict[str, Any]] = json.load(f)
    return data


# --- 1. Page Range Parsing & PDF Extraction Tests ---


def test_parse_page_ranges() -> None:
    """Verify parse_page_ranges handles various syntax formats correctly."""
    assert parse_page_ranges(None, 10) == list(range(1, 11))
    assert parse_page_ranges("", 5) == list(range(1, 6))
    assert parse_page_ranges("1", 10) == [1]
    assert parse_page_ranges("6-21", 50) == list(range(6, 22))
    assert parse_page_ranges("1-3, 5, 8-10", 20) == [1, 2, 3, 5, 8, 9, 10]
    # Bound to max_pages
    assert parse_page_ranges("8-15", 10) == [8, 9, 10]


def test_extract_pdf_pages_relevant_ranges(project_root: Path) -> None:
    """Verify that multi-condition documents extract strictly within their relevant page ranges."""
    pdf_path = (
        project_root
        / "guideline_chatbot"
        / "data"
        / "raw"
        / "mohfw_stg"
        / "mohfw_stg_endocrinology_diabetes.pdf"
    )
    pages = extract_pdf_pages(pdf_path, "6-21")
    assert len(pages) == 16
    assert pages[0].page_num == 6
    assert pages[-1].page_num == 21
    # Check that page 6 begins with diabetes content
    assert "DIABETES" in pages[0].raw_text.upper()


def test_extract_pdf_pages_single_page(project_root: Path) -> None:
    """Verify single-page STWs extract exactly 1 page with 1-based page_num=1."""
    pdf_path = (
        project_root
        / "guideline_chatbot"
        / "data"
        / "raw"
        / "icmr_stw"
        / "icmr_htn_hypertension_in_adults.pdf"
    )
    pages = extract_pdf_pages(pdf_path, "1")
    assert len(pages) == 1
    assert pages[0].page_num == 1
    assert "HYPERTENSION" in pages[0].raw_text.upper()


# --- 2. Cleaning Module Tests ---


def test_normalize_unicode_symbols() -> None:
    """Verify math symbols and ligatures are safely normalized to standard equivalents."""
    raw = "Target BP \u2265 140/90 mmHg, HbA1c \u2264 7.0%, temp 37\u00b10.5 \u2014 normal."
    norm = normalize_unicode_symbols(raw)
    assert ">= 140/90" in norm
    assert "<= 7.0%" in norm
    assert "+/-0.5" in norm
    assert "- normal" in norm


def test_clean_text_strips_nice_footer() -> None:
    """Verify NICE running footers and copyright disclaimers are cleanly removed."""
    raw = (
        "1.4.20 For adults with hypertension aged under 80, "
        "reduce clinic BP to below 140/90 mmHg.\n"
        "Hypertension in adults: diagnosis and management (NG136)\n"
        "© NICE 2026. All rights reserved. Subject to Notice of rights "
        "(https://www.nice.org.uk/terms-and-conditions#notice-of-rights).\n"
        "Page 15 of 52\n"
    )
    cleaned, stats = clean_text(raw, "test_doc")
    assert "1.4.20 For adults with hypertension" in cleaned
    assert "below 140/90 mmHg" in cleaned
    assert "NICE 2026" not in cleaned
    assert "Page 15 of 52" not in cleaned
    assert stats.chars_removed > 0
    assert stats.lines_removed >= 2


def test_clean_text_preserves_clinical_numbers_and_drugs() -> None:
    """Verify cleaning preserves 100% of dosages, frequencies, and clinical numbers."""
    raw = (
        "Initiate Metformin 500 mg twice daily. If eGFR < 30 ml/min, avoid Metformin. "
        "Target HbA1c < 7.0% (53 mmol/mol). Combine Ramipril 2.5-10 mg with Amlodipine 5 mg."
    )
    cleaned, stats = clean_text(raw, "clinical_test")
    assert "Metformin 500 mg twice daily" in cleaned
    assert "eGFR < 30 ml/min" in cleaned
    assert "Target HbA1c < 7.0%" in cleaned
    assert "53 mmol/mol" in cleaned
    assert "Ramipril 2.5-10 mg" in cleaned
    assert "Amlodipine 5 mg" in cleaned


# --- 3. Tagging & Clinical Classifier Tests ---


def test_extract_population_tags() -> None:
    """Verify detection of specific clinical patient populations."""
    text1 = (
        "In elderly patients aged over 80 years with chronic kidney disease, target BP < 150/90."
    )
    tags1 = extract_population_tags(text1)
    assert "elderly" in tags1
    assert "chronic_kidney_disease" in tags1

    text2 = "In pregnant women with gestational hypertension, avoid ACE inhibitors."
    tags2 = extract_population_tags(text2)
    assert "pregnancy" in tags2

    text3 = "For people of Black African or African-Caribbean family origin, start with CCB."
    tags3 = extract_population_tags(text3)
    assert "african_caribbean" in tags3


def test_extract_drug_class_tags() -> None:
    """Verify pharmacological entity extraction across drug classes."""
    text = (
        "Offer an ACE inhibitor (e.g. Ramipril) or ARB (e.g. Losartan). "
        "Add a CCB (e.g. Amlodipine) or Thiazide diuretic (e.g. Indapamide). "
        "In diabetes, add Metformin and an SGLT2 inhibitor (e.g. Dapagliflozin)."
    )
    tags = extract_drug_class_tags(text)
    assert "ace_inhibitor" in tags
    assert "arb" in tags
    assert "ccb" in tags
    assert "thiazide" in tags
    assert "metformin" in tags
    assert "sglt2_inhibitor" in tags


def test_extract_evidence_and_recommendation_strength() -> None:
    """Verify extraction of GRADE evidence certainty and recommendation strength."""
    text = (
        "WHO recommends dual combination therapy as initial treatment. "
        "Strong recommendation, moderate-certainty evidence."
    )
    assert extract_evidence_strength(text) == "Moderate certainty"
    assert extract_recommendation_strength(text) == "Strong recommendation"


def test_extract_applicability_and_exceptions() -> None:
    """Verify extraction of conditional applicability clauses and contraindications."""
    text = (
        "For adults with confirmed hypertension and clinic BP >= 140/90 mmHg, "
        "initiate drug treatment. Avoid if creatinine clearance is less than 30 ml/min. "
        "Do not offer an ACE inhibitor in combination with an ARB."
    )
    conds = extract_applicability_conditions(text)
    assert len(conds) >= 1
    assert any("clinic BP >= 140/90" in c for c in conds)

    exc = extract_exceptions(text)
    assert len(exc) >= 1
    assert any("Avoid if creatinine clearance" in e or "Do not offer" in e for e in exc)


def test_classify_chunk_type() -> None:
    """Verify classification of chunk types."""
    assert (
        classify_chunk_type("Table content\n| a | b |\n|---|---|\n| 1 | 2 |", "Table 1") == "table"
    )
    assert (
        classify_chunk_type(
            "Criteria for diagnosis of diabetes include FPG >= 126.", "Diagnostic Criteria"
        )
        == "definition"
    )
    assert (
        classify_chunk_type("Recheck blood pressure every 3 months until controlled.", "Monitoring")
        == "monitoring"
    )
    assert (
        classify_chunk_type("Offer amlodipine 5 mg once daily as initial treatment.", "Treatment")
        == "recommendation"
    )
    assert (
        classify_chunk_type(
            "The trial evaluated cardiovascular mortality across groups.", "Rationale"
        )
        == "rationale"
    )


def test_resolve_chunk_condition() -> None:
    """Verify multi-condition cross-tagging."""
    assert (
        resolve_chunk_condition("hypertension", "Target blood pressure in adults") == "hypertension"
    )
    assert (
        resolve_chunk_condition("hypertension", "Target BP in diabetic patients is < 130/80")
        == "both"
    )
    assert (
        resolve_chunk_condition("type_2_diabetes", "Metformin titration in diabetes")
        == "type_2_diabetes"
    )
    assert (
        resolve_chunk_condition("type_2_diabetes", "Hypertension management in diabetic patients")
        == "both"
    )


# --- 4. Dataset Integrity & Quality Gate Tests ---


def test_all_chunks_have_all_22_fields(processed_chunks: list[dict]) -> None:
    """Verify that 100% of chunks contain all 22 required metadata fields."""
    assert len(processed_chunks) > 500, f"Expected > 500 chunks, got {len(processed_chunks)}"
    for idx, c in enumerate(processed_chunks):
        for field in CHUNK_METADATA_FIELDS:
            assert field in c, f"Chunk {idx} ({c.get('chunk_id')}) missing field '{field}'"
            if field in [
                "chunk_id",
                "doc_id",
                "document_name",
                "condition",
                "section_path",
                "heading",
                "text",
                "text_hash",
            ]:
                assert c[field] is not None and str(c[field]).strip(), (
                    f"Chunk {idx} ({c.get('chunk_id')}) has empty mandatory field '{field}'"
                )


def test_page_provenance_and_validity(processed_chunks: list[dict]) -> None:
    """Verify that every chunk has valid 1-based page provenance (page_start <= page_end)."""
    for c in processed_chunks:
        assert isinstance(c["page_start"], int) and c["page_start"] >= 1
        assert isinstance(c["page_end"], int) and c["page_end"] >= 1
        assert c["page_start"] <= c["page_end"], (
            f"Chunk {c['chunk_id']} has invalid page range: {c['page_start']} > {c['page_end']}"
        )


def test_flowcharts_excluded_from_retrieval_chunks(processed_chunks: list[dict]) -> None:
    """Verify that unverified flowchart nodes are strictly excluded from the chunk dataset."""
    for c in processed_chunks:
        assert not c["chunk_id"].startswith("fc_"), (
            f"Unverified flowchart node {c['chunk_id']} found in processed chunks!"
        )
        assert c["chunk_type"] != "flowchart", (
            f"Chunk {c['chunk_id']} has unverified chunk_type 'flowchart'!"
        )


def test_word_length_distribution(processed_chunks: list[dict]) -> None:
    """Verify chunk sizes adhere to clinical recommendation boundaries without runaway lengths."""
    for c in processed_chunks:
        words = len(c["text"].split())
        assert words >= 5, f"Chunk {c['chunk_id']} too short ({words} words)"
        assert words <= 650, f"Chunk {c['chunk_id']} too long ({words} words)"


def test_nine_documents_represented(processed_chunks: list[dict]) -> None:
    """Verify that all 9 guideline documents from the inventory have generated chunks."""
    doc_ids = {c["doc_id"] for c in processed_chunks}
    expected_docs = {
        "who_htn_001",
        "who_t2dm_001",
        "icmr_htn_001",
        "icmr_t2dm_001",
        "nice_htn_001",
        "nice_t2dm_001",
        "mohfw_htn_001",
        "mohfw_htn_002",
        "mohfw_t2dm_001",
    }
    assert doc_ids == expected_docs, f"Missing document chunks: {expected_docs - doc_ids}"
