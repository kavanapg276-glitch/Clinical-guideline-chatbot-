"""Phase 0 verification tests.

Tests environment setup, dependency imports, embedding model,
inventory schema, and file integrity.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

# Project root (capstone/)
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestDirectoryStructure:
    """Verify all required directories exist."""

    REQUIRED_DIRS = [
        "guideline_chatbot/config",
        "guideline_chatbot/data/raw/mohfw_stg",
        "guideline_chatbot/data/raw/icmr_stw",
        "guideline_chatbot/data/raw/who",
        "guideline_chatbot/data/raw/nice",
        "guideline_chatbot/data/processed",
        "guideline_chatbot/data/inventory",
        "guideline_chatbot/data/reports",
        "guideline_chatbot/ingestion",
        "guideline_chatbot/chunking",
        "guideline_chatbot/retrieval",
        "guideline_chatbot/chatbot",
        "guideline_chatbot/coherence",
        "guideline_chatbot/integration",
        "guideline_chatbot/evaluation",
        "guideline_chatbot/evaluation/scenarios",
        "guideline_chatbot/evaluation/reference_answers",
        "guideline_chatbot/evaluation/reports",
        "guideline_chatbot/tests",
        "guideline_chatbot/docs",
    ]

    @pytest.mark.parametrize("rel_path", REQUIRED_DIRS)
    def test_directory_exists(self, rel_path: str) -> None:
        """Each required directory must exist."""
        full_path = PROJECT_ROOT / rel_path
        assert full_path.is_dir(), f"Directory missing: {rel_path}"


class TestGitignore:
    """Verify .gitignore contains required patterns."""

    REQUIRED_PATTERNS = [
        ".venv/",
        ".env",
        "guideline_chatbot/data/raw/",
        "chroma/",
        "__pycache__/",
    ]

    def test_gitignore_exists(self) -> None:
        """gitignore file must exist."""
        assert (PROJECT_ROOT / ".gitignore").is_file()

    @pytest.mark.parametrize("pattern", REQUIRED_PATTERNS)
    def test_gitignore_has_pattern(self, pattern: str) -> None:
        """gitignore must contain each required pattern."""
        content = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
        assert pattern in content, f"Pattern '{pattern}' not in .gitignore"


class TestDependencyImports:
    """Verify all required packages are importable."""

    def test_import_pymupdf(self) -> None:
        import pymupdf  # noqa: F401

    def test_import_sentence_transformers(self) -> None:
        import sentence_transformers  # noqa: F401

    def test_import_chromadb(self) -> None:
        import chromadb  # noqa: F401

    def test_import_rank_bm25(self) -> None:
        import rank_bm25  # noqa: F401

    def test_import_pydantic(self) -> None:
        import pydantic  # noqa: F401

    def test_import_yaml(self) -> None:
        import yaml  # noqa: F401

    def test_import_requests(self) -> None:
        import requests  # noqa: F401

    def test_import_bs4(self) -> None:
        import bs4  # noqa: F401

    def test_import_tqdm(self) -> None:
        import tqdm  # noqa: F401

    def test_import_pandas(self) -> None:
        import pandas  # noqa: F401

    def test_import_streamlit(self) -> None:
        import streamlit  # noqa: F401

    def test_import_dotenv(self) -> None:
        import dotenv  # noqa: F401


class TestSettingsYaml:
    """Verify settings.yaml loads correctly."""

    def test_settings_loads(self) -> None:
        import yaml

        settings_path = PROJECT_ROOT / "guideline_chatbot" / "config" / "settings.yaml"
        assert settings_path.is_file(), "settings.yaml not found"

        with open(settings_path, encoding="utf-8") as f:
            settings = yaml.safe_load(f)

        assert isinstance(settings, dict)
        assert "project" in settings
        assert "data" in settings
        assert "sources" in settings
        assert "embedding" in settings
        assert "downloader" in settings

    def test_settings_conditions(self) -> None:
        import yaml

        settings_path = PROJECT_ROOT / "guideline_chatbot" / "config" / "settings.yaml"
        with open(settings_path, encoding="utf-8") as f:
            settings = yaml.safe_load(f)

        conditions = settings["project"]["conditions"]
        assert "hypertension" in conditions
        assert "type_2_diabetes" in conditions

    def test_embedding_config(self) -> None:
        import yaml

        settings_path = PROJECT_ROOT / "guideline_chatbot" / "config" / "settings.yaml"
        with open(settings_path, encoding="utf-8") as f:
            settings = yaml.safe_load(f)

        assert settings["embedding"]["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"
        assert settings["embedding"]["dimension"] == 384


class TestEmbeddingModel:
    """Verify embedding model loads and produces correct output."""

    @pytest.fixture(autouse=True)
    def setup_offline(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Ensure tests use the locally cached model without network calls."""
        monkeypatch.setenv("HF_HUB_OFFLINE", "1")
        monkeypatch.setenv("TRANSFORMERS_OFFLINE", "1")

    def test_embedding_model_loads(self) -> None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)
        assert model is not None

    def test_embedding_shape(self) -> None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)
        result = model.encode(["Test sentence for embedding verification"])
        assert result.shape == (1, 384), f"Expected (1, 384), got {result.shape}"

    def test_embedding_deterministic(self) -> None:
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)
        text = ["Hypertension treatment guidelines"]
        result1 = model.encode(text)
        result2 = model.encode(text)
        np.testing.assert_array_almost_equal(result1, result2, decimal=5)


class TestDocumentation:
    """Verify required documentation files exist."""

    REQUIRED_DOCS = [
        "guideline_chatbot/docs/00_RECON_REPORT.md",
        "guideline_chatbot/docs/OPEN_QUESTIONS.md",
        "guideline_chatbot/docs/REVIEW_LOG.md",
        "guideline_chatbot/docs/ARCHITECTURE.md",
        "guideline_chatbot/docs/LICENSING.md",
    ]

    @pytest.mark.parametrize("doc_path", REQUIRED_DOCS)
    def test_doc_exists(self, doc_path: str) -> None:
        """Each required document must exist."""
        full_path = PROJECT_ROOT / doc_path
        assert full_path.is_file(), f"Document missing: {doc_path}"


class TestInventorySchema:
    """Verify inventory files exist and have correct schema (post-download)."""

    REQUIRED_FIELDS = [
        "doc_id",
        "document_name",
        "issuing_organization",
        "condition",
        "publication_date",
        "date_type",
        "version",
        "jurisdiction",
        "source_url",
        "document_status",
        "licence_note",
        "local_path",
        "sha256",
        "page_count",
        "text_extractable",
        "relevant_page_ranges",
        "ingestion_date",
        "notes",
    ]

    def test_inventory_csv_exists(self) -> None:
        """Inventory CSV must exist after download phase."""
        csv_path = (
            PROJECT_ROOT / "guideline_chatbot" / "data" / "inventory" / "source_inventory.csv"
        )
        assert csv_path.is_file(), "source_inventory.csv not found"

    def test_inventory_json_exists(self) -> None:
        """Inventory JSON must exist after download phase."""
        json_path = (
            PROJECT_ROOT / "guideline_chatbot" / "data" / "inventory" / "source_inventory.json"
        )
        assert json_path.is_file(), "source_inventory.json not found"

    def test_inventory_csv_schema(self) -> None:
        """CSV must have exactly the required fields."""
        csv_path = (
            PROJECT_ROOT / "guideline_chatbot" / "data" / "inventory" / "source_inventory.csv"
        )
        if not csv_path.is_file():
            pytest.skip("source_inventory.csv not yet created")

        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []

        for field in self.REQUIRED_FIELDS:
            assert field in headers, f"Missing field in CSV: {field}"

    def test_inventory_json_schema(self) -> None:
        """JSON records must have all required fields."""
        json_path = (
            PROJECT_ROOT / "guideline_chatbot" / "data" / "inventory" / "source_inventory.json"
        )
        if not json_path.is_file():
            pytest.skip("source_inventory.json not yet created")

        with open(json_path, encoding="utf-8") as f:
            records = json.load(f)

        assert isinstance(records, list)
        if records:
            for field in self.REQUIRED_FIELDS:
                assert field in records[0], f"Missing field in JSON: {field}"

    def test_inventory_sha256_matches(self) -> None:
        """SHA-256 hashes in inventory must match actual files."""
        json_path = (
            PROJECT_ROOT / "guideline_chatbot" / "data" / "inventory" / "source_inventory.json"
        )
        if not json_path.is_file():
            pytest.skip("source_inventory.json not yet created")

        with open(json_path, encoding="utf-8") as f:
            records = json.load(f)

        from guideline_chatbot.ingestion.acquire import compute_sha256

        for record in records:
            local_path = record.get("local_path", "")
            sha256 = record.get("sha256", "")
            if local_path and sha256:
                full_path = PROJECT_ROOT / local_path
                if full_path.is_file():
                    actual_hash = compute_sha256(full_path)
                    assert actual_hash == sha256, (
                        f"SHA-256 mismatch for {local_path}: "
                        f"inventory={sha256[:16]}..., actual={actual_hash[:16]}..."
                    )


class TestAcquireModule:
    """Verify the acquire module loads and has required functions."""

    def test_acquire_imports(self) -> None:
        from guideline_chatbot.ingestion.acquire import (  # noqa: F401
            DownloadResult,
            compute_sha256,
            get_pdf_metadata,
            run_acquisition,
        )

    def test_download_result_model(self) -> None:
        from guideline_chatbot.ingestion.acquire import DownloadResult

        result = DownloadResult(
            doc_id="test_001",
            document_name="Test Document",
            issuing_organization="Test Org",
            condition="hypertension",
            source_url="https://example.com/test.pdf",
        )
        assert result.download_status == "pending"
        assert result.doc_id == "test_001"


class TestInventoryModule:
    """Verify the inventory module loads and has required functions."""

    def test_inventory_imports(self) -> None:
        from guideline_chatbot.ingestion.inventory import (  # noqa: F401
            DOCUMENT_CATALOG,
            InventoryRecord,
            build_inventory,
            write_inventory_csv,
            write_inventory_json,
        )

    def test_inventory_record_model(self) -> None:
        from guideline_chatbot.ingestion.inventory import InventoryRecord

        record = InventoryRecord(
            doc_id="test_001",
            document_name="Test",
            issuing_organization="Test Org",
            condition="hypertension",
            sha256="abc123",
        )
        assert record.document_status == "unknown"
        assert record.ingestion_date  # Should have a default
