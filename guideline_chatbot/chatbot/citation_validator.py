"""Citation validator for clinical guideline responses.

Extracts bracketed citations (e.g. `[Document, p. X, §Y, Year]`) from generated text
and verifies that every cited document and page is supported by retrieved chunks.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CitationReference:
    """Parsed citation entity extracted from generated text."""

    raw_text: str
    doc_identifier: str
    page: int | None = None
    section: str | None = None
    year: str | None = None
    is_valid: bool = False
    matched_chunk_id: str | None = None
    failure_reason: str | None = None


@dataclass
class CitationValidationResult:
    """Result of citation verification against retrieved chunks."""

    valid: bool
    total_citations: int
    validated_citations: list[CitationReference] = field(default_factory=list)
    unverified_citations: list[CitationReference] = field(default_factory=list)
    unsupported_claims_flagged: bool = False

    def summary(self) -> str:
        """Render a readable summary of validation findings."""
        if not self.total_citations:
            return "No citations found in text."
        valid_count = len(self.validated_citations)
        unverified_count = len(self.unverified_citations)
        return (
            f"Citations Verified: {valid_count}/{self.total_citations} "
            f"({(valid_count / self.total_citations) * 100:.1f}% valid). "
            f"Unverified: {unverified_count}"
        )


class CitationValidator:
    """Parses and validates guideline citations against retrieved chunk evidence."""

    CITATION_PATTERN = re.compile(r"\[([^\]]+)\]")

    def extract_citations(self, text: str) -> list[CitationReference]:
        """Extract bracketed citations from text and parse individual components."""
        citations: list[CitationReference] = []

        matches = self.CITATION_PATTERN.findall(text)
        for raw in matches:
            raw_stripped = raw.strip()

            # Ignore non-citation bracket expressions (e.g. [2019], [x], [IMAGE], [Research...])
            upper_raw = raw_stripped.upper()
            if (
                re.match(r"^\d{4}$", raw_stripped)
                or raw_stripped.lower().startswith("research")
                or upper_raw
                in {"IMAGE", "TABLE", "FIGURE", "BOX", "CHART", "PHOTO", "NOTE", "ALERT"}
            ):
                continue

            # Split components by comma or semicolon
            parts = [p.strip() for p in re.split(r"[,;]", raw_stripped) if p.strip()]
            if not parts:
                continue

            # If only a single element without comma/semicolon, require chunk_id pattern
            if len(parts) == 1 and not re.search(r"_[a-z0-9]+_\d{3}_c\d{4}", raw_stripped):
                continue

            doc_ident = parts[0]
            page_val: int | None = None
            section_val: str | None = None
            year_val: str | None = None

            for part in parts[1:]:
                # Check for page pattern: "p. 15", "pp. 12-14", "page 15"
                page_match = re.search(r"\b(?:p|pp|page)\.?\s*(\d+)", part, re.IGNORECASE)
                if page_match:
                    page_val = int(page_match.group(1))
                    continue

                # Check for year pattern: "2016", "2019", "2021", "2026"
                year_match = re.search(r"\b(19\d\d|20\d\d)\b", part)
                if year_match:
                    year_val = year_match.group(1)
                    continue

                # Check for section: "§1.4.15", "Section 3", "Treatment Algorithm"
                sec_match = re.search(r"(?:§|section\s*)(.+)", part, re.IGNORECASE)
                if sec_match:
                    section_val = sec_match.group(1).strip()
                elif not section_val:
                    section_val = part

            citations.append(
                CitationReference(
                    raw_text=f"[{raw_stripped}]",
                    doc_identifier=doc_ident,
                    page=page_val,
                    section=section_val,
                    year=year_val,
                )
            )

        return citations

    def validate(
        self,
        text: str,
        retrieved_chunks: list[dict[str, Any]],
    ) -> CitationValidationResult:
        """Validate all citations in text against retrieved chunks."""
        citations = self.extract_citations(text)
        if not citations:
            # If text had no citations, validity depends on whether it's an abstention/clarify turn
            return CitationValidationResult(
                valid=True,
                total_citations=0,
                validated_citations=[],
                unverified_citations=[],
                unsupported_claims_flagged=False,
            )

        validated: list[CitationReference] = []
        unverified: list[CitationReference] = []

        for cit in citations:
            matched_chunk = self._find_matching_chunk(cit, retrieved_chunks)
            if matched_chunk:
                cit.is_valid = True
                cit.matched_chunk_id = matched_chunk.get("chunk_id")
                validated.append(cit)
            else:
                cit.is_valid = False
                cit.failure_reason = "No retrieved chunk matches document name/id and page."
                unverified.append(cit)

        all_valid = len(unverified) == 0

        return CitationValidationResult(
            valid=all_valid,
            total_citations=len(citations),
            validated_citations=validated,
            unverified_citations=unverified,
            unsupported_claims_flagged=not all_valid,
        )

    def _find_matching_chunk(
        self,
        cit: CitationReference,
        chunks: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Match a citation against the candidate chunk list."""
        doc_q = cit.doc_identifier.lower().strip()

        for chunk in chunks:
            cid = chunk.get("chunk_id", "").lower()
            meta = chunk.get("metadata", {})
            doc_id = meta.get("doc_id", "").lower()
            doc_name = meta.get("document_name", "").lower()
            org = meta.get("issuing_organization", "").lower()
            page_start = meta.get("page_start")
            page_end = meta.get("page_end", page_start)

            # Match chunk_id directly
            if doc_q == cid or doc_q in cid:
                return chunk

            # Match document name or ID or organization keywords
            org_aliases = ["icmr", "nice", "who", "mohfw"]
            doc_matched = (
                doc_q in doc_name
                or doc_name in doc_q
                or doc_q in doc_id
                or any(
                    alias in doc_q and (alias in org or alias in doc_name) for alias in org_aliases
                )
            )

            if not doc_matched:
                continue

            # If page specified, verify page falls within [page_start, page_end]
            if cit.page is not None and page_start is not None:
                p_end = page_end if page_end is not None else page_start
                if page_start <= cit.page <= p_end:
                    return chunk
                # Allow tolerance of +/- 1 page if document matches
                if abs(cit.page - page_start) <= 1:
                    return chunk
            else:
                # If no page was specified in citation, matching the document is sufficient
                return chunk

        return None
