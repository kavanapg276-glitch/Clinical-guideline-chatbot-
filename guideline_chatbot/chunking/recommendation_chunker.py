"""Recommendation-aware chunker for clinical guidelines.

Segments cleaned guideline texts along clinical recommendation and section boundaries,
preserving the recommendation statement together with its conditional logic, applicability
criteria, exceptions, and evidence strength. Generates GuidelineChunk objects with all 22
required metadata fields.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any

from guideline_chatbot.chunking.schemas import ChunkType, GuidelineChunk
from guideline_chatbot.ingestion.clean import clean_text
from guideline_chatbot.ingestion.extract_pdf import ExtractedPage, extract_pdf_pages

logger = logging.getLogger(__name__)

# Clinical population patterns
POPULATION_PATTERNS: dict[str, re.Pattern[str]] = {
    "elderly": re.compile(
        r"\b(?:elderly|older\s+adults?|aged?\s*(?:>=|>|over)?\s*80|>=?\s*80\s*years?|"
        r">=?\s*65\s*years?|octogenarians?|frail(?:\s+elderly)?)\b",
        re.IGNORECASE,
    ),
    "chronic_kidney_disease": re.compile(
        r"\b(?:ckd|chronic\s+kidney\s+disease|renal\s+(?:impairment|failure|insufficiency|disease)|"
        r"egfr|creatinine\s+clearance|crcl|proteinuria|microalbuminuria|macroalbuminuria|"
        r"diabetic\s+nephropathy|albuminuria|acr\s*(?:>=|>)?\s*\d+)\b",
        re.IGNORECASE,
    ),
    "type_2_diabetes": re.compile(
        r"\b(?:type\s*2\s+diabetes|t2dm|diabetes\s+mellitus|diabetic(?:\s+patients?)?|"
        r"hba1c|hyperglycaemia|hyperglycemia)\b",
        re.IGNORECASE,
    ),
    "pregnancy": re.compile(
        r"\b(?:pregnan(?:cy|t)|pre-?eclampsia|gestational(?:\s+diabetes)?|lactat(?:ing|ion)|"
        r"breastfeeding|antenatal|maternal)\b",
        re.IGNORECASE,
    ),
    "cardiovascular_disease": re.compile(
        r"\b(?:cardiovascular\s+disease|ascvd|cvd|coronary(?:\s+artery\s+disease)?|cad|"
        r"heart\s+failure|chf|myocardial\s+infarction|stroke|tia|transient\s+ischaemic\s+attack|"
        r"angina|peripheral\s+artery\s+disease)\b",
        re.IGNORECASE,
    ),
    "african_caribbean": re.compile(
        r"\b(?:black\s+african|african-caribbean|african\s+or\s+caribbean|afro-caribbean|"
        r"black\s+people\s+of\s+african|african\s+family\s+origin)\b",
        re.IGNORECASE,
    ),
    "young_adults": re.compile(
        r"\b(?:young(?:er)?\s+adults?|aged?\s*<\s*40|under\s+40|aged?\s*<\s*55|under\s+55)\b",
        re.IGNORECASE,
    ),
}

# Pharmacological drug class patterns
DRUG_CLASS_PATTERNS: dict[str, re.Pattern[str]] = {
    "ace_inhibitor": re.compile(
        r"\b(?:ace\s+inhibitors?|acei|angiotensin-converting\s+enzyme|"
        r"ramipril|lisinopril|enalapril|perindopril|captopril|benazepril|fosinopril)\b",
        re.IGNORECASE,
    ),
    "arb": re.compile(
        r"\b(?:angiotensin\s+receptor\s+blockers?|arb|angiotensin\s+ii\s+receptor\s+blockers?|"
        r"losartan|telmisartan|valsartan|candesartan|olmesartan|irbesartan)\b",
        re.IGNORECASE,
    ),
    "ccb": re.compile(
        r"\b(?:calcium\s+channel\s+blockers?|ccb|dihydropyridine(?:\s+ccb)?|"
        r"amlodipine|nifedipine|felodipine|diltiazem|verapamil|lercanidipine)\b",
        re.IGNORECASE,
    ),
    "thiazide": re.compile(
        r"\b(?:thiazides?|thiazide-like(?:\s+diuretics?)?|diuretics?|"
        r"chlorthalidone|indapamide|hydrochlorothiazide|hctz)\b",
        re.IGNORECASE,
    ),
    "metformin": re.compile(
        r"\b(?:metformin|biguanides?)\b",
        re.IGNORECASE,
    ),
    "sglt2_inhibitor": re.compile(
        r"\b(?:sglt-?2(?:\s+inhibitors?)?|sglt2-?i|"
        r"dapagliflozin|empagliflozin|canagliflozin|ertugliflozin)\b",
        re.IGNORECASE,
    ),
    "sulfonylurea": re.compile(
        r"\b(?:sulfonylureas?|sulphonylureas?|"
        r"glimepiride|gliclazide|glipizide|glibenclamide|glyburide)\b",
        re.IGNORECASE,
    ),
    "dpp4_inhibitor": re.compile(
        r"\b(?:dpp-?4(?:\s+inhibitors?)?|gliptins?|"
        r"sitagliptin|linagliptin|vildagliptin|saxagliptin|alogliptin)\b",
        re.IGNORECASE,
    ),
    "glp1_ra": re.compile(
        r"\b(?:glp-?1(?:\s+receptor\s+agonists?)?|glp-?1\s*ra|"
        r"semaglutide|liraglutide|dulaglutide|exenatide)\b",
        re.IGNORECASE,
    ),
    "beta_blocker": re.compile(
        r"\b(?:beta-?blockers?|beta-adrenoceptor\s+blockers?|"
        r"atenolol|metoprolol|bisoprolol|carvedilol|labetalol|nebivolol|propranolol)\b",
        re.IGNORECASE,
    ),
    "mra_spironolactone": re.compile(
        r"\b(?:spironolactone|eplerenone|mineralocorticoid\s+receptor\s+antagonists?|mra)\b",
        re.IGNORECASE,
    ),
    "alpha_blocker": re.compile(
        r"\b(?:alpha-?blockers?|doxazosin|prazosin|terazosin)\b",
        re.IGNORECASE,
    ),
    "insulin": re.compile(
        r"\b(?:insulins?|basal\s+insulin|nph\s+insulin|glargine|degludec|detemir|regular\s+insulin)\b",
        re.IGNORECASE,
    ),
    "statin": re.compile(
        r"\b(?:statins?|atorvastatin|rosuvastatin|simvastatin|pravastatin|lipid-lowering)\b",
        re.IGNORECASE,
    ),
    "antiplatelet": re.compile(
        r"\b(?:aspirin|clopidogrel|antiplatelets?)\b",
        re.IGNORECASE,
    ),
}

# Evidence and recommendation strength patterns
EVIDENCE_STRENGTH_PATTERNS = [
    (re.compile(r"\bhigh[- ]certainty(?:\s+evidence)?\b", re.I), "High certainty"),
    (re.compile(r"\bmoderate[- ]certainty(?:\s+evidence)?\b", re.I), "Moderate certainty"),
    (re.compile(r"\blow[- ]certainty(?:\s+evidence)?\b", re.I), "Low certainty"),
    (re.compile(r"\bvery\s+low[- ]certainty(?:\s+evidence)?\b", re.I), "Very low certainty"),
    (re.compile(r"\bhigh[- ]quality\s+evidence\b", re.I), "High quality"),
    (re.compile(r"\bmoderate[- ]quality\s+evidence\b", re.I), "Moderate quality"),
    (re.compile(r"\blow[- ]quality\s+evidence\b", re.I), "Low quality"),
    (re.compile(r"\bexpert\s+opinions?\b", re.I), "Expert opinion"),
    (re.compile(r"\bexpert\s+consensus\b", re.I), "Expert consensus"),
]

RECOMMENDATION_STRENGTH_PATTERNS = [
    (re.compile(r"\bstrong\s+recommendations?\b", re.I), "Strong recommendation"),
    (re.compile(r"\bconditional\s+recommendations?\b", re.I), "Conditional recommendation"),
    (re.compile(r"\bgood\s+practice\s+points?\b", re.I), "Good practice point"),
    (re.compile(r"\bclinical\s+practice\s+advice\b", re.I), "Clinical practice advice"),
]


def extract_population_tags(text: str) -> list[str]:
    """Extract matching patient population tags from text."""
    tags: list[str] = []
    for tag_name, pattern in POPULATION_PATTERNS.items():
        if pattern.search(text):
            tags.append(tag_name)
    return sorted(tags)


def extract_drug_class_tags(text: str) -> list[str]:
    """Extract matching pharmacological drug class tags from text."""
    tags: list[str] = []
    for tag_name, pattern in DRUG_CLASS_PATTERNS.items():
        if pattern.search(text):
            tags.append(tag_name)
    return sorted(tags)


def extract_evidence_strength(text: str) -> str | None:
    """Extract explicit evidence certainty or rating from text."""
    for pattern, label in EVIDENCE_STRENGTH_PATTERNS:
        if pattern.search(text):
            return label
    return None


def extract_recommendation_strength(text: str) -> str | None:
    """Extract explicit recommendation strength from text."""
    for pattern, label in RECOMMENDATION_STRENGTH_PATTERNS:
        if pattern.search(text):
            return label
    return None


def extract_applicability_conditions(text: str) -> list[str]:
    """Extract applicability condition statements (IF / WHEN clauses)."""
    conditions: list[str] = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for s in sentences:
        s_clean = s.strip()
        if (
            re.search(
                r"\b(?:if|when|for\s+(?:adults|people|patients)\s+(?:with|aged)|in\s+adults\s+with|"
                r"where\s+clinic\s+bp\s+is|with\s+confirmed\s+hypertension|in\s+individuals\s+with)\b",
                s_clean,
                re.IGNORECASE,
            )
            and 20 < len(s_clean) < 300
        ):
            conditions.append(s_clean)
    return conditions[:5]


def extract_exceptions(text: str) -> list[str]:
    """Extract exceptions, contraindications, or exclusions."""
    exceptions: list[str] = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for s in sentences:
        s_clean = s.strip()
        if (
            re.search(
                r"\b(?:avoid(?:\s+if|\s+in)?|do\s+not\s+(?:offer|prescribe|combine)|contraindicated|"
                r"caution(?:\s+in)?|discontinue\s+if|except\s+(?:in|for)|not\s+recommended)\b",
                s_clean,
                re.IGNORECASE,
            )
            and 15 < len(s_clean) < 300
        ):
            exceptions.append(s_clean)
    return exceptions[:5]


def classify_chunk_type(text: str, heading: str) -> ChunkType:
    """Determine the chunk type based on text content and heading."""
    text_lower = text.lower()
    heading_lower = heading.lower()

    if "|" in text and "---" in text:
        return "table"

    if any(
        k in heading_lower
        for k in [
            "definition",
            "classification",
            "cutoffs",
            "diagnostic criteria",
            "criteria for diagnosis",
        ]
    ):
        return "definition"

    if any(
        k in heading_lower or k in text_lower
        for k in ["monitoring", "follow-up", "follow up", "frequency of re-assessment", "recheck"]
    ):
        return "monitoring"

    if any(
        k in heading_lower
        for k in [
            "recommendation",
            "algorithm",
            "treatment",
            "pharmacotherapy",
            "management",
            "stepwise",
        ]
    ):
        return "recommendation"

    if any(
        k in text_lower
        for k in [
            "we recommend",
            "who recommends",
            "offer ",
            "start with",
            "initial treatment",
            "prescribe",
            "titrate",
            "target blood pressure",
            "target clinic",
            "first-line",
            "second-line",
        ]
    ):
        return "recommendation"

    if any(
        k in heading_lower or k in text_lower
        for k in ["rationale", "evidence and rationale", "remarks", "background", "epidemiology"]
    ):
        return "rationale"

    return "other"


def resolve_chunk_condition(doc_condition: str, text: str) -> str:
    """Determine chunk condition ('hypertension', 'type_2_diabetes', or 'both')."""
    has_htn = bool(re.search(r"\b(?:hypertension|blood\s+pressure|sbp|dbp)\b", text, re.I))
    has_dm = bool(re.search(r"\b(?:diabetes|diabetic|t2dm|hba1c|glucose)\b", text, re.I))

    if doc_condition == "hypertension" and has_dm:
        return "both"
    if doc_condition == "type_2_diabetes" and has_htn:
        return "both"
    return doc_condition


def is_boundary_line(line: str) -> tuple[bool, str]:
    """Determine if a line marks a section or recommendation boundary.

    Returns:
        Tuple of (is_boundary, detected_heading_or_empty).
    """
    stripped = line.strip()
    if not stripped:
        return False, ""

    # NICE recommendation number at start of line: e.g. 1.1.1, 1.4.20
    if re.match(r"^\d+\.\d+\.\d+\b", stripped):
        return True, stripped

    # NICE / WHO numbered section heading: e.g. 1.4 Treating and monitoring...
    if re.match(r"^\d+\.\d+\s+[A-Z]", stripped):
        return True, stripped

    # WHO recommendation title: e.g. 1. RECOMMENDATION ON..., Recommendation 1
    if re.match(r"^(?:\d+\.\s+)?RECOMMENDATION\s+(?:ON|[0-9]+)\b", stripped, re.I):
        return True, stripped
    if re.match(
        r"^(?:Rationale\s+and\s+remarks|Evidence\s+and\s+rationale|Remarks)\b", stripped, re.I
    ):
        return True, stripped

    # Markdown headers: e.g. # Title, ## Subheading
    if stripped.startswith("#"):
        clean_h = stripped.lstrip("#").strip()
        if clean_h:
            return True, clean_h
        return False, ""

    # ICMR / MoHFW uppercase section headers: e.g. DIAGNOSIS OF HYPERTENSION, PHARMACOTHERAPY
    if (
        stripped.isupper()
        and 4 <= len(stripped) <= 50
        and not stripped.endswith(",")
        and not stripped.startswith("ICD-")
    ):
        return True, stripped

    # MoHFW / STG numbered sections: e.g. 4.2 Pharmacotherapy, 4. Management of Hypertension
    if re.match(r"^[1-9]\d?(?:\.\d+)?\s+[A-Z][a-zA-Z\s]{3,45}$", stripped):
        return True, stripped

    return False, ""


def has_clinical_content(text: str) -> bool:
    """Check if a text block contains substantive clinical guidance."""
    words = text.split()
    if len(words) >= 20:
        return True
    # Clinical imperative verbs and keywords
    clinical_keywords = [
        "recommend",
        "offer",
        "prescribe",
        "initiate",
        "target",
        "titrate",
        "reduce",
        "avoid",
        "contraindicated",
        "caution",
        "measure",
        "diagnose",
        "treat",
        "lifestyle",
        "first-line",
        "second-line",
        "blood pressure",
        "mmhg",
        "hba1c",
        "mg",
        "twice daily",
        "once daily",
        "thiazide",
        "metformin",
    ]
    text_lower = text.lower()
    return any(k in text_lower for k in clinical_keywords) and len(words) >= 8


def split_long_lines(
    lines: list[tuple[str, int]], max_words: int = 350
) -> list[list[tuple[str, int]]]:
    """Split a sequence of lines into cohesive segments bounded by max_words.

    Breaks at sentence ends ('.', '?', ':', ';') or blank lines to preserve sentence integrity.
    """
    batches: list[list[tuple[str, int]]] = []
    current_batch: list[tuple[str, int]] = []
    current_words = 0

    for item in lines:
        line_str = item[0].strip()
        w_count = len(line_str.split())

        if (
            current_words + w_count > max_words
            and current_batch
            and (line_str.endswith((".", "?", ":", ";")) or not line_str or current_words > 450)
        ):
            current_batch.append(item)
            batches.append(current_batch)
            current_batch = []
            current_words = 0
            continue

        current_batch.append(item)
        current_words += w_count

    if current_batch:
        batches.append(current_batch)

    return batches


class GuidelineChunker:
    """Recommendation-aware chunker for clinical guidelines."""

    def __init__(self, target_word_min: int = 40, target_word_max: int = 450):
        self.target_word_min = target_word_min
        self.target_word_max = target_word_max

    def chunk_document(
        self,
        doc_metadata: dict[str, Any],
        extracted_pages: list[ExtractedPage],
    ) -> list[GuidelineChunk]:
        """Chunk a document into GuidelineChunk objects preserving page spans and metadata.

        Args:
            doc_metadata: Document catalog metadata dictionary.
            extracted_pages: List of ExtractedPage objects for the document.

        Returns:
            List of GuidelineChunk objects.
        """
        doc_id = str(doc_metadata.get("doc_id", ""))
        doc_name = str(doc_metadata.get("document_name", ""))
        issuer = str(doc_metadata.get("issuing_organization", ""))
        doc_condition = str(doc_metadata.get("condition", ""))
        version = doc_metadata.get("version")
        pub_date = doc_metadata.get("publication_date")
        jurisdiction = str(doc_metadata.get("jurisdiction", "unknown"))
        doc_status = str(doc_metadata.get("document_status", "current"))

        chunks: list[GuidelineChunk] = []
        chunk_idx = 1

        # Collect all extracted tables across pages first
        for page in extracted_pages:
            for t_idx, table in enumerate(page.tables):
                if table.markdown.strip():
                    t_heading = f"Table (Page {page.page_num}, #{t_idx + 1})"
                    t_text = f"### {t_heading}\n\n{table.markdown.strip()}"
                    t_pop_tags = extract_population_tags(t_text)
                    t_drug_tags = extract_drug_class_tags(t_text)
                    t_cond = resolve_chunk_condition(doc_condition, t_text)
                    t_hash = hashlib.sha256(t_text.encode("utf-8")).hexdigest()

                    chunk_id = f"{doc_id}_c{chunk_idx:04d}"
                    chunk_idx += 1

                    chunks.append(
                        GuidelineChunk(
                            chunk_id=chunk_id,
                            doc_id=doc_id,
                            document_name=doc_name,
                            issuing_organization=issuer,
                            condition=t_cond,
                            section_path=f"{doc_name} > Tables > {t_heading}",
                            heading=t_heading,
                            page_start=page.page_num,
                            page_end=page.page_num,
                            version=version,
                            publication_date=pub_date,
                            jurisdiction=jurisdiction,
                            document_status=doc_status,
                            chunk_type="table",
                            evidence_strength=None,
                            recommendation_strength=None,
                            population_tags=t_pop_tags,
                            drug_class_tags=t_drug_tags,
                            applicability_conditions=[],
                            exceptions=[],
                            text=t_text,
                            text_hash=t_hash,
                        )
                    )

        # Build document-wide sequence of (line_text, page_num)
        doc_lines: list[tuple[str, int]] = []
        for page in extracted_pages:
            cleaned_text, _ = clean_text(page.raw_text, doc_id)
            if cleaned_text.strip():
                for line_str in cleaned_text.splitlines():
                    doc_lines.append((line_str, page.page_num))

        if not doc_lines:
            return chunks

        # Group lines into recommendation/section units
        active_section = doc_name
        active_heading = doc_name
        current_chunk_lines: list[tuple[str, int]] = []
        current_chunk_heading = active_heading
        current_chunk_section = active_section

        def emit_chunk(
            c_lines: list[tuple[str, int]],
            c_heading: str,
            c_section: str,
        ) -> None:
            nonlocal chunk_idx
            if not c_lines:
                return

            text_lines = [item[0] for item in c_lines]
            combined_text = "\n".join(text_lines).strip()
            if not combined_text:
                return

            # Ensure valid, non-empty heading
            final_heading = c_heading.strip() if c_heading.strip() else active_section.strip()
            if not final_heading:
                final_heading = doc_name

            # Check if text exceeds target_word_max; split cleanly by sentence batches
            words = combined_text.split()
            if len(words) > self.target_word_max:
                line_batches = split_long_lines(c_lines, self.target_word_max)
                part = 1
                for batch in line_batches:
                    sub_text = "\n".join(x[0] for x in batch).strip()
                    if not sub_text or not has_clinical_content(sub_text):
                        continue
                    p_start = batch[0][1]
                    p_end = batch[-1][1]
                    sub_heading = f"{final_heading} (Part {part})" if part > 1 else final_heading
                    part += 1
                    _append_chunk(sub_text, p_start, p_end, sub_heading, c_section)
            else:
                if not has_clinical_content(combined_text):
                    return
                p_start = c_lines[0][1]
                p_end = c_lines[-1][1]
                _append_chunk(combined_text, p_start, p_end, final_heading, c_section)

        def _append_chunk(
            text: str,
            page_start: int,
            page_end: int,
            heading: str,
            section: str,
        ) -> None:
            nonlocal chunk_idx
            chunk_id = f"{doc_id}_c{chunk_idx:04d}"
            chunk_idx += 1

            chunk_type = classify_chunk_type(text, heading)
            pop_tags = extract_population_tags(text)
            drug_tags = extract_drug_class_tags(text)
            ev_strength = extract_evidence_strength(text)
            rec_strength = extract_recommendation_strength(text)
            applicability = extract_applicability_conditions(text)
            exceptions = extract_exceptions(text)
            condition = resolve_chunk_condition(doc_condition, text)
            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

            section_clean = section.strip() if section.strip() else doc_name
            heading_clean = heading.strip() if heading.strip() else section_clean

            section_path = (
                f"{doc_name} > {section_clean}"
                if heading_clean == section_clean
                else f"{doc_name} > {section_clean} > {heading_clean}"
            )

            chunks.append(
                GuidelineChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    document_name=doc_name,
                    issuing_organization=issuer,
                    condition=condition,
                    section_path=section_path,
                    heading=heading_clean,
                    page_start=page_start,
                    page_end=page_end,
                    version=version,
                    publication_date=pub_date,
                    jurisdiction=jurisdiction,
                    document_status=doc_status,
                    chunk_type=chunk_type,
                    evidence_strength=ev_strength,
                    recommendation_strength=rec_strength,
                    population_tags=pop_tags,
                    drug_class_tags=drug_tags,
                    applicability_conditions=applicability,
                    exceptions=exceptions,
                    text=text,
                    text_hash=text_hash,
                )
            )

        # Iterate through all document lines
        for line_text, page_num in doc_lines:
            is_boundary, detected_heading = is_boundary_line(line_text)

            if is_boundary and current_chunk_lines:
                buf_words = sum(len(x[0].split()) for x in current_chunk_lines)
                buf_text = " ".join(x[0] for x in current_chunk_lines)

                # If current buffer has substantive content or is an explicit recommendation
                if buf_words >= self.target_word_min or has_clinical_content(buf_text):
                    emit_chunk(current_chunk_lines, current_chunk_heading, current_chunk_section)
                    current_chunk_lines = [(line_text, page_num)]
                    current_chunk_heading = detected_heading
                    current_chunk_section = active_section
                else:
                    # Buffer was sub-heading/short title; update heading context and accumulate
                    current_chunk_lines.append((line_text, page_num))
                    if detected_heading:
                        current_chunk_heading = f"{current_chunk_heading} > {detected_heading}"
            else:
                current_chunk_lines.append((line_text, page_num))

            # Update active section if this is a high-level header
            if (
                is_boundary
                and detected_heading
                and (
                    re.match(r"^\d+\.\d+\s+[A-Z]", detected_heading)
                    or (detected_heading.isupper() and len(detected_heading) > 5)
                )
            ):
                active_section = detected_heading

        # Emit remaining lines
        if current_chunk_lines:
            emit_chunk(current_chunk_lines, current_chunk_heading, current_chunk_section)

        return chunks


def process_all_guidelines(
    data_dir: Path,
    output_dir: Path,
) -> tuple[list[GuidelineChunk], dict[str, Any]]:
    """Process all 9 guideline documents in the inventory into clean chunks.

    Excludes unverified flowchart assets from retrieval indexing.

    Args:
        data_dir: Path to guideline_chatbot/data directory.
        output_dir: Path to guideline_chatbot/data/processed directory.

    Returns:
        Tuple of (all_chunks, processing_summary).
    """
    inventory_path = data_dir / "inventory" / "source_inventory.json"
    if not inventory_path.is_file():
        raise FileNotFoundError(f"Source inventory not found: {inventory_path}")

    with open(inventory_path, encoding="utf-8") as f:
        catalog: list[dict[str, Any]] = json.load(f)

    all_chunks: list[GuidelineChunk] = []
    chunker = GuidelineChunker()
    doc_summaries: list[dict[str, Any]] = []

    output_dir.mkdir(parents=True, exist_ok=True)

    for doc_meta in catalog:
        doc_id = str(doc_meta.get("doc_id", ""))
        local_path_str = str(doc_meta.get("local_path", ""))
        if local_path_str.startswith("guideline_chatbot/data/"):
            file_path = data_dir / local_path_str.replace("guideline_chatbot/data/", "")
        else:
            file_path = data_dir / "raw" / local_path_str
        ranges = doc_meta.get("relevant_page_ranges")

        logger.info("Processing %s from %s (ranges: %s)...", doc_id, file_path, ranges)
        extracted_pages = extract_pdf_pages(file_path, ranges)
        chunks = chunker.chunk_document(doc_meta, extracted_pages)

        # Verify no flowchart nodes or image-only nodes are indexed
        for c in chunks:
            assert not c.chunk_id.startswith("fc_"), (
                f"Flowchart node {c.chunk_id} accidentally indexed!"
            )

        all_chunks.extend(chunks)

        doc_summaries.append(
            {
                "doc_id": doc_id,
                "document_name": doc_meta.get("document_name"),
                "condition": doc_meta.get("condition"),
                "pages_extracted": len(extracted_pages),
                "chunks_generated": len(chunks),
            }
        )

    # Save to guideline_chunks.json
    chunks_json_path = output_dir / "guideline_chunks.json"
    with open(chunks_json_path, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in all_chunks], f, indent=2, ensure_ascii=False)

    # Save to guideline_chunks.jsonl
    chunks_jsonl_path = output_dir / "guideline_chunks.jsonl"
    with open(chunks_jsonl_path, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c.model_dump(), ensure_ascii=False) + "\n")

    summary = {
        "total_documents": len(catalog),
        "total_chunks": len(all_chunks),
        "documents": doc_summaries,
    }

    return all_chunks, summary
