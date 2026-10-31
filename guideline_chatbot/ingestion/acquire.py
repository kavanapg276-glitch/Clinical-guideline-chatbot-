"""Dataset acquisition module for clinical guideline PDFs.

Downloads PDFs from official sources with:
- Configurable User-Agent header
- Exponential backoff retry (3 attempts, 2/4/8s delays)
- 2-second minimum delay between requests
- SHA-256 hash computation on download
- Page count extraction via PyMuPDF
- Text-extractability detection (first 5 pages sampled)
- Structured logging (no print statements)
"""

from __future__ import annotations

import hashlib
import logging
import time
from pathlib import Path
from typing import Any

import pymupdf
import requests
import yaml
from bs4 import BeautifulSoup
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DownloadResult(BaseModel):
    """Result of a single file download attempt."""

    doc_id: str
    document_name: str
    issuing_organization: str
    condition: str
    source_url: str
    local_path: str | None = None
    sha256: str | None = None
    file_size_bytes: int | None = None
    page_count: int | None = None
    text_extractable: bool | None = None
    download_status: str = "pending"  # success | failed | skipped
    error_message: str | None = None
    jurisdiction: str = "unknown"
    relevant_page_ranges: str | None = None
    notes: str | None = None


def load_settings(config_path: Path | None = None) -> dict[str, Any]:
    """Load settings from YAML config file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "settings.yaml"
    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
        if isinstance(data, dict):
            return data
        return {}


def _get_session(settings: dict[str, Any]) -> requests.Session:
    """Create a requests session with configured headers."""
    session = requests.Session()
    downloader_cfg = settings.get("downloader", {})
    session.headers.update(
        {
            "User-Agent": downloader_cfg.get(
                "user_agent",
                "ClinCoherence-Research/0.1 (capstone project)",
            ),
        }
    )
    return session


def _download_with_retry(
    session: requests.Session,
    url: str,
    dest_path: Path,
    settings: dict[str, Any],
) -> tuple[bool, str | None]:
    """Download a file with exponential backoff retry.

    Returns:
        Tuple of (success: bool, error_message: str | None).
    """
    downloader_cfg = settings.get("downloader", {})
    max_retries = downloader_cfg.get("retry_attempts", 3)
    backoff_base = downloader_cfg.get("retry_backoff_base", 2)
    timeout = downloader_cfg.get("timeout_seconds", 60)

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                "Download attempt %d/%d: %s",
                attempt,
                max_retries,
                url,
            )
            response = session.get(url, timeout=timeout, stream=True, allow_redirects=True)
            response.raise_for_status()

            # Check content type — warn if not PDF but still save
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower() and "octet-stream" not in content_type.lower():
                logger.warning(
                    "Unexpected Content-Type '%s' for %s — saving anyway",
                    content_type,
                    url,
                )

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(
                "Downloaded successfully: %s (%d bytes)", dest_path.name, dest_path.stat().st_size
            )
            return True, None

        except requests.exceptions.RequestException as e:
            error_msg = f"Attempt {attempt}/{max_retries} failed for {url}: {e}"
            logger.warning(error_msg)
            if attempt < max_retries:
                wait_time = backoff_base**attempt
                logger.info("Retrying in %ds...", wait_time)
                time.sleep(wait_time)
            else:
                return False, f"All {max_retries} attempts failed. Last error: {e}"

    return False, "Unexpected: exited retry loop without result"


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def get_pdf_metadata(file_path: Path) -> tuple[int, bool]:
    """Extract page count and text-extractability from a PDF.

    Text extractability is determined by sampling the first 5 pages.
    If at least one page has >50 characters of extracted text, it is
    considered text-extractable.

    Returns:
        Tuple of (page_count, text_extractable).
    """
    try:
        doc = pymupdf.open(str(file_path))
        page_count = len(doc)
        text_extractable = False
        sample_pages = min(5, page_count)
        for i in range(sample_pages):
            page_text = doc[i].get_text().strip()
            if len(page_text) > 50:
                text_extractable = True
                break
        doc.close()
        return page_count, text_extractable
    except Exception as e:
        logger.error("Failed to read PDF metadata for %s: %s", file_path, e)
        return 0, False


def _delay(settings: dict[str, Any]) -> None:
    """Respect delay between requests."""
    delay = settings.get("downloader", {}).get("request_delay_seconds", 2)
    time.sleep(delay)


# ---------------------------------------------------------------------------
# Source-specific download functions
# ---------------------------------------------------------------------------


def download_mohfw(
    session: requests.Session,
    data_dir: Path,
    settings: dict[str, Any],
) -> list[DownloadResult]:
    """Download MoHFW Standard Treatment Guidelines for HTN and T2DM.

    Uses verified official STG document URLs from clinicalestablishments.mohfw.gov.in.
    """
    results: list[DownloadResult] = []
    raw_dir = data_dir / "raw" / "mohfw_stg"
    raw_dir.mkdir(parents=True, exist_ok=True)

    base_url = "https://clinicalestablishments.mohfw.gov.in"
    candidates: list[dict[str, Any]] = [
        {
            "doc_id": "mohfw_htn_001",
            "document_name": "MoHFW STG - Hypertension (Background Document)",
            "condition": "hypertension",
            "url": f"{base_url}/sites/default/files/standard-treatment-guidelines/5191.pdf",
            "filename": "mohfw_stg_hypertension_full.pdf",
            "relevant_page_ranges": "1-144",
            "notes": (
                "Standalone Standard Treatment Guideline for Hypertension (Background Document)"
            ),
        },
        {
            "doc_id": "mohfw_htn_002",
            "document_name": "MoHFW STG - Hypertension (Quick Reference Guide)",
            "condition": "hypertension",
            "url": f"{base_url}/sites/default/files/standard-treatment-guidelines/6591.pdf",
            "filename": "mohfw_stg_hypertension_quickref.pdf",
            "relevant_page_ranges": "1-54",
            "notes": "Quick Reference Guide for Hypertension",
        },
        {
            "doc_id": "mohfw_t2dm_001",
            "document_name": "MoHFW STG - Endocrinology (Diabetes Mellitus)",
            "condition": "type_2_diabetes",
            "url": f"{base_url}/sites/default/files/standard-treatment-guidelines/3601.pdf",
            "filename": "mohfw_stg_endocrinology_diabetes.pdf",
            "relevant_page_ranges": "6-21",
            "notes": (
                "Endocrinology STG covering Type 2 Diabetes Mellitus diagnosis and "
                "management (pages 6-21)"
            ),
        },
    ]

    for candidate in candidates:
        result = DownloadResult(
            doc_id=candidate["doc_id"],
            document_name=candidate["document_name"],
            issuing_organization="MoHFW, Government of India",
            condition=candidate["condition"],
            source_url=candidate["url"],
            jurisdiction="India",
            relevant_page_ranges=candidate.get("relevant_page_ranges"),
            notes=candidate.get("notes"),
        )

        dest_path = raw_dir / candidate["filename"]
        _delay(settings)
        success, error = _download_with_retry(session, candidate["url"], dest_path, settings)

        if success:
            with open(dest_path, "rb") as f:
                header = f.read(10)
            if header.startswith(b"%PDF-"):
                result.local_path = str(dest_path.relative_to(data_dir.parent))
                result.sha256 = compute_sha256(dest_path)
                result.file_size_bytes = dest_path.stat().st_size
                result.page_count, result.text_extractable = get_pdf_metadata(dest_path)
                result.download_status = "success"
            else:
                result.download_status = "failed"
                result.error_message = "Downloaded content was not a valid PDF"
        else:
            result.download_status = "failed"
            result.error_message = error

        results.append(result)

    return results


def download_icmr(
    session: requests.Session,
    data_dir: Path,
    settings: dict[str, Any],
) -> list[DownloadResult]:
    """Download ICMR Standard Treatment Workflows for HTN and T2DM.

    Uses verified direct PDF URLs from ICMR STWs repository.
    """
    results: list[DownloadResult] = []
    raw_dir = data_dir / "raw" / "icmr_stw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    candidates = [
        {
            "doc_id": "icmr_htn_001",
            "document_name": "ICMR STW - Hypertension in Adults",
            "condition": "hypertension",
            "url": "https://www.icmr.gov.in/icmrobject/uploads/STWs/1778941063_hypertensioninadults_final.pdf",
            "filename": "icmr_htn_hypertension_in_adults.pdf",
        },
        {
            "doc_id": "icmr_t2dm_001",
            "document_name": "ICMR STW - Diabetes Mellitus Type 2",
            "condition": "type_2_diabetes",
            "url": "https://www.icmr.gov.in/icmrobject/uploads/STWs/1726567245_diabetes_mellitus_type_2.pdf",
            "filename": "icmr_t2dm_diabetes_type2.pdf",
        },
    ]

    for candidate in candidates:
        result = DownloadResult(
            doc_id=candidate["doc_id"],
            document_name=candidate["document_name"],
            issuing_organization="ICMR / DHR, Government of India",
            condition=candidate["condition"],
            source_url=candidate["url"],
            jurisdiction="India",
        )

        dest_path = raw_dir / candidate["filename"]
        _delay(settings)
        success, error = _download_with_retry(session, candidate["url"], dest_path, settings)

        if success:
            with open(dest_path, "rb") as f:
                header = f.read(10)
            if header.startswith(b"%PDF-"):
                result.local_path = str(dest_path.relative_to(data_dir.parent))
                result.sha256 = compute_sha256(dest_path)
                result.file_size_bytes = dest_path.stat().st_size
                result.page_count, result.text_extractable = get_pdf_metadata(dest_path)
                result.download_status = "success"
            else:
                result.download_status = "failed"
                result.error_message = "Downloaded content was not a valid PDF"
        else:
            result.download_status = "failed"
            result.error_message = error

        results.append(result)

    return results


def download_who(
    session: requests.Session,
    data_dir: Path,
    settings: dict[str, Any],
) -> list[DownloadResult]:
    """Download WHO guidelines for HTN and T2DM.

    Uses verified direct bitstream URLs from WHO IRIS.
    """
    results: list[DownloadResult] = []
    raw_dir = data_dir / "raw" / "who"
    raw_dir.mkdir(parents=True, exist_ok=True)

    candidates = [
        {
            "doc_id": "who_htn_001",
            "document_name": (
                "WHO Guideline for Pharmacological Treatment of Hypertension in Adults (2021)"
            ),
            "condition": "hypertension",
            "url": "https://iris.who.int/server/api/core/bitstreams/f062769d-f075-4a00-87af-0a2106e0bd04/content",
            "filename": "who_htn_pharmacological_treatment_2021.pdf",
            "landing_url": "https://www.who.int/publications/i/item/9789240033986",
        },
        {
            "doc_id": "who_t2dm_001",
            "document_name": "WHO HEARTS-D: Diagnosis and Management of Type 2 Diabetes (2020)",
            "condition": "type_2_diabetes",
            "url": "https://iris.who.int/server/api/core/bitstreams/2a0b4f68-7155-4ad1-b543-945791e31830/content",
            "filename": "who_t2dm_hearts_d_2020.pdf",
            "landing_url": "https://www.who.int/publications/i/item/WHO-UCN-NCD-20.1",
        },
    ]

    for candidate in candidates:
        result = DownloadResult(
            doc_id=candidate["doc_id"],
            document_name=candidate["document_name"],
            issuing_organization="World Health Organization",
            condition=candidate["condition"],
            source_url=candidate["landing_url"],
            jurisdiction="International",
        )

        dest_path = raw_dir / candidate["filename"]
        _delay(settings)

        success, error = _download_with_retry(session, candidate["url"], dest_path, settings)

        if success:
            # Verify valid PDF header
            with open(dest_path, "rb") as f:
                header = f.read(10)
            if header.startswith(b"%PDF-"):
                result.local_path = str(dest_path.relative_to(data_dir.parent))
                result.sha256 = compute_sha256(dest_path)
                result.file_size_bytes = dest_path.stat().st_size
                result.page_count, result.text_extractable = get_pdf_metadata(dest_path)
                result.download_status = "success"
            else:
                result.download_status = "failed"
                result.error_message = "Downloaded content was not a valid PDF"
        else:
            result.download_status = "failed"
            result.error_message = error

        results.append(result)

    return results


def download_nice(
    session: requests.Session,
    data_dir: Path,
    settings: dict[str, Any],
) -> list[DownloadResult]:
    """Download NICE guidelines for HTN and T2DM.

    Strategy: Scrape the guidance page to find the dynamically generated
    PDF download URL. NICE PDFs are not at static URLs.
    """
    results: list[DownloadResult] = []
    raw_dir = data_dir / "raw" / "nice"
    raw_dir.mkdir(parents=True, exist_ok=True)

    candidates = [
        {
            "doc_id": "nice_htn_001",
            "document_name": "NICE NG136: Hypertension in Adults — Diagnosis and Management",
            "condition": "hypertension",
            "guidance_url": "https://www.nice.org.uk/guidance/ng136",
            "filename": "nice_ng136_hypertension.pdf",
        },
        {
            "doc_id": "nice_t2dm_001",
            "document_name": "NICE NG28: Type 2 Diabetes in Adults — Management",
            "condition": "type_2_diabetes",
            "guidance_url": "https://www.nice.org.uk/guidance/ng28",
            "filename": "nice_ng28_type2_diabetes.pdf",
        },
    ]

    for candidate in candidates:
        result = DownloadResult(
            doc_id=candidate["doc_id"],
            document_name=candidate["document_name"],
            issuing_organization="NICE (National Institute for Health and Care Excellence)",
            condition=candidate["condition"],
            source_url=candidate["guidance_url"],
            jurisdiction="United Kingdom",
        )

        dest_path = raw_dir / candidate["filename"]
        _delay(settings)

        # Step 1: Fetch the guidance page to find the PDF link
        pdf_url = None
        logger.info("Fetching NICE guidance page: %s", candidate["guidance_url"])
        try:
            resp = session.get(
                candidate["guidance_url"],
                timeout=settings.get("downloader", {}).get("timeout_seconds", 60),
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Look for PDF download links — NICE typically uses links containing
            # "resources" and "pdf" in the href
            for link in soup.find_all("a", href=True):
                raw_href = link["href"]
                href = raw_href[0] if isinstance(raw_href, list) and raw_href else str(raw_href)
                link_text = link.get_text(strip=True).lower()
                if "pdf" in href.lower() and (
                    "download" in link_text or "pdf" in link_text or "guidance" in link_text
                ):
                    pdf_url = href if href.startswith("http") else "https://www.nice.org.uk" + href
                    logger.info("Found NICE PDF link: %s", pdf_url)
                    break

            # Also check the /resources page
            if not pdf_url:
                resources_url = candidate["guidance_url"] + "/resources"
                _delay(settings)
                resp2 = session.get(
                    resources_url,
                    timeout=settings.get("downloader", {}).get("timeout_seconds", 60),
                )
                resp2.raise_for_status()
                soup2 = BeautifulSoup(resp2.text, "html.parser")

                for link in soup2.find_all("a", href=True):
                    raw_href = link["href"]
                    href = raw_href[0] if isinstance(raw_href, list) and raw_href else str(raw_href)
                    if ".pdf" in href.lower() or "pdf" in href.lower():
                        pdf_url = (
                            href if href.startswith("http") else "https://www.nice.org.uk" + href
                        )
                        logger.info("Found NICE PDF link from resources page: %s", pdf_url)
                        break

        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch NICE guidance page: %s", e)

        # Step 2: Download the PDF
        if pdf_url:
            _delay(settings)
            success, error = _download_with_retry(session, pdf_url, dest_path, settings)
            if success:
                result.local_path = str(dest_path.relative_to(data_dir.parent))
                result.source_url = pdf_url
                result.sha256 = compute_sha256(dest_path)
                result.file_size_bytes = dest_path.stat().st_size
                result.page_count, result.text_extractable = get_pdf_metadata(dest_path)
                result.download_status = "success"
            else:
                result.download_status = "failed"
                result.error_message = error
        else:
            result.download_status = "failed"
            result.error_message = (
                "Could not find PDF download link on NICE guidance page. "
                "NICE generates PDFs dynamically. "
                f"Please download manually from: {candidate['guidance_url']}"
            )

        results.append(result)

    return results


def log_failures_to_open_questions(
    results: list[DownloadResult],
    docs_dir: Path,
) -> None:
    """Append failed downloads to OPEN_QUESTIONS.md per Standing Rule 10."""
    failures = [r for r in results if r.download_status == "failed"]
    if not failures:
        return

    oq_path = docs_dir / "OPEN_QUESTIONS.md"
    with open(oq_path, "a", encoding="utf-8") as f:
        f.write("\n\n## Failed Downloads — Requires Manual Action\n\n")
        f.write(f"*Logged at: {time.strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        for fail in failures:
            f.write(f"### {fail.document_name}\n\n")
            f.write(f"- **Doc ID:** `{fail.doc_id}`\n")
            f.write(f"- **Organisation:** {fail.issuing_organization}\n")
            f.write(f"- **Condition:** {fail.condition}\n")
            f.write(f"- **URL attempted:** {fail.source_url}\n")
            f.write(f"- **Error:** {fail.error_message}\n")
            f.write("- **Manual download instruction:** Please visit the official page, ")
            f.write("download the PDF manually, and place it in ")
            source_map = {
                "MoHFW": "mohfw_stg",
                "ICMR": "icmr_stw",
                "WHO": "who",
                "World Health": "who",
                "NICE": "nice",
            }
            target_dir = "raw/"
            for key, val in source_map.items():
                if key.lower() in fail.issuing_organization.lower():
                    target_dir = f"raw/{val}/"
                    break
            f.write(f"`guideline_chatbot/data/{target_dir}`\n\n")

    logger.info("Logged %d failed download(s) to %s", len(failures), oq_path)


def run_acquisition(data_dir: Path | None = None) -> list[DownloadResult]:
    """Run the full dataset acquisition pipeline.

    Args:
        data_dir: Path to the data directory. Defaults to guideline_chatbot/data/.

    Returns:
        List of DownloadResult objects for all attempted downloads.
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"

    settings = load_settings()
    session = _get_session(settings)
    all_results: list[DownloadResult] = []

    logger.info("=" * 60)
    logger.info("Starting dataset acquisition")
    logger.info("=" * 60)

    # Download from each source
    logger.info("--- Downloading from WHO (IRIS) ---")
    who_results = download_who(session, data_dir, settings)
    all_results.extend(who_results)

    logger.info("--- Downloading from ICMR ---")
    icmr_results = download_icmr(session, data_dir, settings)
    all_results.extend(icmr_results)

    logger.info("--- Downloading from NICE ---")
    nice_results = download_nice(session, data_dir, settings)
    all_results.extend(nice_results)

    logger.info("--- Downloading from MoHFW ---")
    mohfw_results = download_mohfw(session, data_dir, settings)
    all_results.extend(mohfw_results)

    # Log failures
    docs_dir = data_dir.parent / "docs"
    log_failures_to_open_questions(all_results, docs_dir)

    # Summary
    success_count = sum(1 for r in all_results if r.download_status == "success")
    fail_count = sum(1 for r in all_results if r.download_status == "failed")
    logger.info("=" * 60)
    logger.info(
        "Acquisition complete: %d succeeded, %d failed, %d total",
        success_count,
        fail_count,
        len(all_results),
    )
    logger.info("=" * 60)

    return all_results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    results = run_acquisition()
    for r in results:
        status_icon = "✓" if r.download_status == "success" else "✗"
        logger.info(
            "%s [%s] %s — %s",
            status_icon,
            r.doc_id,
            r.document_name,
            r.download_status,
        )
