"""CLI runner for guideline chunking pipeline.

Extracts, cleans, and chunks all 9 guideline documents, writes out
guideline_chunks.json and guideline_chunks.jsonl, and generates
the Phase 1 Dataset Quality Report.
"""

from __future__ import annotations

import logging
from pathlib import Path

from guideline_chatbot.chunking.recommendation_chunker import process_all_guidelines

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    output_dir = data_dir / "processed"

    print("Starting chunking pipeline...")
    print(f"Data directory: {data_dir}")
    print(f"Output directory: {output_dir}")

    chunks, summary = process_all_guidelines(data_dir, output_dir)

    print("\n" + "=" * 60)
    print("CHUNK GENERATION COMPLETE")
    print(f"Total documents processed: {summary['total_documents']}")
    print(f"Total chunks generated: {summary['total_chunks']}")
    print("=" * 60)
    for doc in summary["documents"]:
        cid = doc["doc_id"]
        cnt = doc["chunks_generated"]
        pgs = doc["pages_extracted"]
        print(f"  - {cid}: {cnt} chunks ({pgs} pages)")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
