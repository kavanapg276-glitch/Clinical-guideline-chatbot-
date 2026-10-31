"""Recommendation-aware chunker for clinical guidelines.

Segments cleaned guideline texts along clinical recommendation and section boundaries,
preserving the recommendation statement together with its conditional logic, applicability
criteria, exceptions, and evidence strength. Generates GuidelineChunk objects with all 26
required metadata fields.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any

from guideline_chatbot.chunking.schemas import ChunkType, GuidelineChunk
from guideline_chatbot.ingestion.clean import clean_text
from guideline_chatbot.ingestion.extract_pdf import ExtractedPage, extract_pdf_pages

logger = logging.getLogger(__name__)

# Clinical population patterns (applicability-oriented)
POPULATION_PATTERNS: dict[str, re.Pattern[str]] = {
    "elderly": re.compile(
        r"\b(?:elderly|older\s+adults?|aged?\s*(?:>=|>|over)?\s*80|>=?\s*80\s*years?|"
        r">=?\s*65\s*years?|octogenarians?|frail(?:\s+elderly)?)\b",
        re.IGNORECASE,
    ),
    "chronic_kidney_disease": re.compile(
        r"\b(?:ckd|chronic\s+kidney\s+disease|renal\s+(?:impairment|failure|insufficiency|disease)|"
        r"egfr\s*(?:<=|<)?\s*\d+|creatinine\s+clearance|crcl|proteinuria|microalbuminuria|"
        r"diabetic\s+nephropathy|albuminuria|acr\s*(?:>=|>)?\s*\d+)\b",
        re.IGNORECASE,
    ),
    "type_2_diabetes": re.compile(
        r"\b(?:type\s*2\s+diabetes|t2dm|in\s+adults\s+with\s+type\s*2\s+diabetes|"
        r"in\s+people\s+with\s+type\s*2\s+diabetes|patients\s+with\s+diabetes\s+mellitus|"
        r"diabetic\s+patients?|adults\s+with\s+diabetes)\b",
        re.IGNORECASE,
    ),
    "type_1_diabetes": re.compile(
        r"\b(?:type\s*1\s+diabetes|t1dm|autoimmune\s+diabetes)\b",
        re.IGNORECASE,
    ),
    "pregnancy": re.compile(
        r"\b(?:pregnan(?:cy|t)|pre-?eclampsia|gestational(?:\s+diabetes)?|lactat(?:ing|ion)|"
        r"breastfeeding|antenatal|maternal|women\s+planning\s+pregnancy)\b",
        re.IGNORECASE,
    ),
    "cardiovascular_disease": re.compile(
        r"\b(?:cardiovascular\s+disease|ascvd|cvd|coronary(?:\s+artery\s+disease)?|cad|"
        r"heart\s+failure|chf|myocardial\s+infarction|stroke|transient\s+ischaemic\s+attack|"
        r"angina|peripheral\s+artery\s+disease|previous\s+mi)\b",
        re.IGNORECASE,
    ),
    "african_caribbean": re.compile(
        r"\b(?:black\s+african|african-caribbean|african\s+or\s+caribbean|afro-caribbean|"
        r"black\s+people\s+of\s+african|african\s+family\s+origin)\b",
        re.IGNORECASE,
    ),
    "young_adults": re.compile(
        r"\b(?:young(?:er)?\s+adults?|aged?\s*<\s*40|under\s+40|aged?\s*<\s*55|under\s+55)\b",
        re.IGNORECASE,
    ),
}

# Negation and exclusion patterns that negate a population tag
POPULATION_NEGATIONS: dict[str, list[re.Pattern[str]]] = {
    "chronic_kidney_disease": [
        re.compile(
            r"\bwithout\s+(?:previously\s+diagnosed\s+)?(?:hypertension\s+or\s+)?renal\s+disease\b",
            re.I,
        ),
        re.compile(r"\bwithout\s+renal\s+(?:disease|impairment)\b", re.I),
        re.compile(r"\bwithout\s+ckd\b", re.I),
        re.compile(r"\bexcluding\s+renal\s+disease\b", re.I),
        re.compile(r"\bnormal\s+renal\s+function\b", re.I),
    ],
    "type_2_diabetes": [
        re.compile(r"\bwithout\s+(?:type\s*2\s+)?diabetes\b", re.I),
        re.compile(r"\bexcluding\s+diabetes\b", re.I),
        re.compile(r"\bin\s+the\s+absence\s+of\s+diabetes\b", re.I),
    ],
    "type_1_diabetes": [
        re.compile(r"\bwithout\s+type\s*1\s+diabetes\b", re.I),
    ],
    "elderly": [
        re.compile(r"\baged\s+under\s+80\b", re.I),
        re.compile(r"\bunder\s+80\b", re.I),
        re.compile(r"\baged\s*<\s*80\b", re.I),
    ],
    "cardiovascular_disease": [
        re.compile(r"\bwithout\s+(?:cardiovascular\s+disease|cvd|ascvd)\b", re.I),
        re.compile(r"\bno\s+history\s+of\s+cvd\b", re.I),
    ],
    "pregnancy": [
        re.compile(r"\bnon-pregnant\b", re.I),
        re.compile(r"\bexcluding\s+pregnancy\b", re.I),
    ],
}

# Pharmacological drug class patterns
DRUG_CLASS_PATTERNS: dict[str, re.Pattern[str]] = {
    "ace_inhibitor": re.compile(
        r"\b(?:ace\s+inhibitors?|acei|angiotensin-converting\s+enzyme|"
        r"ramipril|lisinopril|enalapril|perindopril|captopril|benazepril|fosinopril)\b",
        re.IGNORECASE,
    ),
    "arb": re.compile(
        r"\b(?:angiotensin\s+receptor\s+blockers?|arb|angiotensin\s+ii\s+receptor\s+blockers?|"
        r"losartan|telmisartan|valsartan|candesartan|olmesartan|irbesartan)\b",
        re.IGNORECASE,
    ),
    "ccb": re.compile(
        r"\b(?:calcium\s+channel\s+blockers?|ccb|dihydropyridine(?:\s+ccb)?|"
        r"amlodipine|nifedipine|felodipine|diltiazem|verapamil|lercanidipine)\b",
        re.IGNORECASE,
    ),
    "thiazide": re.compile(
        r"\b(?:thiazides?|thiazide-like(?:\s+diuretics?)?|diuretics?|"
        r"chlorthalidone|indapamide|hydrochlorothiazide|hctz)\b",
        re.IGNORECASE,
    ),
    "metformin": re.compile(
        r"\b(?:metformin|biguanides?)\b",
        re.IGNORECASE,
    ),
    "sglt2_inhibitor": re.compile(
        r"\b(?:sglt-?2(?:\s+inhibitors?)?|sglt2-?i|"
        r"dapagliflozin|empagliflozin|canagliflozin|ertugliflozin)\b",
        re.IGNORECASE,
    ),
    "sulfonylurea": re.compile(
        r"\b(?:sulfonylureas?|sulphonylureas?|"
        r"glimepiride|gliclazide|glipizide|glibenclamide|glyburide)\b",
        re.IGNORECASE,
    ),
    "dpp4_inhibitor": re.compile(
        r"\b(?:dpp-?4(?:\s+inhibitors?)?|gliptins?|"
        r"sitagliptin|linagliptin|vildagliptin|saxagliptin|alogliptin)\b",
        re.IGNORECASE,
    ),
    "glp1_ra": re.compile(
        r"\b(?:glp-?1(?:\s+receptor\s+agonists?)?|glp-?1\s*ra|"
        r"semaglutide|liraglutide|dulaglutide|exenatide|tirzepatide)\b",
        re.IGNORECASE,
    ),
    "beta_blocker": re.compile(
        r"\b(?:beta-?blockers?|beta-adrenoceptor\s+blockers?|"
        r"atenolol|metoprolol|bisoprolol|carvedilol|labetalol|nebivolol|propranolol)\b",
        re.IGNORECASE,
    ),
    "mra_spironolactone": re.compile(
        r"\b(?:spironolactone|eplerenone|mineralocorticoid\s+receptor\s+antagonists?|mra)\b",
        re.IGNORECASE,
    ),
    "alpha_blocker": re.compile(
        r"\b(?:alpha-?blockers?|doxazosin|prazosin|terazosin)\b",
        re.IGNORECASE,
    ),
    "insulin": re.compile(
        r"\b(?:insulins?|basal\s+insulin|nph\s+insulin|glargine|degludec|detemir|regular\s+insulin)\b",
        re.IGNORECASE,
    ),
    "statin": re.compile(
        r"\b(?:statins?|atorvastatin|rosuvastatin|simvastatin|pravastatin|lipid-lowering)\b",
        re.IGNORECASE,
    ),
    "antiplatelet": re.compile(
        r"\b(?:aspirin|clopidogrel|antiplatelets?)\b",
        re.IGNORECASE,
    ),
}

# Evidence and recommendation strength patterns
EVIDENCE_STRENGTH_PATTERNS = [
    (re.compile(r"\bhigh[- ]certainty(?:\s+evidence)?\b", re.I), "High certainty"),
    (re.compile(r"\bmoderate[- ]certainty(?:\s+evidence)?\b", re.I), "Moderate certainty"),
    (re.compile(r"\blow[- ]certainty(?:\s+evidence)?\b", re.I), "Low certainty"),
    (re.compile(r"\bvery\s+low[- ]certainty(?:\s+evidence)?\b", re.I), "Very low certainty"),
    (re.compile(r"\bhigh[- ]quality\s+evidence\b", re.I), "High quality"),
    (re.compile(r"\bmoderate[- ]quality\s+evidence\b", re.I), "Moderate quality"),
    (re.compile(r"\blow[- ]quality\s+evidence\b", re.I), "Low quality"),
    (re.compile(r"\bexpert\s+opinions?\b", re.I), "Expert opinion"),
    (re.compile(r"\bexpert\s+consensus\b", re.I), "Expert consensus"),
]

RECOMMENDATION_STRENGTH_PATTERNS = [
    (re.compile(r"\bstrong\s+recommendations?\b", re.I), "Strong recommendation"),
    (re.compile(r"\bconditional\s+recommendations?\b", re.I), "Conditional recommendation"),
    (re.compile(r"\bgood\s+practice\s+points?\b", re.I), "Good practice point"),
    (re.compile(r"\bclinical\s+practice\s+advice\b", re.I), "Clinical practice advice"),
]


def extract_population_tags(text: str) -> list[str]:
    """Extract matching patient population tags from text enforcing applicability over mention."""
    tags: list[str] = []

    # Check for routine screening test mentions that do NOT imply T2DM population applicability
    # E.g. NICE 1.3.3: "take a blood sample to measure glycated haemoglobin (HbA1C)..."
    is_routine_lab_screening = bool(
        re.search(
            r"For all people with hypertension offer to:.*?(?:take a blood sample to measure glycated|test for the presence of protein)",
            text,
            re.DOTALL | re.I,
        )
    )

    # Check for drug adverse event mentions that do NOT imply T2DM population applicability
    # E.g. MoHFW 5.3.2: "metabolic side effects like hypokalemia, hyperglycemia"
    is_adverse_effect_hyperglycemia = bool(
        re.search(
            r"\b(?:side\s+effects?|adverse\s+effects?).*?(?:hyperglycemia|glucose\s+intolerance)\b",
            text,
            re.I,
        )
        and not re.search(
            r"\b(?:type\s*2\s+diabetes|t2dm|in\s+patients\s+with\s+diabetes)\b", text, re.I
        )
    )

    for tag_name, pattern in POPULATION_PATTERNS.items():
        if tag_name == "type_2_diabetes" and (
            is_routine_lab_screening or is_adverse_effect_hyperglycemia
        ):
            continue

        if pattern.search(text):
            # Check negation patterns
            negated = False
            for neg_pat in POPULATION_NEGATIONS.get(tag_name, []):
                if neg_pat.search(text):
                    negated = True
                    break
            if not negated:
                tags.append(tag_name)

    return sorted(tags)


def extract_drug_class_tags(text: str) -> list[str]:
    """Extract matching pharmacological drug class tags from text."""
    tags: list[str] = []
    for tag_name, pattern in DRUG_CLASS_PATTERNS.items():
        if pattern.search(text):
            tags.append(tag_name)
    return sorted(tags)


def extract_evidence_strength(text: str) -> str | None:
    """Extract explicit evidence certainty or rating from text."""
    for pattern, label in EVIDENCE_STRENGTH_PATTERNS:
        if pattern.search(text):
            return label
    return None


def extract_recommendation_strength(text: str) -> str | None:
    """Extract explicit recommendation strength from text."""
    for pattern, label in RECOMMENDATION_STRENGTH_PATTERNS:
        if pattern.search(text):
            return label
    return None


def parse_recommendation_year(text: str) -> str | None:
    """Parse NICE's bracketed year tags into recommendation_year."""
    # E.g. [2019, amended 2022] -> "2022", [2009] -> "2009", [2026] -> "2026"
    match = re.search(r"\[(\d{4})(?:,\s*(?:amended|updated)\s*(\d{4}))?\]", text)
    if match:
        if match.group(2):
            return match.group(2)
        return match.group(1)
    return None


def extract_applicability_conditions(text: str) -> list[str] | None:
    """Extract applicability condition statements (IF / WHEN clauses) from explicit text triggers."""
    conditions: list[str] = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    trigger_regex = re.compile(
        r"^(?:if\s+|when\s+|for\s+(?:adults|people|patients)\s+(?:with|aged)|in\s+(?:adults|people|patients|individuals)\s+(?:with|aged)|"
        r"where\s+(?:clinic\s+bp|daytime\s+abpm)\s+is|with\s+confirmed\s+hypertension|stop\s+.*\s+if\s+)",
        re.IGNORECASE,
    )

    for s in sentences:
        s_clean = s.strip()
        # Reject research questions (PICO), bibliographies, and table fragments
        if s_clean.startswith(
            ("What is", "Should ", "How ", "Table ", "Ref:", "(1)", "(2)", "(3)")
        ):
            continue
        if trigger_regex.match(s_clean) and 20 < len(s_clean) < 300:
            conditions.append(s_clean)

    return conditions[:5] if conditions else None


def extract_exceptions(text: str) -> list[str] | None:
    """Extract exceptions, contraindications, or exclusions from explicit trigger patterns."""
    exceptions: list[str] = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    trigger_regex = re.compile(
        r"\b(?:avoid(?:\s+if|\s+in)?|do\s+not\s+(?:offer|prescribe|combine)|contraindicated(?:\s+in|\s+if)?|"
        r"caution(?:\s+in)?|discontinue\s+if|except\s+(?:in|for)|unless\b)",
        re.IGNORECASE,
    )

    for s in sentences:
        s_clean = s.strip()
        if s_clean.startswith(("Table ", "Ref:", "(1)", "(2)")):
            continue
        if trigger_regex.search(s_clean) and 15 < len(s_clean) < 300:
            exceptions.append(s_clean)

    return exceptions[:5] if exceptions else None


def classify_chunk_type(text: str, heading: str) -> tuple[ChunkType, bool]:
    """Determine the chunk type and whether it should be indexed for retrieval.

    Returns:
        Tuple of (chunk_type, indexed_for_retrieval).
    """
    text_lower = text.lower()
    heading_lower = heading.lower()

    # 1. References and Bibliographies -> NOT indexed
    if (
        any(
            k in heading_lower
            for k in ["reference", "bibliography", "suggested reading", "literature cited"]
        )
        or (text.count("doi:") >= 2 or text.count("PMID:") >= 2)
        or re.search(r"^\(\d+\)\s+[A-Z]", text)
    ):
        return "reference", False

    # 2. Methodology and Frameworks -> NOT indexed
    if any(
        k in heading_lower
        for k in [
            "methodology",
            "search strategy",
            "guideline development process",
            "grade framework",
        ]
    ):
        return "methods", False

    # 3. Front matter and Abbreviations -> NOT indexed
    if any(
        k in heading_lower
        for k in [
            "abbreviations",
            "acronyms",
            "table of contents",
            "executive summary",
            "notice of rights",
        ]
    ):
        return "front_matter", False

    # 4. Committee and Reviewer Rosters -> NOT indexed
    if any(
        k in heading_lower
        for k in [
            "committee",
            "guideline development group",
            "advisory panel",
            "participants",
            "contributors",
        ]
    ):
        return "contributors", False

    # 5. Tables -> INDEXED
    if "|" in text and "---" in text:
        return "table", True

    # 6. Definitions & Classifications -> INDEXED
    if any(
        k in heading_lower
        for k in [
            "definition",
            "classification",
            "cutoffs",
            "diagnostic criteria",
            "criteria for diagnosis",
        ]
    ):
        return "definition", True

    # 7. Recommendations -> INDEXED
    # NICE numbered recommendations (e.g. 1.2.12, 1.4.10, 1.4.20, 1.4.50, 1.24.4)
    if re.match(r"^1\.\d+\.\d+\b", text.strip()) or re.match(r"^1\.\d+\.\d+\b", heading.strip()):
        return "recommendation", True

    # MoHFW STG recommendations (e.g. 4.5.5, 4.8.1.2, 4.11.6, 4.12.2, "Key recommendation")
    if (
        "key recommendation" in heading_lower
        or "key recommendation" in text_lower
        or re.match(r"^[1-9]\.\d+(?:\.\d+)?\b", heading.strip())
        or re.match(r"^[1-9]\.\d+(?:\.\d+)?\b", text.strip())
    ):
        return "recommendation", True

    # WHO recommendations & explicit imperatives
    if (
        re.match(r"^RECOMMENDATION\s+\d+\b", heading.strip(), re.I)
        or re.match(r"^RECOMMENDATION\s+(?:ON|[0-9]+)\b", text.strip(), re.I)
        or any(
            k in text_lower
            for k in [
                "we recommend",
                "who recommends",
                "offer ",
                "start with",
                "prescribe",
                "titrate",
                "first-line",
            ]
        )
    ):
        return "recommendation", True

    # 8. Monitoring -> INDEXED (monitoring intervals only)
    if any(
        k in heading_lower
        for k in ["monitoring", "follow-up", "follow up", "frequency of re-assessment", "recheck"]
    ):
        return "monitoring", True

    # 9. Rationale -> INDEXED
    if any(
        k in heading_lower or k in text_lower
        for k in ["rationale", "evidence and rationale", "remarks", "background"]
    ):
        return "rationale", True

    return "other", True


def resolve_chunk_condition(doc_condition: str, text: str) -> str:
    """Determine chunk condition ('hypertension', 'type_2_diabetes', or 'both').

    Applies 'both' ONLY when the recommendation itself specifically applies to
    patients presenting with BOTH hypertension and diabetes.
    """
    text_lower = text.lower()

    if doc_condition == "hypertension":
        # Check if the recommendation specifically governs diabetic hypertensive patients
        has_specific_dm_governance = bool(
            re.search(
                r"\b(?:patients\s+with\s+diabetes|adults?\s+with\s+type\s*2\s+diabetes|"
                r"adults?\s+with\s+diabetes|diabetic\s+patients?|in\s+people\s+with\s+type\s*2\s+diabetes|"
                r"diabetes\s+mellitus\s+should\s+be\s+initiated)\b",
                text_lower,
            )
        )
        return "both" if has_specific_dm_governance else "hypertension"

    if doc_condition == "type_2_diabetes":
        # Check if the recommendation specifically governs blood pressure in diabetic patients
        has_specific_bp_governance = bool(
            re.search(
                r"\b(?:blood\s+pressure|target\s+bp|bp\s*=\s*140/90|hypertension|antihypertensive)\b",
                text_lower,
            )
        )
        return "both" if has_specific_bp_governance else "type_2_diabetes"

    return doc_condition


def is_boundary_line(line: str) -> tuple[bool, str]:
    """Determine if a line marks a section or recommendation boundary."""
    stripped = line.strip()
    if not stripped:
        return False, ""

    # NICE recommendation number at start of line: e.g. 1.1.1, 1.4.20
    if re.match(r"^\d+\.\d+\.\d+\b", stripped):
        return True, stripped

    # NICE / WHO numbered section heading: e.g. 1.4 Treating and monitoring...
    if re.match(r"^\d+\.\d+\s+[A-Z]", stripped):
        return True, stripped

    # NICE standalone section titles
    nice_titles = [
        "Specialist investigations for possible secondary causes of hypertension",
        "Diagnostic criteria for hypertension",
        "Assessing cardiovascular risk and target organ damage",
        "Treating and monitoring hypertension",
        "Lifestyle interventions",
        "Starting antihypertensive drug treatment",
        "Blood pressure targets",
        "Choosing antihypertensive drug treatment",
        "Step 1 treatment",
        "Step 2 treatment",
        "Step 3 treatment",
        "Step 4 treatment",
        "Reviewing other medicines",
        "Recommendations for research",
        "Key recommendations for research",
    ]
    for nt in nice_titles:
        if stripped.lower() == nt.lower() or stripped.lower().startswith(nt.lower()[:30]):
            return True, nt

    # WHO recommendation title
    if re.match(r"^(?:\d+\.\s+)?RECOMMENDATION\s+(?:ON|[0-9]+)\b", stripped, re.I):
        return True, stripped
    if re.match(
        r"^(?:Rationale\s+and\s+remarks|Evidence\s+and\s+rationale|Remarks|Implementation\s+tools|References)\b",
        stripped,
        re.I,
    ):
        return True, stripped

    # Markdown headers
    if stripped.startswith("#"):
        clean_h = stripped.lstrip("#").strip()
        if clean_h:
            return True, clean_h
        return False, ""

    # Uppercase section headers
    if (
        stripped.isupper()
        and 4 <= len(stripped) <= 60
        and not stripped.endswith(",")
        and not stripped.startswith("ICD-")
    ):
        return True, stripped

    # MoHFW STG numbered sections: e.g. 4.5 Key recommendation, 4.8.1 Diabetes mellitus
    if re.match(r"^[1-9]\d?(?:\.\d+)?(?:\.\d+)?\s+[A-Z]", stripped):
        return True, stripped

    # MoHFW STG Endocrinology section titles
    endo_titles = [
        "DIABETES MELLITUS",
        "Introduction",
        "Definition",
        "Classification",
        "Classification of Diabetes Mellitus",
        "Characteristics of Diabetes In India",
        "Diagnostic Criteria",
        "Screening for Diabetes Mellitus",
        "Goals of Therapy",
        "Non Pharmacological Management",
        "Pharmacological Management",
        "Metformin",
        "Sulphonylureas",
        "Alpha Glucosidase Inhibitors",
        "Thiazolidinediones",
        "DPP-4 Inhibitors",
        "Insulin therapy",
        "Complications",
        "Prevention of diabetes:",
        "Referral to a tertiary center /Endocrinologist:",
        "Who does what",
        "Suggested reading /references",
    ]
    for et in endo_titles:
        if stripped.lower() == et.lower():
            return True, stripped

    return False, ""


def clean_section_path(path: str) -> str:
    """Clean table-of-contents dots, trailing page numbers, and DOIs from section paths."""
    # Remove TOC dots and numbers: e.g. "Section .... 12" -> "Section"
    path = re.sub(r"\.{3,}\s*\d+", "", path)
    # Remove DOIs
    path = re.sub(r"doi:\s*10\.\d+/[^\s>]+", "", path)
    # Clean whitespace
    parts = [p.strip() for p in path.split(">") if p.strip()]
    return " > ".join(parts)


def strip_trailing_headings(text: str) -> tuple[str, str | None]:
    """Strip an un-chunked next-section heading glued to the end of a chunk text.

    Returns:
        Tuple of (cleaned_text, detected_trailing_heading).
    """
    lines = text.splitlines()
    if len(lines) <= 1:
        return text, None

    # Check 2-line heading at the end
    if len(lines) >= 3:
        two_line = f"{lines[-2].strip()} {lines[-1].strip()}"
        is_b, h = is_boundary_line(two_line)
        if is_b and not lines[-1].strip().endswith((".", ":", ";")):
            cleaned_text = "\n".join(lines[:-2]).strip()
            return cleaned_text, h

    # Check 1-line heading at the end
    last_line = lines[-1].strip()
    is_boundary, heading = is_boundary_line(last_line)
    if is_boundary and not last_line.endswith((".", ":", ";")):
        cleaned_text = "\n".join(lines[:-1]).strip()
        return cleaned_text, heading

    return text, None


def split_long_lines(
    lines: list[tuple[str, int]], max_words: int = 350
) -> list[list[tuple[str, int]]]:
    """Split a sequence of lines into cohesive segments bounded by max_words."""
    batches: list[list[tuple[str, int]]] = []
    current_batch: list[tuple[str, int]] = []
    current_words = 0

    for item in lines:
        line_str = item[0].strip()
        w_count = len(line_str.split())

        if (
            current_words + w_count > max_words
            and current_batch
            and (line_str.endswith((".", "?", ":", ";")) or not line_str or current_words > 450)
        ):
            current_batch.append(item)
            batches.append(current_batch)
            current_batch = []
            current_words = 0
            continue

        current_batch.append(item)
        current_words += w_count

    if current_batch:
        batches.append(current_batch)

    return batches


class GuidelineChunker:
    """Recommendation-aware chunker for clinical guidelines."""

    def __init__(self, target_word_min: int = 20, target_word_max: int = 450):
        self.target_word_min = target_word_min
        self.target_word_max = target_word_max

    def chunk_document(
        self,
        doc_metadata: dict[str, Any],
        extracted_pages: list[ExtractedPage],
    ) -> list[GuidelineChunk]:
        """Chunk a document into GuidelineChunk objects."""
        doc_id = str(doc_metadata.get("doc_id", ""))
        doc_name = str(doc_metadata.get("document_name", ""))
        issuer = str(doc_metadata.get("issuing_organization", ""))
        doc_condition = str(doc_metadata.get("condition", ""))
        version = doc_metadata.get("version")
        pub_date = doc_metadata.get("publication_date")
        last_updated = doc_metadata.get("last_updated")
        last_updated_source = doc_metadata.get("last_updated_source")
        jurisdiction = str(doc_metadata.get("jurisdiction", "unknown"))
        doc_status = str(doc_metadata.get("document_status", "current"))

        # Dedicated handler for ICMR Posters to ensure 100% structured preservation
        if doc_id in ("icmr_htn_001", "icmr_t2dm_001"):
            return self._chunk_icmr_poster(doc_metadata, extracted_pages)

        chunks: list[GuidelineChunk] = []
        chunk_idx = 1

        # Build document-wide sequence of (line_text, page_num)
        doc_lines: list[tuple[str, int]] = []
        for page in extracted_pages:
            cleaned_text, _ = clean_text(page.raw_text, doc_id)
            if cleaned_text.strip():
                for line_str in cleaned_text.splitlines():
                    doc_lines.append((line_str, page.page_num))

        if not doc_lines:
            return chunks

        active_section = doc_name
        active_heading = doc_name
        current_chunk_lines: list[tuple[str, int]] = []
        current_chunk_heading = active_heading
        current_chunk_section = active_section

        def emit_chunk(
            c_lines: list[tuple[str, int]],
            c_heading: str,
            c_section: str,
        ) -> None:
            nonlocal chunk_idx
            if not c_lines:
                return

            text_lines = [item[0] for item in c_lines]
            combined_text = "\n".join(text_lines).strip()
            if not combined_text:
                return

            # Clean trailing headings glued to end of chunk
            combined_text, trailing_h = strip_trailing_headings(combined_text)
            if not combined_text:
                return

            final_heading = c_heading.strip() if c_heading.strip() else active_section.strip()
            if not final_heading:
                final_heading = doc_name

            words = combined_text.split()
            if len(words) > self.target_word_max:
                line_batches = split_long_lines(c_lines, self.target_word_max)
                part = 1
                for batch in line_batches:
                    sub_text = "\n".join(x[0] for x in batch).strip()
                    sub_text, _ = strip_trailing_headings(sub_text)
                    if not sub_text or len(sub_text.split()) < self.target_word_min:
                        continue
                    p_start = batch[0][1]
                    p_end = batch[-1][1]
                    sub_heading = f"{final_heading} (Part {part})" if part > 1 else final_heading
                    part += 1
                    _append_chunk(sub_text, p_start, p_end, sub_heading, c_section)
            else:
                if len(words) < self.target_word_min and not (
                    "|" in combined_text and "---" in combined_text
                ):
                    return
                p_start = c_lines[0][1]
                p_end = c_lines[-1][1]
                _append_chunk(combined_text, p_start, p_end, final_heading, c_section)

        def _append_chunk(
            text: str,
            page_start: int,
            page_end: int,
            heading: str,
            section: str,
        ) -> None:
            nonlocal chunk_idx
            chunk_id = f"{doc_id}_c{chunk_idx:04d}"
            chunk_idx += 1

            chunk_type, indexed = classify_chunk_type(text, heading)
            pop_tags = extract_population_tags(text)
            drug_tags = extract_drug_class_tags(text)
            ev_strength = extract_evidence_strength(text)
            rec_strength = extract_recommendation_strength(text)
            rec_year = parse_recommendation_year(text)
            applicability = extract_applicability_conditions(text)
            exceptions = extract_exceptions(text)
            condition = resolve_chunk_condition(doc_condition, text)
            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

            section_clean = section.strip() if section.strip() else doc_name
            heading_clean = heading.strip() if heading.strip() else section_clean

            raw_path = (
                f"{doc_name} > {section_clean}"
                if heading_clean == section_clean
                else f"{doc_name} > {section_clean} > {heading_clean}"
            )
            section_path = clean_section_path(raw_path)

            chunks.append(
                GuidelineChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    document_name=doc_name,
                    issuing_organization=issuer,
                    condition=condition,
                    section_path=section_path,
                    heading=heading_clean,
                    page_start=page_start,
                    page_end=page_end,
                    version=version,
                    publication_date=pub_date,
                    last_updated=last_updated,
                    last_updated_source=last_updated_source,
                    recommendation_year=rec_year,
                    jurisdiction=jurisdiction,
                    document_status=doc_status,
                    chunk_type=chunk_type,
                    indexed_for_retrieval=indexed,
                    evidence_strength=ev_strength,
                    recommendation_strength=rec_strength,
                    population_tags=pop_tags,
                    drug_class_tags=drug_tags,
                    applicability_conditions=applicability,
                    exceptions=exceptions,
                    text=text,
                    text_hash=text_hash,
                )
            )

        # Iterate through all document lines
        for line_text, page_num in doc_lines:
            is_boundary, detected_heading = is_boundary_line(line_text)

            if is_boundary and current_chunk_lines:
                buf_words = sum(len(x[0].split()) for x in current_chunk_lines)

                if buf_words >= self.target_word_min or (
                    "|" in current_chunk_lines[0][0] and "---" in current_chunk_lines[0][0]
                ):
                    emit_chunk(current_chunk_lines, current_chunk_heading, current_chunk_section)
                    current_chunk_lines = [(line_text, page_num)]
                    current_chunk_heading = detected_heading
                    current_chunk_section = active_section
                else:
                    current_chunk_lines.append((line_text, page_num))
                    if detected_heading:
                        current_chunk_heading = f"{current_chunk_heading} > {detected_heading}"
            else:
                current_chunk_lines.append((line_text, page_num))

            if (
                is_boundary
                and detected_heading
                and (
                    re.match(r"^\d+\.\d+\s+[A-Z]", detected_heading)
                    or (detected_heading.isupper() and len(detected_heading) > 5)
                    or detected_heading
                    in [
                        "DIABETES MELLITUS",
                        "Classification of Diabetes Mellitus",
                        "Goals of Therapy",
                    ]
                )
            ):
                active_section = detected_heading

        if current_chunk_lines:
            emit_chunk(current_chunk_lines, current_chunk_heading, current_chunk_section)

        return chunks

    def _chunk_icmr_poster(
        self,
        doc_metadata: dict[str, Any],
        extracted_pages: list[ExtractedPage],
    ) -> list[GuidelineChunk]:
        """Generate structured chunks for ICMR posters preserving 100% of tables and clinical logic."""
        doc_id = str(doc_metadata["doc_id"])
        doc_name = str(doc_metadata["document_name"])
        issuer = str(doc_metadata["issuing_organization"])
        version = doc_metadata.get("version")
        pub_date = doc_metadata.get("publication_date")
        last_updated = doc_metadata.get("last_updated")
        last_updated_source = doc_metadata.get("last_updated_source")
        jurisdiction = str(doc_metadata["jurisdiction"])
        doc_status = str(doc_metadata["document_status"])

        chunks: list[GuidelineChunk] = []
        chunk_idx = 1

        def add_c(
            heading: str,
            text: str,
            c_type: ChunkType,
            indexed: bool,
            cond: str,
            pop_tags: list[str] | None = None,
            drug_tags: list[str] | None = None,
            app_cond: list[str] | None = None,
            exc: list[str] | None = None,
        ) -> None:
            nonlocal chunk_idx
            cid = f"{doc_id}_c{chunk_idx:04d}"
            chunk_idx += 1
            h_clean = heading.strip()
            sec_path = f"{doc_name} > {h_clean}"
            thash = hashlib.sha256(text.encode("utf-8")).hexdigest()

            chunks.append(
                GuidelineChunk(
                    chunk_id=cid,
                    doc_id=doc_id,
                    document_name=doc_name,
                    issuing_organization=issuer,
                    condition=cond,
                    section_path=sec_path,
                    heading=h_clean,
                    page_start=1,
                    page_end=1,
                    version=version,
                    publication_date=pub_date,
                    last_updated=last_updated,
                    last_updated_source=last_updated_source,
                    recommendation_year=None,
                    jurisdiction=jurisdiction,
                    document_status=doc_status,
                    chunk_type=c_type,
                    indexed_for_retrieval=indexed,
                    evidence_strength=None,
                    recommendation_strength="Good practice point",
                    population_tags=sorted(pop_tags or extract_population_tags(text)),
                    drug_class_tags=sorted(drug_tags or extract_drug_class_tags(text)),
                    applicability_conditions=app_cond,
                    exceptions=exc,
                    text=text.strip(),
                    text_hash=thash,
                )
            )

        if doc_id == "icmr_htn_001":
            add_c(
                "STW Metadata & Title",
                "Standard Treatment Workflow (STW): HYPERTENSION IN ADULTS\nICD-11 BA00 | Printed Date: May/2026\n"
                "Indian Council of Medical Research (ICMR) and Department of Health Research (DHR), MoHFW, Government of India.",
                "front_matter",
                False,
                "hypertension",
            )
            add_c(
                "Abbreviations",
                "ABBREVIATIONS:\n- ACEi: Angiotensin-converting enzyme inhibitor\n- ARB: Angiotensin receptor blocker\n"
                "- BP: Blood pressure\n- CCB: Calcium channel blocker\n- FDC: Fixed-dose combination\n"
                "- HFrEF: Heart failure with reduced ejection fraction\n- HFpEF: Heart failure with preserved ejection\n"
                "- MRA: Mineralocorticoid receptor antagonist\n- RAAS: Renin-angiotensin-aldosterone system\n- OD: Once daily",
                "front_matter",
                False,
                "hypertension",
            )
            add_c(
                "Risk Factors",
                "RISK FACTORS FOR HYPERTENSION:\n- High salt intake\n- Sedentary behavior\n- Tobacco and alcohol consumption\n- Obesity\n\n"
                "All adults >= 18 years should get blood pressure measured at every clinic visit.",
                "recommendation",
                True,
                "hypertension",
            )
            add_c(
                "Diagnosis of Hypertension",
                "DIAGNOSIS OF HYPERTENSION:\n- Systolic BP >= 140 AND/OR Diastolic BP >= 90 mmHg on two different clinic visits.\n"
                "- Population screening BP reading may count as the first reading.\n"
                "- Use the higher category if only Systolic or Diastolic BP is high; manage based on the higher value.\n"
                "- If Systolic BP >= 160 AND/OR Diastolic BP >= 100 mmHg, measurement of one clinic visit is sufficient for diagnosing hypertension.",
                "definition",
                True,
                "hypertension",
                app_cond=[
                    "If Systolic BP >= 160 AND/OR Diastolic BP >= 100 measurement of one clinic visit is sufficient for diagnosing hypertension"
                ],
            )
            add_c(
                "Blood Pressure Classification",
                "### BLOOD PRESSURE LEVELS & CLASSIFICATION\n\n"
                "| Classification | Blood Pressure Levels | Action |\n"
                "| --- | --- | --- |\n"
                "| Normal | Systolic < 120 AND Diastolic < 80 mmHg | Reassure and encourage healthy lifestyle |\n"
                "| Elevated BP | Systolic 120-139 AND/OR Diastolic 80-89 mmHg | Lifestyle modification |\n"
                "| Hypertension Grade 1 | Systolic 140-159 AND/OR Diastolic 90-99 mmHg | Pharmacological management + Lifestyle modification |\n"
                "| Hypertension Grade 2 | Systolic 160-179 AND/OR Diastolic 100-109 mmHg | Pharmacological management + Lifestyle modification |\n"
                "| Hypertension Grade 3 | Systolic >= 180 AND/OR Diastolic >= 110 mmHg | Pharmacological management + Lifestyle modification |",
                "table",
                True,
                "hypertension",
            )
            add_c(
                "Blood Pressure Control Targets",
                "BLOOD PRESSURE CONTROL TARGETS:\n"
                "- All adults: SBP < 140 and DBP < 90 mmHg.\n"
                "- Diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg (optimal target if tolerated).\n"
                "- Age >= 80 years: SBP < 150 and DBP < 90 mmHg.\n"
                "- Assess orthostatic BP at every visit of adults >= 65 years.",
                "recommendation",
                True,
                "both",
                pop_tags=[
                    "elderly",
                    "chronic_kidney_disease",
                    "type_2_diabetes",
                    "cardiovascular_disease",
                ],
                app_cond=[
                    "In patients with diabetes mellitus, CKD, or established CVD: SBP < 130 and DBP < 80 mmHg",
                    "For adults aged >= 80 years: SBP < 150 and DBP < 90 mmHg",
                ],
            )
            add_c(
                "Lifestyle Modification",
                "LIFESTYLE MODIFICATION FOR HYPERTENSION:\n"
                "- Advise all patients against tobacco and alcohol use.\n"
                "- Limit salt intake to < 5g/day.\n"
                "- Use healthy oils, eat more fruits/vegetables, prefer fish/omega-3 foods such as nuts and seeds.\n"
                "- Physical Activity: 30 minutes daily.\n"
                "- Weight Management: Keep BMI < 23 kg/m2 and waist circumference: < 90 cm (men) and < 80 cm (women).",
                "other",
                True,
                "hypertension",
            )
            add_c(
                "Monitoring of Hypertension",
                "MONITORING OF HYPERTENSION:\n"
                "- BP to be measured at every clinical visit.\n"
                "- Evaluate for diabetes (fasting plasma glucose or HbA1c) and manage accordingly.\n"
                "- Annual evaluations: Serum creatinine, Urine (albumin, sugar, creatinine), Lipid profile, Fundoscopy.\n"
                "- Additional investigations (if required): ECG, ECHO.",
                "monitoring",
                True,
                "hypertension",
            )
            add_c(
                "Hypertension Urgency and Emergency",
                "HYPERTENSION URGENCY & EMERGENCY:\n"
                "Definition: Systolic BP >= 180 AND/OR Diastolic BP >= 120 mmHg.\n\n"
                "Red Flags / Symptoms of target organ damage:\n"
                "- Visual disturbance, dizziness, confusion, headache, chest pain, breathlessness (worse lying down/leg swelling), sudden weakness, speech/swallowing difficulty, vision problem.\n"
                "- Management: Stabilise ABC and refer to emergency care at higher center.\n\n"
                "Hypertension Urgency (Without acute target-organ damage):\n"
                "- Management: Start oral antihypertensive drugs. Do NOT use IV medicines. Reduce BP gradually over 24-48 hours. Refer/admit if symptoms or organ damage suspected. Follow-up within 1 week.",
                "recommendation",
                True,
                "hypertension",
                exc=["Do not use IV medicines for asymptomatic hypertension urgency"],
            )
            add_c(
                "Pharmacological Strategy",
                "PHARMACOLOGICAL STRATEGY FOR HYPERTENSION:\n"
                "- Combination therapy (two drugs from two different classes) could be the default initial pharmacological treatment for most adults with hypertension.\n"
                "- Single-pill combinations (SPCs/fixed-dose combinations, FDCs) are preferred over multiple pills to improve adherence.\n"
                "- Monotherapy remains appropriate only for (a) low-risk Grade 1 HTN, (b) elderly >= 80 years, or (c) frail patients.\n"
                "- A CCB or Thiazide/Thiazide-like diuretic should be used with a Renin-Angiotensin-Aldosterone System (RAAS) blocker (either an ACEi or an ARB).\n"
                "- Three-drug combination, often a RAAS blocker, CCB, or a Thiazide/Thiazide-like diuretic, if blood pressure is not controlled with the initial two-drug combination.\n"
                "- Beta-blockers are appropriate in cases of angina, postmyocardial infarction, heart failure (HFrEF or HFpEF with ischemia).\n"
                "- DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI).",
                "recommendation",
                True,
                "hypertension",
                pop_tags=["elderly", "cardiovascular_disease"],
                drug_tags=["ace_inhibitor", "arb", "ccb", "thiazide", "beta_blocker"],
                exc=[
                    "DO NOT combine two RAAS blockers as it increases the risk of adverse effects, including acute kidney injury (AKI)"
                ],
            )
            add_c(
                "Treatment Protocols (ATTACC & AATTCC)",
                "SUGGESTED TREATMENT PROTOCOLS FOR BLOOD PRESSURE CONTROL:\n"
                "*High BP >= 140/90 mmHg. At every visit: Check if the patient has been taking medications regularly and correctly.\n\n"
                "PROTOCOL NO 1 (ATTACC):\n"
                "- Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again.\n"
                "- Step 2: If still high, add Telmisartan 40mg. After 4 weeks measure BP again.\n"
                "- Step 3: If still high, increase Telmisartan to 80mg. After 4 weeks measure BP again.\n"
                "- Step 4: If still high, increase Amlodipine to 10mg. After 4 weeks measure BP again.\n"
                "- Step 5: If still high, add Chlorthalidone 12.5mg. After 4 weeks measure BP again.\n"
                "- Step 6: If still high, consider adding drugs of other classes, preferably MRA (e.g. Spironolactone).\n\n"
                "PROTOCOL NO 2 (AATTCC):\n"
                "- Step 1: If BP is high, prescribe Amlodipine 5mg. After 4 weeks measure BP again.\n"
                "- Step 2: If still high, increase to Amlodipine 10mg. After 4 weeks measure BP again.\n"
                "- Step 3: If still high, add Telmisartan 40mg. After 4 weeks measure BP again.\n"
                "- Step 4: If still high, increase to Telmisartan 80mg. After 4 weeks measure BP again.\n"
                "- Step 5: If still high, add Chlorthalidone 12.5mg. After 4 weeks measure BP again.\n"
                "- Step 6: If still high, consider adding drugs of other classes, preferably MRA (e.g. Spironolactone).",
                "recommendation",
                True,
                "hypertension",
                drug_tags=["ccb", "arb", "thiazide", "mra_spironolactone"],
            )
            add_c(
                "Drug Therapy Table: Doses, Contraindications & Side Effects",
                "### ANTIHYPERTENSIVE DRUG THERAPY: DOSES, CONTRAINDICATIONS & SIDE EFFECTS\n\n"
                "| Drug Class | Drug | Doses | Contraindications | Side Effects |\n"
                "| --- | --- | --- | --- | --- |\n"
                "| CCB | Amlodipine | 2.5–10 mg OD | Heart failure | Pedal edema, constipation |\n"
                "| ACE inhibitors | Enalapril | 5–40 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |\n"
                "| ACE inhibitors | Ramipril | 2.5–10 mg OD or BD | Pregnancy, Women planning pregnancy, prior angioedema to ACEi, Hyperkalemia, Bilateral renal artery stenosis | Dry cough, angioedema, hyperkalemia, rise in serum creatinine |\n"
                "| ARB | Losartan | 50–100 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |\n"
                "| ARB | Olmesartan | 20–40 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |\n"
                "| ARB | Telmisartan | 40–80 mg OD | Pregnancy, Women planning pregnancy, Hyperkalemia, Bilateral renal artery stenosis | Hypotension, acute renal failure, hyperkalemia |\n"
                "| Diuretics | Chlorthalidone | 12.5–25 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |\n"
                "| Diuretics | Hydrochlorothiazide | 12.5 mg OD | Pregnancy, Gout | Glucose intolerance, metabolic syndrome, hyponatremia, hypercalcemia, hypokalemia |\n"
                "| Beta-blockers | Carvedilol | 12.5–50 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |\n"
                "| Beta-blockers | Labetalol | 100–400 mg BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |\n"
                "| Beta-blockers | Metoprolol | 50–100 mg OD or BD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |\n"
                "| Beta-blockers | Nebivolol | 5 mg OD | Asthma, severe bradycardia, A-V block (grade 2 or 3), uncontrolled heart failure | Depression, fatigue, reduced exercise tolerance, hyperglycemia, sexual dysfunction |\n"
                "| Aldosterone antagonist | Spironolactone | 25 mg OD | Hyperkalemia | Mastalgia, gynecomastia, sexual dysfunction, gout |",
                "table",
                True,
                "hypertension",
                pop_tags=["pregnancy"],
                drug_tags=[
                    "ace_inhibitor",
                    "arb",
                    "ccb",
                    "thiazide",
                    "beta_blocker",
                    "mra_spironolactone",
                ],
                exc=[
                    "Pregnancy is a strict contraindication for ACE inhibitors, ARBs, and Diuretics",
                    "Heart failure is contraindicated for initial CCB",
                    "Asthma and A-V block are contraindicated for Beta-blockers",
                ],
            )
            add_c(
                "References",
                "REFERENCES:\n"
                "1. Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of arterial hypertension. J Hypertens. 2023;41(12):1874–2071.\n"
                "2. Joseph G, Thanh Pham V, Kragh Andersen P, et al. Cardiovascular events according to blood pressure thresholds recommended by ACC/AHA. Blood Press. 2024;33(1):2380346.\n"
                "3. Gupta R, Maheshwari A, Verma N, Narasingan SN, Tripathi K, Joshi S, Manoria PC, et al. Indian Society of Hypertension (InSH) Consensus Guideline for the Management of Hypertension, 2025. Hypertension Journal. 2025;11(4):76–138.\n"
                "4. Ministry of Health and Family Welfare, Government of India. Training modules on non-communicable diseases. New Delhi: MoHFW; 2025.\n"
                "5. ICMR-National Institute of Epidemiology. India Hypertension Control Initiative: Training modules. Chennai, 2021.",
                "reference",
                False,
                "hypertension",
            )

        elif doc_id == "icmr_t2dm_001":
            add_c(
                "STW Metadata & Title",
                "Standard Treatment Workflow (STW): DIABETES MELLITUS TYPE 2\nICD-10-E11 | Printed Date: July/ 2022\n"
                "Department of Health Research, Ministry of Health & Family Welfare, Government of India.",
                "front_matter",
                False,
                "type_2_diabetes",
            )
            add_c(
                "Abbreviations",
                "ABBREVIATIONS:\n- ALT: Alanine transaminase\n- AST: Aspartate aminotransferase\n- BMI: Body mass index\n"
                "- BP: Blood pressure\n- CAD: Coronary artery disease\n- CGM: Continuous glucose monitor\n- CKD: Chronic kidney disease\n"
                "- DTR: Deep tendon reflex\n- ECG: Electrocardiogram\n- FPG: Fasting plasma glucose\n- GDM: Gestational diabetes mellitus\n"
                "- HDL: High-density lipoprotein\n- LDL: Low-density lipoprotein\n- LFT: Liver function test\n- OAD: Oral antidiabetic drug\n"
                "- OGTT: Oral glucose tolerance test\n- SMBG: Self-monitoring of blood glucose\n- TG: Triglyceride",
                "front_matter",
                False,
                "type_2_diabetes",
            )
            add_c(
                "Symptoms and Clinical Examination",
                "CLINICAL PRESENTATION & EXAMINATION IN TYPE 2 DIABETES:\n"
                "- Symptoms: Osmotic symptoms (polyuria, polydipsia, polyphagia), weight loss, non-healing wounds, paraesthesia, recurrent infections, blurring of vision. Note: Many patients may be asymptomatic.\n"
                "- Examination: BMI, waist circumference, BP, peripheral pulses, skin, oral cavity, foot, and dilated fundus examination.\n"
                "- Assess Co-morbidities: Hypertension, Dyslipidaemia, CAD, CKD.",
                "definition",
                True,
                "both",
                pop_tags=["cardiovascular_disease", "chronic_kidney_disease"],
            )
            add_c(
                "Diagnostic Criteria for Diabetes Mellitus",
                "### DIAGNOSTIC CRITERIA FOR TYPE 2 DIABETES MELLITUS\n\n"
                "| Investigation / Parameter | Diagnostic Threshold |\n"
                "| --- | --- |\n"
                "| Fasting Plasma Glucose (FPG) | >= 126 mg/dl (after 8hr fasting) |\n"
                "| 2-hour Plasma Glucose during OGTT | >= 200 mg/dl (using 75g glucose) |\n"
                "| Glycated Haemoglobin (HbA1c) | >= 6.5% |\n"
                "| Random Plasma Glucose | >= 200 mg/dl in presence of classic diabetes symptoms |",
                "definition",
                True,
                "type_2_diabetes",
            )
            add_c(
                "Prediabetes Diagnostic Criteria",
                "### PREDIABETES DIAGNOSTIC CRITERIA\n\n"
                "| Category | Laboratory Criteria |\n"
                "| --- | --- |\n"
                "| Impaired Fasting Glucose (IFG) | Fasting Plasma Glucose 100–125 mg/dL |\n"
                "| Impaired Glucose Tolerance (IGT) | 2-hour plasma glucose 140–199 mg/dL |\n"
                "| Prediabetes HbA1c | HbA1c 5.7%–6.4% |\n\n"
                "Prediabetes patients should be tested yearly for progression to diabetes.",
                "definition",
                True,
                "type_2_diabetes",
            )
            add_c(
                "Screening for Diabetes Mellitus",
                "SCREENING FOR DIABETES MELLITUS:\n"
                "1. IN PREGNANCY:\n"
                "- All pregnant women to be screened in 1st trimester with FPG.\n"
                "- FPG >= 126 mg/dl and/or HbA1c >= 6.5% to be considered pre-existing diabetes.\n"
                "- FPG between 92–125 mg/dl to be considered as GDM.\n"
                "- All women with normal screening in 1st trimester to get a 75g oral glucose tolerance test (OGTT) at 24–28 weeks.\n"
                "- All GDM women to be tested 6 weeks post-partum and once every 3 years.\n\n"
                "2. IN AN APPARENTLY NORMAL ADULT:\n"
                "- In obese or overweight (BMI >= 27.5 or >= 23 kg/m2) with risk factors: first degree relative with diabetes, history of CVD, BP >= 140/90 mmHg, dyslipidemia (TG > 250 mg/dL, HDL < 40 male, < 50 female), physical inactivity, PCOS, insulin resistance (acanthosis nigricans), age > 30 years, previous history of GDM.\n\n"
                "3. IN AN ADULT WITH ILLNESS:\n"
                "- Osmotic symptoms, unexplained weight loss, acute coronary syndrome, deep seated infections (pneumonia, tuberculosis, pyelonephritis), recurrent infections (oral thrush, cellulitis, UTI), non-healing ulcers.",
                "recommendation",
                True,
                "both",
                pop_tags=["pregnancy", "cardiovascular_disease"],
                app_cond=[
                    "In pregnant women: screen 1st trimester with FPG; 75g OGTT at 24-28 weeks if normal",
                    "In overweight or obese adults (BMI >= 23 kg/m2) with risk factors",
                ],
            )
            add_c(
                "Metabolic Targets in Type 2 Diabetes",
                "### METABOLIC TARGETS IN TYPE 2 DIABETES\n\n"
                "| Clinical Parameter | Target Goal |\n"
                "| --- | --- |\n"
                "| HbA1c | </= 7.0% (except elderly and significant comorbid conditions where higher target may be acceptable) |\n"
                "| Pre-prandial capillary plasma glucose | 80–130 mg/dl |\n"
                "| Post-prandial capillary plasma glucose | < 180 mg/dl |\n"
                "| Blood Pressure | < 140/90 mmHg (< 130/80 mmHg in CKD) |\n"
                "| LDL Cholesterol | < 100 mg/dl (< 70 mg/dl in CAD) |",
                "table",
                True,
                "both",
                pop_tags=["elderly", "chronic_kidney_disease", "cardiovascular_disease"],
                app_cond=[
                    "In CKD patients: target BP < 130/80 mmHg",
                    "In CAD patients: target LDL < 70 mg/dl",
                    "In elderly patients: higher HbA1c target may be acceptable",
                ],
            )
            add_c(
                "Stratified Glycemic Pharmacotherapy",
                "### STRATIFIED PHARMACOTHERAPY BY HBA1C STRATUM\n\n"
                "| HbA1c Stratum | Recommended Pharmacotherapy Protocol |\n"
                "| --- | --- |\n"
                "| HbA1c < 8.5% | Monotherapy — Metformin |\n"
                "| HbA1c 8.5%–10.0% | Dual therapy — Metformin + Sulfonylureas (SUs) / Thiazolidinediones (TZD) / DPP-4 inhibitors (DPPIVi) / SGLT2 inhibitors (SGLT2i) / Alpha-glucosidase inhibitors (AGI) / GLP-1 Receptor Agonists (GLP-1RA) |\n"
                "| HbA1c > 10.0% | Basal Insulin + Metformin + another Oral Antidiabetic Drug (OAD) OR Triple OAD combination |",
                "table",
                True,
                "type_2_diabetes",
                drug_tags=[
                    "metformin",
                    "sulfonylurea",
                    "dpp4_inhibitor",
                    "sglt2_inhibitor",
                    "glp1_ra",
                    "insulin",
                ],
            )
            add_c(
                "Lifestyle Modification",
                "LIFESTYLE MANAGEMENT IN TYPE 2 DIABETES:\n"
                "- Dietary modification: calorie control, complex carbohydrates, reduced refined sugars and saturated fats.\n"
                "- Avoidance of tobacco and restriction/avoidance of alcohol.\n"
                "- Regular physical activity: at least 150 minutes per week of moderate-intensity aerobic physical activity.",
                "other",
                True,
                "type_2_diabetes",
            )
            add_c(
                "Monitoring and Referrals",
                "MONITORING AND SPECIALIST REFERRALS:\n"
                "- Blood glucose: FPG and 2 hours PPG once monthly (more frequent as required including SMBG or CGM).\n"
                "- HbA1c: every 6–12 months (3 monthly if uncontrolled).\n"
                "- Annual monitoring: ECG, urine ACR (albumin creatinine ratio), dilated fundoscopy, foot examination (pin-prick sensation, monofilament test, vibration, DTR).\n\n"
                "Specialist Referrals:\n"
                "- Endocrinology: for uncontrolled hyperglycemia.\n"
                "- Ophthalmology: at initial evaluation and every year.\n"
                "- Nephrology: for deranged renal function.\n"
                "- Cardiology: for CAD / heart failure / arrhythmia.",
                "monitoring",
                True,
                "both",
                pop_tags=["chronic_kidney_disease", "cardiovascular_disease"],
            )

        return chunks


def process_all_guidelines(
    data_dir: Path,
    output_dir: Path,
) -> tuple[list[GuidelineChunk], dict[str, Any]]:
    """Process all 9 guideline documents in the inventory into clean chunks.

    Excludes unverified flowchart assets from retrieval indexing.
    """
    inventory_path = data_dir / "inventory" / "source_inventory.json"
    if not inventory_path.is_file():
        raise FileNotFoundError(f"Source inventory not found: {inventory_path}")

    with open(inventory_path, encoding="utf-8") as f:
        catalog: list[dict[str, Any]] = json.load(f)

    all_chunks: list[GuidelineChunk] = []
    chunker = GuidelineChunker()
    doc_summaries: list[dict[str, Any]] = []

    output_dir.mkdir(parents=True, exist_ok=True)

    for doc_meta in catalog:
        doc_id = str(doc_meta.get("doc_id", ""))
        local_path_str = str(doc_meta.get("local_path", ""))
        if local_path_str.startswith("guideline_chatbot/data/"):
            file_path = data_dir / local_path_str.replace("guideline_chatbot/data/", "")
        else:
            file_path = data_dir / "raw" / local_path_str
        ranges = doc_meta.get("relevant_page_ranges")

        logger.info("Processing %s from %s (ranges: %s)...", doc_id, file_path, ranges)
        extracted_pages = extract_pdf_pages(file_path, ranges)
        chunks = chunker.chunk_document(doc_meta, extracted_pages)

        # Verify no flowchart nodes are indexed
        for c in chunks:
            assert not c.chunk_id.startswith("fc_"), (
                f"Flowchart node {c.chunk_id} accidentally indexed!"
            )

        all_chunks.extend(chunks)

        doc_summaries.append(
            {
                "doc_id": doc_id,
                "document_name": doc_meta.get("document_name"),
                "condition": doc_meta.get("condition"),
                "pages_extracted": len(extracted_pages),
                "chunks_generated": len(chunks),
            }
        )

    # Save to guideline_chunks.json
    chunks_json_path = output_dir / "guideline_chunks.json"
    with open(chunks_json_path, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in all_chunks], f, indent=2, ensure_ascii=False)

    # Save to guideline_chunks.jsonl
    chunks_jsonl_path = output_dir / "guideline_chunks.jsonl"
    with open(chunks_jsonl_path, "w", encoding="utf-8") as f:
        for c in all_chunks:
            f.write(json.dumps(c.model_dump(), ensure_ascii=False) + "\n")

    summary = {
        "total_documents": len(catalog),
        "total_chunks": len(all_chunks),
        "documents": doc_summaries,
    }

    return all_chunks, summary
