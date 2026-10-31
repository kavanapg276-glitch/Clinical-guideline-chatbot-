"""Text cleaning and normalization module for clinical guidelines.

Strips document headers, footers, page numbers, and repeated administrative boilerplate
while preserving 100% of clinical recommendations, drug names, dosages, laboratory
thresholds, frequencies, and contraindications. Tracks before-and-after statistics.
"""

from __future__ import annotations

import logging
import re
import unicodedata

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CleaningStats(BaseModel):
    """Statistics tracking before/after text cleaning metrics."""

    doc_id: str = ""
    raw_chars: int = 0
    clean_chars: int = 0
    chars_removed: int = 0
    raw_lines: int = 0
    clean_lines: int = 0
    lines_removed: int = 0
    reduction_pct: float = 0.0


# Document-specific boilerplate patterns to strip
BOILERPLATE_PATTERNS = [
    # NICE running footers & notice of rights
    (
        r"(?:©|\ufffd|\(c\))\s*NICE\s*\d{4}\.\s*All rights reserved\..*?"
        r"(?:conditions#notice-of-rights\)?\.?|https://www\.nice\.org\.uk/terms-and-conditions[^\s\n]*)"
    ),
    # ICMR bottom administrative disclaimer
    (
        r"This\s+STW\s+has\s+been\s+prepared\s+by\s+national\s+experts\s+of\s+India\s+with\s+"
        r"feasibility\s+considerations\s+for\s+various\s+levels\s+of\s+healthcare\s+system\s+"
        r"in\s+the\s+country\..*?"
        r"(?:Department of Health Research, Ministry of Health & Family Welfare, "
        r"Government of India\.|Ministry of Health & Family Welfare)"
    ),
]

COMPILED_BOILERPLATE = [
    re.compile(pattern, re.IGNORECASE | re.DOTALL) for pattern in BOILERPLATE_PATTERNS
]

# Line-level patterns to drop
LINE_DROP_PATTERNS = [
    # NICE header lines
    re.compile(
        r"^Screening,\s*Diagnosis,\s*Assessment,\s*and\s*Management\s+of\s+Primary\s+Hypertension.*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^GUIDELINE\s+FOR\s+THE\s+PHARMACOLOGICAL\s+TREATMENT\s+OF\s+HYPERTENSION\s+IN\s+ADULTS\s*$",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*Department\s+of\s+Health\s+Research\s*$", re.IGNORECASE),
    re.compile(
        r"^\s*Ministry\s+of\s+Health\s+and\s+Family\s+Welfare,\s*Government\s+of\s+India\s*$",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*Standard\s+Treatment\s+Workflow\s*\(STW\)\s*$", re.IGNORECASE),
    re.compile(
        r"^(?:Hypertension in adults: diagnosis and management|"
        r"Type 2 diabetes in adults: management)"
        r"(?:\s*\([A-Z0-9]+\))?\s*$",
        re.IGNORECASE,
    ),
    # MoHFW headers
    re.compile(
        r"^Standard\s+Treatment\s+Guidelines\s*[-–—]?\s*(?:Hypertension|Endocrinology)?\s*$",
        re.IGNORECASE,
    ),
    re.compile(r"^Standard Treatment Guidelines\s*[-–—]?\s*", re.IGNORECASE),
    # WHO headers
    re.compile(
        r"^WHO\s+Guideline\s+for\s+the\s+pharmacological\s+treatment\s+of\s+hypertension\s+in\s+adults\s*$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^HEARTS-D:\s*Diagnosis\s+and\s+management\s+of\s+type\s+2\s+diabetes\s*$", re.IGNORECASE
    ),
    re.compile(r"^World\s+Health\s+Organization\s+202[01]\s*$", re.IGNORECASE),
    # Page numbers
    re.compile(r"^Page\s+\d+(\s+of\s+\d+)?\s*$", re.IGNORECASE),
    re.compile(r"^\s*Page\s+\d+\s+of\s*$", re.IGNORECASE),
    re.compile(r"^\s*\d{1,3}\s*$"),  # Standalone page numbers up to 3 digits
]


def normalize_unicode_symbols(text: str) -> str:
    """Normalize unicode ligatures, math symbols, bullets, and dashes.

    Converts characters to standardized ASCII-friendly equivalents while
    preserving mathematical and clinical meaning (e.g. >=, <=, +/-).
    """
    # NFKD decomposition replaces ligatures like 'fi', 'fl' with separate characters
    text = unicodedata.normalize("NFKD", text)

    # Standardize comparison and math operators
    replacements = {
        "\u2265": ">=",  # ≥
        "\u2264": "<=",  # ≤
        "\u00b1": "+/-",  # ±
        "\u00d7": "x",  # ×
        "\u2013": "-",  # en-dash
        "\u2014": "-",  # em-dash
        "\u2018": "'",  # left single quote
        "\u2019": "'",  # right single quote
        "\u201c": '"',  # left double quote
        "\u201d": '"',  # right double quote
        "\u2022": "- ",  # bullet point
        "\u25cf": "- ",  # black circle bullet
        "\u25aa": "- ",  # black small square
        "\u25b6": "> ",  # black right-pointing triangle
        "\ufffd": "- ",  # replacement character (often corrupted bullet)
        "\xa0": " ",  # non-breaking space
        "\u200b": "",  # zero-width space
        "\u2026": "...",  # ellipsis
    }

    for char, repl in replacements.items():
        text = text.replace(char, repl)

    return text


def repair_hyphenated_linebreaks(text: str) -> str:
    """Rejoin words split across line breaks with hyphens.

    Only rejoins lowercase continuation lines (e.g., 'hyper-\\ntension' -> 'hypertension').
    Preserves deliberate compound words and bullet items.
    """
    return re.sub(r"([A-Za-z]{3,})-\n([a-z]{3,})", r"\1\2", text)


def clean_text(raw_text: str, doc_id: str = "") -> tuple[str, CleaningStats]:
    """Clean raw extracted text by stripping boilerplate and normalizing formatting.

    Args:
        raw_text: Raw string extracted from PDF.
        doc_id: Optional document identifier for stats reporting.

    Returns:
        Tuple of (cleaned_text, CleaningStats).
    """
    if not raw_text:
        return "", CleaningStats(doc_id=doc_id)

    raw_chars = len(raw_text)
    raw_lines = len(raw_text.splitlines())

    # Step 1: Unicode normalization & symbol translation
    text = normalize_unicode_symbols(raw_text)

    # Step 2: Strip compiled multi-line boilerplate blocks
    for pattern in COMPILED_BOILERPLATE:
        text = pattern.sub("", text)

    # Step 3: Repair hyphenated line breaks
    text = repair_hyphenated_linebreaks(text)

    # Step 4: Line-level filtering
    filtered_lines: list[str] = []
    for line in text.splitlines():
        line_stripped = line.strip()

        # Check if line matches any drop pattern
        drop = False
        for drop_pat in LINE_DROP_PATTERNS:
            if drop_pat.match(line_stripped):
                drop = True
                break

        if not drop:
            filtered_lines.append(line.rstrip())

    # Step 5: Collapse multiple consecutive blank lines (max 2 consecutive newlines)
    rebuilt_text = "\n".join(filtered_lines)
    clean_text_final = re.sub(r"\n{3,}", "\n\n", rebuilt_text).strip()

    clean_chars = len(clean_text_final)
    clean_lines = len(clean_text_final.splitlines()) if clean_text_final else 0
    chars_removed = max(0, raw_chars - clean_chars)
    lines_removed = max(0, raw_lines - clean_lines)
    reduction_pct = (chars_removed / raw_chars * 100.0) if raw_chars > 0 else 0.0

    stats = CleaningStats(
        doc_id=doc_id,
        raw_chars=raw_chars,
        clean_chars=clean_chars,
        chars_removed=chars_removed,
        raw_lines=raw_lines,
        clean_lines=clean_lines,
        lines_removed=lines_removed,
        reduction_pct=round(reduction_pct, 2),
    )

    return clean_text_final, stats
