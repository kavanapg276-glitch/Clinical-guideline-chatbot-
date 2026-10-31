"""Schema definitions for guideline chunking.

Defines the GuidelineChunk model with clinical provenance, versioning,
applicability logic, and indexability flags.
"""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, Field, field_validator

ChunkType = Literal[
    "recommendation",
    "rationale",
    "table",
    "flowchart",
    "definition",
    "monitoring",
    "reference",
    "methods",
    "front_matter",
    "contributors",
    "other",
]


class GuidelineChunk(BaseModel):
    """A clinical guideline chunk with complete provenance and clinical metadata."""

    chunk_id: str
    doc_id: str
    document_name: str
    issuing_organization: str
    condition: str  # "hypertension" | "type_2_diabetes" | "both"
    section_path: str
    heading: str
    page_start: int
    page_end: int
    version: str | None = None
    publication_date: str | None = None
    last_updated: str | None = None
    last_updated_source: str | None = None
    recommendation_year: str | None = None
    jurisdiction: str = "unknown"
    document_status: str = "current"
    chunk_type: ChunkType = "other"
    indexed_for_retrieval: bool = True
    evidence_strength: str | None = None
    recommendation_strength: str | None = None
    population_tags: list[str] = Field(default_factory=list)
    drug_class_tags: list[str] = Field(default_factory=list)
    applicability_conditions: list[str] | None = None
    exceptions: list[str] | None = None
    text: str
    text_hash: str = ""

    @field_validator("text_hash", mode="before")
    @classmethod
    def set_text_hash(cls, v: str, info: object) -> str:
        """Compute sha256 text hash if not provided."""
        if v:
            return v
        data = getattr(info, "data", {})
        text = data.get("text", "") if isinstance(data, dict) else ""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def model_post_init(self, __context: object) -> None:
        """Ensure text_hash is set after initialization."""
        if not self.text_hash and self.text:
            self.text_hash = hashlib.sha256(self.text.encode("utf-8")).hexdigest()


CHUNK_METADATA_FIELDS = [
    "chunk_id",
    "doc_id",
    "document_name",
    "issuing_organization",
    "condition",
    "section_path",
    "heading",
    "page_start",
    "page_end",
    "version",
    "publication_date",
    "last_updated",
    "last_updated_source",
    "recommendation_year",
    "jurisdiction",
    "document_status",
    "chunk_type",
    "indexed_for_retrieval",
    "evidence_strength",
    "recommendation_strength",
    "population_tags",
    "drug_class_tags",
    "applicability_conditions",
    "exceptions",
    "text",
    "text_hash",
]
