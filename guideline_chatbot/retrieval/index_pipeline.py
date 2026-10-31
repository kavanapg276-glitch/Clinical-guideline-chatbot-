"""Pipeline for building and loading ChromaDB and BM25 retrieval indices.

Can be run directly via CLI to initialize or refresh the persistent Chroma database.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from guideline_chatbot.chunking.schemas import GuidelineChunk
from guideline_chatbot.retrieval.embeddings import EmbeddingManager
from guideline_chatbot.retrieval.hybrid import HybridRetriever
from guideline_chatbot.retrieval.keyword_index import KeywordIndex
from guideline_chatbot.retrieval.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def build_retrieval_system(
    chunks_path: Path | str = "guideline_chatbot/data/processed/guideline_chunks.json",
    chroma_dir: Path | str = "chroma",
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    rebuild: bool = False,
) -> tuple[HybridRetriever, list[GuidelineChunk]]:
    """Build or load ChromaDB vector store and in-memory BM25 index.

    Args:
        chunks_path: Path to guideline_chunks.json.
        chroma_dir: Directory for persistent ChromaDB storage.
        model_name: Embedding model identifier.
        rebuild: Whether to force re-indexing of ChromaDB.

    Returns:
        Tuple of (HybridRetriever, loaded_chunks).
    """
    chunks_file = Path(chunks_path)
    if not chunks_file.is_file():
        raise FileNotFoundError(f"Chunks file not found at {chunks_file}")

    with open(chunks_file, encoding="utf-8") as f:
        chunks_data: list[dict[str, Any]] = json.load(f)

    chunks = [GuidelineChunk(**c) for c in chunks_data]
    logger.info("Loaded %d guideline chunks from %s", len(chunks), chunks_file)

    embedding_manager = EmbeddingManager(model_name=model_name)
    vector_store = VectorStore(persist_dir=chroma_dir)

    # Index in ChromaDB if empty or rebuild requested
    if rebuild or vector_store.count() == 0:
        logger.info("Initializing ChromaDB collection...")
        vector_store.index_chunks(chunks, embedding_manager)
    else:
        logger.info("Reusing existing ChromaDB collection (%d vectors).", vector_store.count())

    # Build BM25 keyword index
    keyword_index = KeywordIndex()
    keyword_index.build_index(chunks)

    retriever = HybridRetriever(
        vector_store=vector_store,
        keyword_index=keyword_index,
        embedding_manager=embedding_manager,
    )

    return retriever, chunks


if __name__ == "__main__":
    retriever, chunks = build_retrieval_system(rebuild=True)
    logger.info("Retrieval system built successfully.")
    # Test query
    sample_query = "What is the blood pressure target for patients with type 2 diabetes?"
    res = retriever.retrieve(sample_query, top_k=3)
    print("\n--- SAMPLE RETRIEVAL TEST ---")
    print(f"Query: {sample_query}")
    print(f"Hits: {len(res['hits'])}")
    for h in res["hits"]:
        print(
            f"- [{h['chunk_id']}] score={h['score']:.4f} app={h['applicability']} | {h['metadata']['document_name']} (p. {h['metadata']['page_start']})"
        )
        print(f"  {h['text'][:120]}...\n")
