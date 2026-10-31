"""ChromaDB persistent vector store for clinical guideline chunks.

Indexes normalized semantic embeddings with complete clinical metadata filters:
condition, population tags, jurisdiction, document status, and chunk type.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings

from guideline_chatbot.chunking.schemas import GuidelineChunk
from guideline_chatbot.retrieval.embeddings import EmbeddingManager

logger = logging.getLogger(__name__)

DEFAULT_CHROMA_DIR = Path("chroma")
COLLECTION_NAME = "guideline_chunks"


class VectorStore:
    """ChromaDB vector database wrapper with typed metadata filtering."""

    def __init__(
        self,
        persist_dir: Path | str = DEFAULT_CHROMA_DIR,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name

        self._client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(anonymized_telemetry=False, is_persistent=True),
        )
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @property
    def collection(self) -> chromadb.Collection:
        """Return the active Chroma collection."""
        return self._collection

    def count(self) -> int:
        """Return the number of vectors stored in the collection."""
        return self._collection.count()

    def index_chunks(
        self,
        chunks: list[GuidelineChunk],
        embedding_manager: EmbeddingManager,
        batch_size: int = 100,
    ) -> int:
        """Index chunks flagged for retrieval into ChromaDB.

        Args:
            chunks: List of GuidelineChunk objects.
            embedding_manager: Pre-configured EmbeddingManager instance.
            batch_size: Batch size for ChromaDB upsert operations.

        Returns:
            Number of successfully indexed chunks.
        """
        # Strictly filter out non-indexable noise (references, methods, flowcharts, front matter)
        indexable_chunks = [c for c in chunks if c.indexed_for_retrieval]
        logger.info(
            "Indexing %d chunks into ChromaDB (excluded %d noise/flowchart chunks)...",
            len(indexable_chunks),
            len(chunks) - len(indexable_chunks),
        )

        if not indexable_chunks:
            return 0

        # Compute or retrieve cached embeddings for enriched chunk representations
        texts = [f"[{c.issuing_organization}] {c.heading}\n{c.text}" for c in indexable_chunks]
        hashes = [hashlib.sha256(t.encode("utf-8")).hexdigest() for t in texts]
        embeddings = embedding_manager.embed_batch(texts, hashes)

        total_upserted = 0
        for i in range(0, len(indexable_chunks), batch_size):
            chunk_batch = indexable_chunks[i : i + batch_size]
            emb_batch = embeddings[i : i + batch_size]

            ids: list[str] = []
            documents: list[str] = []
            metadatas: list[dict[str, Any]] = []

            for c in chunk_batch:
                ids.append(c.chunk_id)
                documents.append(c.text)

                # ChromaDB requires primitive metadata types (str, int, float, bool)
                meta: dict[str, Any] = {
                    "chunk_id": c.chunk_id,
                    "doc_id": c.doc_id,
                    "document_name": c.document_name,
                    "issuing_organization": c.issuing_organization,
                    "condition": c.condition,
                    "section_path": c.section_path,
                    "heading": c.heading,
                    "page_start": c.page_start,
                    "page_end": c.page_end,
                    "version": c.version or "",
                    "publication_date": c.publication_date or "",
                    "last_updated": c.last_updated or "",
                    "recommendation_year": c.recommendation_year or "",
                    "jurisdiction": c.jurisdiction,
                    "document_status": c.document_status,
                    "chunk_type": c.chunk_type,
                    "evidence_strength": c.evidence_strength or "",
                    "recommendation_strength": c.recommendation_strength or "",
                    "population_tags": ",".join(c.population_tags),
                    "drug_class_tags": ",".join(c.drug_class_tags),
                }
                metadatas.append(meta)

            self._collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=emb_batch,  # type: ignore[arg-type]
                metadatas=metadatas,  # type: ignore[arg-type]
            )
            total_upserted += len(chunk_batch)

        logger.info("ChromaDB indexing complete. Total in collection: %d", self.count())
        return total_upserted

    def query_dense(
        self,
        query_text: str,
        embedding_manager: EmbeddingManager,
        top_k: int = 10,
        where_filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Perform dense semantic vector search.

        Args:
            query_text: User clinical question or prompt.
            embedding_manager: EmbeddingManager instance.
            top_k: Number of nearest neighbors to retrieve.
            where_filter: Optional ChromaDB metadata filter dictionary.

        Returns:
            List of hit dictionaries: {chunk_id, text, score, metadata}.
        """
        query_vec = embedding_manager.embed_text(query_text)

        kwargs: dict[str, Any] = {
            "query_embeddings": [query_vec],
            "n_results": top_k,
            "include": ["documents", "metadatas", "distances"],
        }
        if where_filter:
            kwargs["where"] = where_filter

        results = self._collection.query(**kwargs)

        hits: list[dict[str, Any]] = []
        if (
            not results
            or not results["ids"]
            or not results["documents"]
            or not results["metadatas"]
            or not results["distances"]
        ):
            return hits

        for cid, doc, meta, dist in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
            strict=False,
        ):
            # For cosine distance, similarity is 1.0 - distance
            score = max(0.0, 1.0 - float(dist))
            hits.append(
                {
                    "chunk_id": cid,
                    "text": doc,
                    "score": score,
                    "metadata": meta,
                }
            )

        return hits
