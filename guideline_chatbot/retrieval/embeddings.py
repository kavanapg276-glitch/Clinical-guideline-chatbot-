"""Embedding generation and caching for clinical guideline chunks.

Uses sentence-transformers/all-MiniLM-L6-v2 (configurable) to produce 384-dimensional
normalized embeddings. Caches embeddings by SHA-256 text_hash in a local SQLite store
to avoid redundant re-computation across pipeline runs.
"""

from __future__ import annotations

import logging
import os
import sqlite3
from pathlib import Path

# Ensure HuggingFace runs strictly in offline mode without attempting network retries
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_CACHE_DIR = Path("guideline_chatbot/data/cache")


class EmbeddingManager:
    """Manages embedding generation, normalization, batching, and persistent caching."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        cache_dir: Path | str = DEFAULT_CACHE_DIR,
        batch_size: int = 32,
    ) -> None:
        self.model_name = model_name
        self.batch_size = batch_size
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.cache_dir / "embeddings_cache.sqlite3"

        self._init_cache_db()
        self._model: SentenceTransformer | None = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy loader for SentenceTransformer model."""
        if self._model is None:
            logger.info("Loading embedding model '%s'...", self.model_name)
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _init_cache_db(self) -> None:
        """Initialize SQLite table for caching vectors by text_hash."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS embedding_cache (
                    text_hash TEXT PRIMARY KEY,
                    model_name TEXT NOT NULL,
                    dimension INTEGER NOT NULL,
                    vector BLOB NOT NULL
                )
                """
            )
            conn.commit()

    def _get_cached_vectors(self, text_hashes: list[str]) -> dict[str, list[float]]:
        """Retrieve pre-computed embeddings from SQLite cache."""
        if not text_hashes:
            return {}

        results: dict[str, list[float]] = {}
        # Batch query in chunks of 500 to stay within SQLite variable limits
        for i in range(0, len(text_hashes), 500):
            chunk = text_hashes[i : i + 500]
            placeholders = ",".join("?" for _ in chunk)
            query = f"""
                SELECT text_hash, vector, dimension
                FROM embedding_cache
                WHERE model_name = ? AND text_hash IN ({placeholders})
            """
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query, [self.model_name, *chunk])
                for thash, blob, _dim in cursor.fetchall():
                    vec = np.frombuffer(blob, dtype=np.float32).tolist()
                    results[thash] = vec
        return results

    def _save_vectors_to_cache(self, hashes_and_vectors: list[tuple[str, list[float]]]) -> None:
        """Store newly computed embeddings into SQLite cache."""
        if not hashes_and_vectors:
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            rows: list[tuple[str, str, int, bytes]] = []
            for thash, vec in hashes_and_vectors:
                arr = np.array(vec, dtype=np.float32)
                rows.append((thash, self.model_name, len(vec), arr.tobytes()))

            cursor.executemany(
                """
                INSERT OR REPLACE INTO embedding_cache (text_hash, model_name, dimension, vector)
                VALUES (?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()

    def embed_text(self, text: str, text_hash: str | None = None) -> list[float]:
        """Generate normalized embedding for a single text."""
        res = self.embed_batch([text], [text_hash] if text_hash else None)
        return res[0]

    def embed_batch(
        self,
        texts: list[str],
        text_hashes: list[str] | None = None,
    ) -> list[list[float]]:
        """Generate normalized embeddings for a batch of texts with cache acceleration.

        Args:
            texts: List of strings to encode.
            text_hashes: Optional list of corresponding sha256 text hashes.

        Returns:
            List of normalized float vectors (dimension 384).
        """
        if not texts:
            return []

        if text_hashes is None:
            import hashlib

            text_hashes = [hashlib.sha256(t.encode("utf-8")).hexdigest() for t in texts]

        # 1. Lookup in cache
        cached = self._get_cached_vectors(text_hashes)
        missing_indices: list[int] = []
        missing_texts: list[str] = []
        missing_hashes: list[str] = []

        for idx, (t, thash) in enumerate(zip(texts, text_hashes, strict=False)):
            if thash not in cached:
                missing_indices.append(idx)
                missing_texts.append(t)
                missing_hashes.append(thash)

        # 2. Compute missing vectors in batches
        if missing_texts:
            logger.info(
                "Embedding %d new chunks (%d loaded from cache)...",
                len(missing_texts),
                len(cached),
            )
            raw_vectors = self.model.encode(
                missing_texts,
                batch_size=self.batch_size,
                normalize_embeddings=True,
                show_progress_bar=len(missing_texts) > 50,
            )

            to_cache: list[tuple[str, list[float]]] = []
            for m_hash, m_vec in zip(missing_hashes, raw_vectors, strict=False):
                vec_list = m_vec.tolist()
                cached[m_hash] = vec_list
                to_cache.append((m_hash, vec_list))

            self._save_vectors_to_cache(to_cache)

        # 3. Assemble full results in original order
        return [cached[thash] for thash in text_hashes]
