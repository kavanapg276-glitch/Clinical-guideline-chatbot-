"""Script to generate the Phase 1 30-chunk random audit markdown report."""

import json
import random
from pathlib import Path


def main() -> None:
    guideline_dir = Path(__file__).resolve().parent.parent
    chunks_path = guideline_dir / "data" / "processed" / "guideline_chunks.json"
    audit_path = guideline_dir / "data" / "reports" / "chunk_audit_30.md"

    with open(chunks_path, encoding="utf-8") as f:
        chunks = json.load(f)

    random.seed(42)
    sample_indices = sorted(random.sample(range(len(chunks)), 30))
    sample_chunks = [chunks[i] for i in sample_indices]

    out = []
    out.append("# Phase 1: 30-Chunk Random Provenance & Clinical Integrity Audit\n")
    out.append("**Date:** 2026-11-01  ")
    out.append(
        "**Sampling Method:** Pseudo-random deterministic sampling (`random.seed(42)`) "
        "across 974 guideline chunks  "
    )
    out.append(
        "**Purpose:** Manual verification of source document traceability, page bounds, "
        "recommendation context, and exclusion of unverified flowcharts.\n"
    )
    out.append("---\n")
    out.append("## Summary Audit Table\n")
    out.append(
        "| # | Chunk ID | Document ID | Source Page(s) | Condition | Chunk Type | "
        "Populations | Drug Classes | Heading |"
    )
    out.append("|---|---|---|---|---|---|---|---|---|")

    for idx, c in enumerate(sample_chunks, 1):
        cid = c["chunk_id"]
        did = c["doc_id"]
        pstart = c["page_start"]
        pend = c["page_end"]
        pages = f"p. {pstart}" if pstart == pend else f"pp. {pstart}-{pend}"
        cond = c["condition"]
        ctype = c["chunk_type"]
        pops = ", ".join(c["population_tags"]) if c["population_tags"] else "None"
        drugs = ", ".join(c["drug_class_tags"]) if c["drug_class_tags"] else "None"
        h = c["heading"].replace("|", "/")
        if len(h) > 50:
            h = h[:47] + "..."
        out.append(
            f"| {idx} | `{cid}` | `{did}` | {pages} | {cond} | {ctype} | {pops} | {drugs} | {h} |"
        )

    out.append("\n---\n")
    out.append("## Detailed Chunk Inspection\n")

    for idx, c in enumerate(sample_chunks, 1):
        cid = c["chunk_id"]
        did = c["doc_id"]
        dname = c["document_name"]
        pstart = c["page_start"]
        pend = c["page_end"]
        pages = f"p. {pstart}" if pstart == pend else f"pp. {pstart}-{pend}"
        cond = c["condition"]
        ctype = c["chunk_type"]
        spath = c["section_path"]
        h = c["heading"]
        pops = c["population_tags"]
        drugs = c["drug_class_tags"]
        app = c["applicability_conditions"]
        exc = c["exceptions"]
        txt = c["text"]
        thash = c["text_hash"]

        out.append(f"### Audit Item #{idx}: `{cid}`\n")
        out.append(f"- **Source Document:** {dname} (`{did}`)")
        out.append(f"- **Source Page(s):** {pages}")
        out.append(f"- **Condition:** `{cond}` | **Chunk Type:** `{ctype}`")
        out.append(f"- **Section Path:** `{spath}`")
        out.append(f"- **Heading:** {h}")
        out.append(f"- **Population Tags:** {pops}")
        out.append(f"- **Drug Class Tags:** {drugs}")
        out.append(f"- **Applicability Conditions:** {app}")
        out.append(f"- **Exceptions / Contraindications:** {exc}")
        out.append(f"- **Text Hash:** `{thash}`")
        out.append("\n```text")
        out.append(txt)
        out.append("```\n")
        out.append("---\n")

    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"Saved {audit_path} successfully!")


if __name__ == "__main__":
    main()
