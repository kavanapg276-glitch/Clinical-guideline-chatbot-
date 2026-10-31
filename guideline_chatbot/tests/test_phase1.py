"""Unit tests for Phase 1 & Phase 1b: PDF Extraction, Cleaning, and Recommendation-Aware Chunking.

Verifies:
1. Extraction preserves 1-based page numbers and respects relevant_page_ranges.
2. Cleaning strips running headers, footers, and boilerplate without corrupting clinical text.
3. Chunker satisfies the GuidelineChunk schema with all 26 required metadata fields.
4. 100% of chunks have valid page provenance and non-empty text/hashes.
5. Transcribed flowchart nodes and noise chunks are excluded from retrieval indexing.
6. Clinical entity tagging correctly detects populations, separate T1/T2 tags, and drug classes.
7. Automated numeric preservation check across critical thresholds and doses.
8. Ten clinical trap verifications.
9. ICMR poster drug table row-by-row and T2DM strata preservation.
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
    parse_recommendation_year,
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
    cleaned, _ = clean_text(raw, "clinical_test")
    assert "Metformin 500 mg twice daily" in cleaned
    assert "eGFR < 30 ml/min" in cleaned
    assert "Target HbA1c < 7.0%" in cleaned
    assert "53 mmol/mol" in cleaned
    assert "Ramipril 2.5-10 mg" in cleaned
    assert "Amlodipine 5 mg" in cleaned


# --- 3. Tagging & Clinical Classifier Tests ---


def test_extract_population_tags_applicability_and_negation() -> None:
    """Verify population tags enforce applicability over mere mention and handle negations."""
    # Negation: "without renal disease" must NOT tag chronic_kidney_disease
    text_negation = (
        "Measure blood pressure at least annually in an adult with type 2 diabetes without "
        "previously diagnosed hypertension or renal disease."
    )
    tags_neg = extract_population_tags(text_negation)
    assert "type_2_diabetes" in tags_neg
    assert "chronic_kidney_disease" not in tags_neg

    # Routine lab screening: HbA1c mentioned in general hypertension workup must NOT tag T2DM
    text_screening = (
        "For all people with hypertension offer to: test for the presence of protein in the urine... "
        "take a blood sample to measure glycated haemoglobin (HbA1C), electrolytes, creatinine."
    )
    tags_screen = extract_population_tags(text_screening)
    assert "type_2_diabetes" not in tags_screen

    # Type 1 vs Type 2 diabetes disambiguation
    text_t1dm = (
        "See also table 1 for guidance on clinic blood pressure targets for people aged under 80 "
        "with type 1 diabetes or severe chronic kidney disease."
    )
    tags_t1 = extract_population_tags(text_t1dm)
    assert "type_1_diabetes" in tags_t1
    assert "type_2_diabetes" not in tags_t1

    # Adverse drug effect mention must NOT tag T2DM
    text_ae = (
        "The common side effects of diuretics are metabolic side effects like "
        "hypokalemia, hyperglycemia but which are less frequent when used in doses of 12.5 mg."
    )
    tags_ae = extract_population_tags(text_ae)
    assert "type_2_diabetes" not in tags_ae


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
    assert conds is not None
    assert any("clinic BP >= 140/90" in c for c in conds)

    exc = extract_exceptions(text)
    assert exc is not None
    assert any("Avoid if creatinine clearance" in e or "Do not offer" in e for e in exc)


def test_parse_recommendation_year() -> None:
    """Verify parsing of NICE bracketed year tags."""
    assert parse_recommendation_year("Recommend lifestyle advice. [2009]") == "2009"
    assert (
        parse_recommendation_year("Reduce clinic BP to below 140/90. [2019, amended 2022]")
        == "2022"
    )
    assert (
        parse_recommendation_year("Stop GLP-1 receptor agonists if targets not reached. [2026]")
        == "2026"
    )
    assert parse_recommendation_year("Unversioned recommendation text.") is None


def test_classify_chunk_type() -> None:
    """Verify classification of chunk types and retrieval indexability flags."""
    c_tab, idx_tab = classify_chunk_type(
        "Table content\n| a | b |\n|---|---|\n| 1 | 2 |", "Table 1"
    )
    assert c_tab == "table" and idx_tab is True

    c_def, idx_def = classify_chunk_type(
        "Criteria for diagnosis of diabetes include FPG >= 126.", "Diagnostic Criteria"
    )
    assert c_def == "definition" and idx_def is True

    c_rec, idx_rec = classify_chunk_type("1.4.20 For adults with hypertension", "1.4.20")
    assert c_rec == "recommendation" and idx_rec is True

    c_ref, idx_ref = classify_chunk_type(
        "1. Mancia G. 2023 ESH Guidelines. doi: 10.1097/...", "References"
    )
    assert c_ref == "reference" and idx_ref is False

    c_fm, idx_fm = classify_chunk_type(
        "ACEi: Angiotensin-converting enzyme inhibitor", "Abbreviations"
    )
    assert c_fm == "front_matter" and idx_fm is False


def test_resolve_chunk_condition() -> None:
    """Verify multi-condition scoping (both only when both conditions are governed)."""
    assert (
        resolve_chunk_condition("hypertension", "Target blood pressure in adults") == "hypertension"
    )
    assert (
        resolve_chunk_condition("hypertension", "Target BP in diabetic patients is < 140/90")
        == "both"
    )
    assert (
        resolve_chunk_condition("type_2_diabetes", "Metformin titration in diabetes")
        == "type_2_diabetes"
    )
    assert (
        resolve_chunk_condition("type_2_diabetes", "Target BP = 140/90 in diabetic patients")
        == "both"
    )


# --- 4. Dataset Integrity & Quality Gate Tests ---


def test_all_chunks_have_all_26_fields(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify that 100% of chunks contain all 26 required metadata fields."""
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


def test_page_provenance_and_validity(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify that every chunk has valid 1-based page provenance (page_start <= page_end)."""
    for c in processed_chunks:
        assert isinstance(c["page_start"], int) and c["page_start"] >= 1
        assert isinstance(c["page_end"], int) and c["page_end"] >= 1
        assert c["page_start"] <= c["page_end"], (
            f"Chunk {c['chunk_id']} has invalid page range: {c['page_start']} > {c['page_end']}"
        )


def test_flowcharts_and_noise_indexability(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify that unverified flowchart nodes and noise chunks are not indexed for retrieval."""
    for c in processed_chunks:
        assert not c["chunk_id"].startswith("fc_"), (
            f"Unverified flowchart node {c['chunk_id']} found in processed chunks!"
        )
        if c["chunk_type"] in ["reference", "methods", "front_matter", "contributors"]:
            assert c["indexed_for_retrieval"] is False, (
                f"Noise chunk {c['chunk_id']} of type {c['chunk_type']} was marked indexable!"
            )


def test_word_length_distribution(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify chunk sizes adhere to clinical recommendation boundaries without runaway lengths."""
    for c in processed_chunks:
        words = len(c["text"].split())
        assert words >= 20, f"Chunk {c['chunk_id']} too short ({words} words)"
        assert words <= 650, f"Chunk {c['chunk_id']} too long ({words} words)"


def test_nine_documents_represented(processed_chunks: list[dict[str, Any]]) -> None:
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


# --- 5. Phase 1b Numeric Preservation & Trap Tests ---


def test_numeric_preservation(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify critical clinical thresholds, blood pressures, and doses are preserved in chunk text."""
    corpus_text = " ".join(c["text"] for c in processed_chunks).lower()

    critical_tokens = [
        "140/90",
        "130/80",
        "135/85",
        "150/90",
        "160/100",
        "180/120",
        "2.5 mg",
        "5 mg",
        "10 mg",
        "12.5 mg",
        "20 mg",
        "25 mg",
        "40 mg",
        "50 mg",
        "80 mg",
        "100 mg",
        "400 mg",
        "500 mg",
        "1000 mg",
        "2000 mg",
        "6.5%",
        "7.0%",
        "8.5%",
        "48 mmol/mol",
        "53 mmol/mol",
        "30 ml/min",
        "23 kg/m2",
    ]

    for tok in critical_tokens:
        clean_tok = tok.lower()
        variants = [clean_tok, clean_tok.replace(" ", "")]
        assert any(v in corpus_text for v in variants), (
            f"Critical numeric token '{tok}' missing from chunks!"
        )


def test_icmr_drug_table_and_strata_preservation(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify complete row-wise preservation of ICMR antihypertensive table and T2DM strata."""
    c_htn = next(c for c in processed_chunks if c["chunk_id"] == "icmr_htn_001_c0012")
    c_t2dm = next(c for c in processed_chunks if c["chunk_id"] == "icmr_t2dm_001_c0008")

    assert c_htn["chunk_type"] == "table"
    assert c_t2dm["chunk_type"] == "table"

    # Verify all 13 drugs appear in the HTN table chunk
    drugs = [
        "Amlodipine",
        "Enalapril",
        "Ramipril",
        "Losartan",
        "Olmesartan",
        "Telmisartan",
        "Chlorthalidone",
        "Hydrochlorothiazide",
        "Carvedilol",
        "Labetalol",
        "Metoprolol",
        "Nebivolol",
        "Spironolactone",
    ]
    for d in drugs:
        assert d in c_htn["text"], f"Drug '{d}' missing from ICMR HTN table chunk!"

    # Verify all 3 HbA1c strata appear in the T2DM table chunk
    assert "HbA1c < 8.5%" in c_t2dm["text"]
    assert "HbA1c 8.5%" in c_t2dm["text"]
    assert "HbA1c > 10.0%" in c_t2dm["text"]


def test_ten_clinical_traps(processed_chunks: list[dict[str, Any]]) -> None:
    """Verify all 10 clinical trap assertions specified in Gate 1 defect remediation."""
    # Trap 1: NICE 1.4.20 tags type_1_diabetes, NOT type_2_diabetes
    c1 = next(
        c
        for c in processed_chunks
        if c["text"].strip().startswith("1.4.20") and c["doc_id"] == "nice_htn_001"
    )
    assert "type_1_diabetes" in c1["population_tags"]
    assert "type_2_diabetes" not in c1["population_tags"]

    # Trap 2: NICE 1.2.12 negates chronic_kidney_disease
    c2 = next(
        c
        for c in processed_chunks
        if c["text"].strip().startswith("1.2.12") and c["doc_id"] == "nice_htn_001"
    )
    assert "type_2_diabetes" in c2["population_tags"]
    assert "chronic_kidney_disease" not in c2["population_tags"]

    # Trap 3: NICE 1.3.3 does NOT tag type_2_diabetes
    c3 = next(
        c
        for c in processed_chunks
        if c["text"].strip().startswith("1.3.3") and c["doc_id"] == "nice_htn_001"
    )
    assert "type_2_diabetes" not in c3["population_tags"]

    # Trap 4: MoHFW 5.3.2 does NOT tag type_2_diabetes
    c4 = next(c for c in processed_chunks if "5.3.2" in c["text"] and "hypokalemia" in c["text"])
    assert "type_2_diabetes" not in c4["population_tags"]

    # Trap 5: ICMR HTN table tags pregnancy and records contraindication
    c5 = next(c for c in processed_chunks if c["chunk_id"] == "icmr_htn_001_c0012")
    assert "pregnancy" in c5["population_tags"]
    assert any("Pregnancy" in e for e in (c5["exceptions"] or []))

    # Trap 6: NICE 1.4.21 age-80 target <150/90 mmHg
    c6 = next(
        c
        for c in processed_chunks
        if c["text"].strip().startswith("1.4.21") and c["doc_id"] == "nice_htn_001"
    )
    assert "150/90" in c6["text"]
    assert "elderly" in c6["population_tags"]

    # Trap 7: WHO Recommendation 6 target <140/90 mmHg
    c7 = next(
        c
        for c in processed_chunks
        if c["doc_id"] == "who_htn_001"
        and "RECOMMENDATION ON TARGET BLOOD PRESSURE" in c["heading"]
    )
    assert "<140/90" in c7["text"]

    # Trap 8: ICMR HTN age-80 target <150/90 mmHg
    c8 = next(
        c
        for c in processed_chunks
        if c["doc_id"] == "icmr_htn_001" and "CONTROL TARGETS" in c["text"]
    )
    assert "150" in c8["text"]
    assert "elderly" in c8["population_tags"]

    # Trap 9: MoHFW diabetes target <140/90 mmHg
    c9 = next(
        c for c in processed_chunks if "4.8.1.1" in c["text"] and c["doc_id"] == "mohfw_htn_001"
    )
    assert "140 mm Hg" in c9["text"]
    assert "90 mm Hg" in c9["text"]

    # Trap 10: Trailing section header not glued to NICE 1.2.12
    assert "Specialist investigations" not in c2["text"]
