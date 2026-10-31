"""Source inventory builder.

Scans data/raw/<source>/ directories, computes metadata for each PDF,
and outputs source_inventory.csv and source_inventory.json with exactly
the fields specified in the project spec (§5.3).
"""

from __future__ import annotations

import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from guideline_chatbot.ingestion.acquire import (
    compute_sha256,
    get_pdf_metadata,
)

logger = logging.getLogger(__name__)


class InventoryRecord(BaseModel):
    """One row in the source inventory."""

    doc_id: str
    document_name: str
    issuing_organization: str
    condition: str
    publication_date: str | None = None
    date_type: str | None = None  # publication | copyright | unspecified | None
    version: str | None = None
    jurisdiction: str = "unknown"
    source_url: str = ""
    document_status: str = "unknown"  # current | superseded | draft | unknown
    licence_note: str | None = None
    local_path: str = ""
    sha256: str = ""
    page_count: int = 0
    text_extractable: bool = False
    relevant_page_ranges: str | None = None
    ingestion_date: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d")
    )
    notes: str | None = None


INVENTORY_FIELDS = [
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

# Verified official licence quotes
WHO_LICENCE_NOTE = (
    "CC BY-NC-SA 3.0 IGO; quoted: 'Some rights reserved. This work is available under "
    "the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO licence "
    "(CC BY-NC-SA 3.0 IGO; https://creativecommons.org/licenses/by-nc-sa/3.0/igo). "
    "Under the terms of this licence, you may copy, redistribute and adapt the work "
    "for non-commercial purposes, provided the work is appropriately cited.' "
    "(URL: https://www.who.int/about/policies/publishing/copyright)"
)

ICMR_LICENCE_NOTE = (
    "Government of India / ICMR official STW publication; quoted: 'This STW has been "
    "prepared by national experts of India with feasibility considerations for various "
    "levels of healthcare system in the country. These broad guidelines are advisory, and "
    "are based on expert opinions and available scientific evidence. ... (c) Indian "
    "Council of Medical Research and Department of Health Research, Ministry of Health & "
    "Family Welfare, Government of India.' "
    "(URL: https://www.icmr.gov.in/standard-treatment-workflows-stws)"
)

NICE_LICENCE_NOTE = (
    "NICE UK Notice of Rights / Crown Copyright; quoted: '18. Reproduction, publication or "
    "distribution of the content from the website, including NICE copyright material, is subject "
    "to the following \\'Notice of Rights\\': Copyright content owned by the National "
    "Institute for Health and Care Excellence (NICE) is made available for reuse to individuals "
    "and commercial/non-commercial organisations on a non-exclusive basis in the United Kingdom "
    "only under the NICE UK Open Content Licence. Except for personal use, study or personal "
    "research, copyright content owned by the National Institute for Health and Care Excellence "
    "(NICE) may not be used, reproduced, translated, distributed or transmitted in any form, in "
    "whole or in part, by any means, electronic, mechanical, photocopying, recording or otherwise, "
    "without prior written permission from NICE.' "
    "(URL: https://www.nice.org.uk/terms-and-conditions#notice-of-rights)"
)

MOHFW_LICENCE_NOTE = (
    "Permission required before reproduction; source acknowledgement required; quoted: "
    "'Material featured on this Portal may be reproduced free of charge after taking proper "
    "permission by sending a mail to us. However, the material has to be reproduced accurately "
    "and not to be used in a derogatory manner or in a misleading context. Wherever the material "
    "is being published or issued to others, the source must be prominently acknowledged.' "
    "(URL: https://clinicalestablishments.mohfw.gov.in/en/copyright-policy)"
)

# Canonical catalog of target guideline documents
DOCUMENT_CATALOG = [
    {
        "doc_id": "who_htn_001",
        "document_name": (
            "WHO Guideline for the Pharmacological Treatment of Hypertension in Adults"
        ),
        "issuing_organization": "World Health Organization",
        "condition": "hypertension",
        "publication_date": "2021",
        "date_type": "publication",
        "version": None,
        "jurisdiction": "International",
        "source_url": "https://www.who.int/publications/i/item/9789240033986",
        "document_status": "current",
        "licence_note": WHO_LICENCE_NOTE,
        "rel_path": "who/who_htn_pharmacological_treatment_2021.pdf",
        "relevant_page_ranges": "1-61",
        "notes": (
            "Status: current (latest WHO adult hypertension guideline, active 2021). "
            "Full guideline covering BP thresholds, drug classes, combination therapy, and targets."
        ),
    },
    {
        "doc_id": "who_t2dm_001",
        "document_name": "WHO HEARTS-D: Diagnosis and Management of Type 2 Diabetes",
        "issuing_organization": "World Health Organization",
        "condition": "type_2_diabetes",
        "publication_date": "2020",
        "date_type": "publication",
        "version": None,
        "jurisdiction": "International",
        "source_url": "https://www.who.int/publications/i/item/WHO-UCN-NCD-20.1",
        "document_status": "current",
        "licence_note": WHO_LICENCE_NOTE,
        "rel_path": "who/who_t2dm_hearts_d_2020.pdf",
        "relevant_page_ranges": "1-35",
        "notes": (
            "Status: current (active primary care module). "
            "Primary healthcare module on diagnosis, lifestyle, oral agents, insulin initiation."
        ),
    },
    {
        "doc_id": "icmr_htn_001",
        "document_name": "ICMR Standard Treatment Workflow - Hypertension in Adults (ICD-11 BA00)",
        "issuing_organization": "Indian Council of Medical Research (ICMR) / DHR",
        "condition": "hypertension",
        "publication_date": "May/2026",
        "date_type": "unspecified",
        "version": None,
        "jurisdiction": "India",
        "source_url": (
            "https://www.icmr.gov.in/icmrobject/uploads/STWs/1778941063_hypertensioninadults_final.pdf"
        ),
        "document_status": "current",
        "licence_note": ICMR_LICENCE_NOTE,
        "rel_path": "icmr_stw/icmr_htn_hypertension_in_adults.pdf",
        "relevant_page_ranges": "1",
        "notes": (
            "Status: current. Printed date: May/2026 (date_type: unspecified; printed date of "
            "unspecified type, exact meaning unstated in document). Active on stw.icmr.org.in. "
            "Evidence-based clinical decision workflow for all levels of Indian healthcare system."
        ),
    },
    {
        "doc_id": "icmr_t2dm_001",
        "document_name": (
            "ICMR Standard Treatment Workflow - Diabetes Mellitus Type 2 (ICD-10-E11)"
        ),
        "issuing_organization": "Indian Council of Medical Research (ICMR) / DHR",
        "condition": "type_2_diabetes",
        "publication_date": "July/ 2022",
        "date_type": "unspecified",
        "version": None,
        "jurisdiction": "India",
        "source_url": (
            "https://www.icmr.gov.in/icmrobject/uploads/STWs/1726567245_diabetes_mellitus_type_2.pdf"
        ),
        "document_status": "current",
        "licence_note": ICMR_LICENCE_NOTE,
        "rel_path": "icmr_stw/icmr_t2dm_diabetes_type2.pdf",
        "relevant_page_ranges": "1",
        "notes": (
            "Status: current. Printed date: July/ 2022 (date_type: unspecified; printed date of "
            "unspecified type, exact meaning unstated in document). Active on stw.icmr.org.in. "
            "Stepwise algorithmic management of Type 2 Diabetes Mellitus in primary/secondary care."
        ),
    },
    {
        "doc_id": "nice_htn_001",
        "document_name": "NICE Guideline NG136: Hypertension in Adults - Diagnosis and Management",
        "issuing_organization": "National Institute for Health and Care Excellence (NICE)",
        "condition": "hypertension",
        "publication_date": "2019-08-28",
        "date_type": "publication",
        "version": None,
        "jurisdiction": "United Kingdom",
        "source_url": "https://www.nice.org.uk/guidance/ng136",
        "document_status": "current",
        "licence_note": NICE_LICENCE_NOTE,
        "rel_path": "nice/nice_ng136_hypertension.pdf",
        "relevant_page_ranges": "1-52",
        "notes": (
            "Status: current (published 28 August 2019, last updated 26 February 2026, active). "
            "Comprehensive clinical guideline covering diagnosis, risk assessment, drug therapy."
        ),
    },
    {
        "doc_id": "nice_t2dm_001",
        "document_name": "NICE Guideline NG28: Type 2 Diabetes in Adults - Management",
        "issuing_organization": "National Institute for Health and Care Excellence (NICE)",
        "condition": "type_2_diabetes",
        "publication_date": "2015-12-02",
        "date_type": "publication",
        "version": None,
        "jurisdiction": "United Kingdom",
        "source_url": "https://www.nice.org.uk/guidance/ng28",
        "document_status": "current",
        "licence_note": NICE_LICENCE_NOTE,
        "rel_path": "nice/nice_ng28_type2_diabetes.pdf",
        "relevant_page_ranges": "1-131",
        "notes": (
            "Status: current (published 2 December 2015, last updated 18 February 2026, active). "
            "Comprehensive management guideline: individualised targets, "
            "dietary advice, drug therapy."
        ),
    },
    {
        "doc_id": "mohfw_htn_001",
        "document_name": "MoHFW STG - Hypertension (Background Document)",
        "issuing_organization": "Ministry of Health and Family Welfare, Government of India",
        "condition": "hypertension",
        "publication_date": "March 2016",
        "date_type": "unspecified",
        "version": None,
        "jurisdiction": "India",
        "source_url": (
            "https://clinicalestablishments.mohfw.gov.in/sites/default/files/"
            "standard-treatment-guidelines/5191.pdf"
        ),
        "document_status": "current",
        "licence_note": MOHFW_LICENCE_NOTE,
        "rel_path": "mohfw_stg/mohfw_stg_hypertension_full.pdf",
        "relevant_page_ranges": "1-144",
        "notes": (
            "Status: current. Printed date: March 2016 (date_type: unspecified; printed on cover, "
            "meaning unstated). Tagged as background document. Contains comprehensive "
            "epidemiology, pathophysiology, screening, and diagnostic rationale for primary "
            "hypertension in adults in India."
        ),
    },
    {
        "doc_id": "mohfw_htn_002",
        "document_name": (
            "MoHFW Standard Treatment Guidelines - Hypertension (Quick Reference Guide)"
        ),
        "issuing_organization": "Ministry of Health and Family Welfare, Government of India",
        "condition": "hypertension",
        "publication_date": "May 2016",
        "date_type": "unspecified",
        "version": None,
        "jurisdiction": "India",
        "source_url": (
            "https://clinicalestablishments.mohfw.gov.in/sites/default/files/"
            "standard-treatment-guidelines/6591.pdf"
        ),
        "document_status": "current",
        "licence_note": MOHFW_LICENCE_NOTE,
        "rel_path": "mohfw_stg/mohfw_stg_hypertension_quickref.pdf",
        "relevant_page_ranges": "1-54",
        "notes": (
            "Status: current. Printed date: May 2016 (date_type: unspecified; printed on cover, "
            "meaning unstated). Clinical practice guidelines with quick reference flowcharts."
        ),
    },
    {
        "doc_id": "mohfw_t2dm_001",
        "document_name": "MoHFW Standard Treatment Guidelines - Endocrinology (Diabetes Mellitus)",
        "issuing_organization": "Ministry of Health and Family Welfare, Government of India",
        "condition": "type_2_diabetes",
        "publication_date": None,
        "date_type": None,
        "version": None,
        "jurisdiction": "India",
        "source_url": (
            "https://clinicalestablishments.mohfw.gov.in/sites/default/files/"
            "standard-treatment-guidelines/3601.pdf"
        ),
        "document_status": "current",
        "licence_note": MOHFW_LICENCE_NOTE,
        "rel_path": "mohfw_stg/mohfw_stg_endocrinology_diabetes.pdf",
        "relevant_page_ranges": "6-21",
        "notes": (
            "Status: current (no publication date printed in document). Endocrinology STG covering "
            "diagnostic criteria, treatment goals, and anti-diabetic regimens on pages 6-21."
        ),
    },
]


def build_inventory(data_dir: Path) -> list[InventoryRecord]:
    """Build inventory records by verifying files on disk against the catalog.

    Args:
        data_dir: Path to guideline_chatbot/data directory.

    Returns:
        List of InventoryRecord objects.
    """
    raw_dir = data_dir / "raw"
    records: list[InventoryRecord] = []

    for item in DOCUMENT_CATALOG:
        rel_path = str(item.get("rel_path") or "")
        file_path = raw_dir / rel_path
        if not file_path.is_file():
            logger.warning("Catalog file not found on disk: %s", file_path)
            continue

        sha256 = compute_sha256(file_path)
        page_count, text_extractable = get_pdf_metadata(file_path)
        rel_local_path = f"guideline_chatbot/data/raw/{rel_path}"

        record = InventoryRecord(
            doc_id=str(item.get("doc_id") or ""),
            document_name=str(item.get("document_name") or ""),
            issuing_organization=str(item.get("issuing_organization") or ""),
            condition=str(item.get("condition") or ""),
            publication_date=item.get("publication_date"),
            date_type=item.get("date_type"),
            version=item.get("version"),
            jurisdiction=str(item.get("jurisdiction") or "unknown"),
            source_url=str(item.get("source_url") or ""),
            document_status=str(item.get("document_status") or "unknown"),
            licence_note=item.get("licence_note"),
            local_path=rel_local_path,
            sha256=sha256,
            page_count=page_count,
            text_extractable=text_extractable,
            relevant_page_ranges=item.get("relevant_page_ranges"),
            notes=item.get("notes"),
        )
        records.append(record)

    return records


def write_inventory_csv(records: list[InventoryRecord], output_path: Path) -> None:
    """Write inventory records to CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()
        for record in records:
            row = record.model_dump()
            for key in row:
                if row[key] is None:
                    row[key] = ""
            writer.writerow(row)
    logger.info("Wrote %d records to %s", len(records), output_path)


def write_inventory_json(records: list[InventoryRecord], output_path: Path) -> None:
    """Write inventory records to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = [record.model_dump() for record in records]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    logger.info("Wrote %d records to %s", len(records), output_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    data_dir = Path(__file__).parent.parent / "data"
    inventory_dir = data_dir / "inventory"

    records = build_inventory(data_dir)
    write_inventory_csv(records, inventory_dir / "source_inventory.csv")
    write_inventory_json(records, inventory_dir / "source_inventory.json")
    print(f"Inventory successfully created with {len(records)} verified guideline records.")


if __name__ == "__main__":
    main()
