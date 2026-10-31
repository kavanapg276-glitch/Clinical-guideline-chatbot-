"""PDF extraction pipeline for clinical guidelines.

Uses PyMuPDF to extract per-page text, layout blocks, font spans,
and tabular structures while preserving original 1-based page numbers
and enforcing relevant page ranges for multi-condition documents.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pymupdf

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ExtractedSpan:
    """A span of text with typographic properties."""

    text: str
    font: str = ""
    size: float = 0.0
    flags: int = 0
    is_bold: bool = False
    bbox: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


@dataclass(slots=True)
class ExtractedLine:
    """A line of text consisting of one or more spans."""

    text: str
    spans: list[ExtractedSpan] = field(default_factory=list)
    bbox: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


@dataclass(slots=True)
class ExtractedBlock:
    """A layout block from the page."""

    bbox: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    text: str = ""
    lines: list[ExtractedLine] = field(default_factory=list)
    block_type: int = 0  # 0 for text, 1 for image


@dataclass(slots=True)
class ExtractedTable:
    """A structured table extracted from the page."""

    bbox: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    rows: list[list[str]] = field(default_factory=list)
    markdown: str = ""


@dataclass(slots=True)
class ExtractedPage:
    """A single extracted PDF page with full provenance and structure."""

    page_num: int  # 1-based physical page number
    raw_text: str
    blocks: list[ExtractedBlock] = field(default_factory=list)
    tables: list[ExtractedTable] = field(default_factory=list)
    headings: list[tuple[str, int, float]] = field(default_factory=list)
    has_images: bool = False
    image_count: int = 0


def parse_page_ranges(range_str: str | None, max_pages: int) -> list[int]:
    """Parse a page range string into a list of 1-based page numbers.

    Supported formats:
        - None or "" -> all pages 1..max_pages
        - "6-21" -> [6, 7, ..., 21]
        - "1" -> [1]
        - "1-3, 5, 8-10" -> [1, 2, 3, 5, 8, 9, 10]

    Args:
        range_str: Range specification string.
        max_pages: Total number of pages in the PDF.

    Returns:
        Sorted list of unique 1-based page numbers within 1..max_pages.
    """
    if not range_str or not range_str.strip():
        return list(range(1, max_pages + 1))

    pages: set[int] = set()
    parts = [p.strip() for p in range_str.split(",") if p.strip()]

    for part in parts:
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            try:
                start = int(start_s.strip())
                end = int(end_s.strip())
                for p in range(start, end + 1):
                    if 1 <= p <= max_pages:
                        pages.add(p)
            except ValueError:
                logger.warning("Invalid page range slice: %s", part)
        else:
            try:
                p = int(part.strip())
                if 1 <= p <= max_pages:
                    pages.add(p)
            except ValueError:
                logger.warning("Invalid page number: %s", part)

    result = sorted(pages)
    return result if result else list(range(1, max_pages + 1))


def format_table_as_markdown(rows: list[list[str]]) -> str:
    """Format a 2D grid of cell values into a Markdown table."""
    if not rows:
        return ""

    cleaned_rows: list[list[str]] = []
    for row in rows:
        cleaned_row = [re.sub(r"\s+", " ", str(cell or "")).strip() for cell in row]
        cleaned_rows.append(cleaned_row)

    max_cols = max(len(r) for r in cleaned_rows)
    if max_cols == 0:
        return ""

    normalized_rows = [r + [""] * (max_cols - len(r)) for r in cleaned_rows]

    header = normalized_rows[0]
    separator = ["---"] * max_cols
    body = normalized_rows[1:]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")

    return "\n".join(lines)


def _is_bold_font(font_name: str, flags: int) -> bool:
    """Check if font properties indicate bold text."""
    lower_font = font_name.lower()
    return (
        bool(flags & 2)
        or bool(flags & 16)
        or "bold" in lower_font
        or "black" in lower_font
        or "heavy" in lower_font
    )


def _to_bbox(val: Any) -> tuple[float, float, float, float]:
    """Convert a bounding box sequence to a 4-tuple of floats."""
    if isinstance(val, (list, tuple)) and len(val) >= 4:
        return (float(val[0]), float(val[1]), float(val[2]), float(val[3]))
    return (0.0, 0.0, 0.0, 0.0)


def extract_pdf_pages(
    file_path: Path,
    relevant_page_ranges: str | None = None,
) -> list[ExtractedPage]:
    """Extract structured pages from a PDF document.

    Args:
        file_path: Absolute path to the PDF file.
        relevant_page_ranges: Page range string (e.g. "6-21"). If None, all pages.

    Returns:
        List of ExtractedPage objects with 1-based page numbers.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"PDF file does not exist: {file_path}")

    doc = pymupdf.open(file_path)
    total_doc_pages = len(doc)
    page_numbers = parse_page_ranges(relevant_page_ranges, total_doc_pages)

    extracted_pages: list[ExtractedPage] = []

    for page_num in page_numbers:
        page_idx = page_num - 1
        page = doc[page_idx]

        raw_text = page.get_text()
        page_dict: dict[str, Any] = page.get_text("dict")
        blocks_data = page_dict.get("blocks", [])

        extracted_blocks: list[ExtractedBlock] = []
        headings: list[tuple[str, int, float]] = []

        font_sizes: list[float] = []
        for b in blocks_data:
            if b.get("type", 0) == 0:
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        if span.get("text", "").strip():
                            font_sizes.append(float(span.get("size", 10.0)))

        body_font_size = 10.0
        if font_sizes:
            font_sizes.sort()
            body_font_size = font_sizes[len(font_sizes) // 2]

        for b in blocks_data:
            b_type = b.get("type", 0)
            bbox = _to_bbox(b.get("bbox"))

            if b_type == 0:  # text block
                extracted_lines: list[ExtractedLine] = []
                block_text_parts: list[str] = []

                for l_data in b.get("lines", []):
                    l_bbox = _to_bbox(l_data.get("bbox"))
                    extracted_spans: list[ExtractedSpan] = []
                    line_text_parts: list[str] = []

                    for s_data in l_data.get("spans", []):
                        s_text = s_data.get("text", "")
                        s_font = s_data.get("font", "")
                        s_size = float(s_data.get("size", 0.0))
                        s_flags = int(s_data.get("flags", 0))
                        is_bold = _is_bold_font(s_font, s_flags)
                        s_bbox = _to_bbox(s_data.get("bbox"))

                        extracted_spans.append(
                            ExtractedSpan(
                                text=s_text,
                                font=s_font,
                                size=s_size,
                                flags=s_flags,
                                is_bold=is_bold,
                                bbox=s_bbox,
                            )
                        )
                        line_text_parts.append(s_text)

                    line_text = "".join(line_text_parts)
                    extracted_lines.append(
                        ExtractedLine(
                            text=line_text,
                            spans=extracted_spans,
                            bbox=l_bbox,
                        )
                    )
                    block_text_parts.append(line_text)

                    # Heading detection
                    stripped_line = line_text.strip()
                    if stripped_line and len(stripped_line) < 120:
                        first_span_size = (
                            extracted_spans[0].size if extracted_spans else body_font_size
                        )
                        is_line_bold = any(s.is_bold for s in extracted_spans)

                        if first_span_size >= body_font_size * 1.25 or (
                            is_line_bold and first_span_size >= body_font_size * 1.15
                        ):
                            headings.append((stripped_line, 1, first_span_size))
                        elif is_line_bold or re.match(
                            r"^(?:Recommendation\s+\d+|\d+\.\d+(?:\.\d+)?\b)", stripped_line
                        ):
                            headings.append((stripped_line, 2, first_span_size))

                block_text = "\n".join(block_text_parts)
                extracted_blocks.append(
                    ExtractedBlock(
                        bbox=bbox,
                        text=block_text,
                        lines=extracted_lines,
                        block_type=0,
                    )
                )
            else:
                extracted_blocks.append(
                    ExtractedBlock(
                        bbox=bbox,
                        text="[IMAGE]",
                        block_type=1,
                    )
                )

        # Tables: detect structured tables if page text or structure indicates a table
        extracted_tables: list[ExtractedTable] = []
        has_table_indicator = bool(
            re.search(
                r"\b(?:Table\s+\d+|TABLE\s+\d+|Table\s*#|guidelines?\s+comparison)\b",
                raw_text,
                re.I,
            )
        ) or (file_path.name.startswith("mohfw_stg_hypertension_full") and 30 <= page_num <= 46)
        if has_table_indicator:
            try:
                drawings = page.get_drawings()
                if drawings:
                    tabs = page.find_tables()
                    for t in tabs.tables:
                        rows = t.extract()
                        if rows and len(rows) >= 2 and max(len(r) for r in rows) >= 2:
                            t_bbox = _to_bbox(t.bbox)
                            md = format_table_as_markdown(rows)
                            if md.strip():
                                extracted_tables.append(
                                    ExtractedTable(
                                        bbox=t_bbox,
                                        rows=rows,
                                        markdown=md,
                                    )
                                )
            except Exception as e:
                logger.warning("Error detecting tables on page %d: %s", page_num, e)

        # If tables were detected, replace text blocks inside table regions with markdown table
        if extracted_tables:
            filtered_blocks: list[ExtractedBlock] = []
            table_inserted: set[int] = set()

            for b in extracted_blocks:
                # Check if block falls inside any detected table
                inside_idx = -1
                for idx, t_obj in enumerate(extracted_tables):
                    tb = t_obj.bbox
                    bb = b.bbox
                    if (
                        bb[0] >= tb[0] - 5
                        and bb[1] >= tb[1] - 5
                        and bb[2] <= tb[2] + 5
                        and bb[3] <= tb[3] + 5
                    ):
                        inside_idx = idx
                        break

                if inside_idx >= 0:
                    if inside_idx not in table_inserted:
                        table_inserted.add(inside_idx)
                        filtered_blocks.append(
                            ExtractedBlock(
                                bbox=extracted_tables[inside_idx].bbox,
                                text=extracted_tables[inside_idx].markdown,
                                lines=[],
                                block_type=0,
                            )
                        )
                else:
                    filtered_blocks.append(b)

            extracted_blocks = filtered_blocks
            raw_text = "\n\n".join(b.text for b in extracted_blocks if b.text.strip())

        # Images
        image_list = page.get_images()
        image_count = len(image_list)
        has_images = image_count > 0

        extracted_pages.append(
            ExtractedPage(
                page_num=page_num,
                raw_text=raw_text,
                blocks=extracted_blocks,
                tables=extracted_tables,
                headings=headings,
                has_images=has_images,
                image_count=image_count,
            )
        )

    doc.close()
    return extracted_pages
