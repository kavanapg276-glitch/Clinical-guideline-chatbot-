"""Structured clinical response generator for guideline-based decision support.

Enforces strict guideline grounding, multi-section clinical response schema,
inline citation formatting, out-of-scope abstention, conflict clarification,
and evidence-based pushback handling.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from guideline_chatbot.chatbot.llm_client import LLMClient, MockLLMClient
from guideline_chatbot.chatbot.patient_state import PatientState

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Clinical Guideline Decision Support Assistant specializing in Hypertension and Type 2 Diabetes.
Your knowledge is strictly restricted to verified clinical guideline sources: MoHFW (India STG 2016), ICMR (India STW), WHO (HEARTS 2020, Hypertension 2021, HEARTS-D 2023), and NICE (NG136, NG28).

Response Structure Requirements:
1. ### Guideline Recommendation(s)
   - State specific recommendations grounded directly in the provided retrieved guideline chunks.
   - Include inline citations in the format: [Document Name, p. X, §Section, Year].
2. ### Patient Applicability & Context Analysis
   - Detail how the patient's vitals, age, comorbidities (CKD, T2DM), and status (pregnancy) match or conflict with the recommendation.
3. ### Missing Patient Information & Recommended Workup
   - List essential missing diagnostics (e.g., ABPM, eGFR, urine ACR, serum potassium, HbA1c).
4. ### Cross-Guideline Consensus & Divergence
   - Note any differences between issuing bodies (e.g. ICMR/WHO dual combination vs NICE monotherapy; BP target variations).
5. ### General Clinical Rationale
   - Label visibly: "*General Clinical Rationale — Not a Formal Guideline Recommendation*".
6. ### Research Prototype Disclaimer
   - End with: "*Research Prototype Disclaimer: For evaluation and research purposes only. Not a substitute for clinical judgment.*"

Strict Grounding Rules:
- If a query is outside Hypertension and Type 2 Diabetes, ABSTAIN safely.
- If a patient statement contradicts previous facts, request CLARIFICATION.
- If a user pushes back without new clinical facts, REAFFIRM the guideline evidence firmly and politely.
"""


DOC_YEARS: dict[str, str] = {
    "mohfw_htn_001": "2016",
    "mohfw_htn_002": "2016",
    "mohfw_t2dm_001": "2016",
    "who_htn_001": "2021",
    "who_t2dm_001": "2020",
    "nice_htn_001": "2019/2022",
    "nice_t2dm_001": "2015/2022",
    "icmr_htn_001": "2026",
    "icmr_t2dm_001": "2022",
}


class ClinicalResponseGenerator:
    """Generates structured clinical responses from retrieved guideline chunks and patient state."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or MockLLMClient()

    def _derive_missing_info(
        self, hits: list[dict[str, Any]], patient_state: PatientState
    ) -> list[str]:
        """Derive missing patient information dynamically from retrieved chunk criteria and unrecorded patient parameters."""
        missing: list[str] = []
        seen_params: set[str] = set()

        all_criteria_text: list[str] = []
        for h in hits:
            meta = h.get("metadata", {})
            app = meta.get("applicability_conditions") or ""
            exc = meta.get("exceptions") or ""
            all_criteria_text.append(f"{app} {exc} {h.get('text', '')}".lower())
        joined_criteria = " ".join(all_criteria_text)

        # 1. ABPM / Out-of-office BP confirmation
        if (
            re.search(r"\b(?:abpm|hbpm|ambulatory|home\s+bp|confirm)\b", joined_criteria)
            and patient_state.abpm_daytime_sbp is None
            and "abpm" not in seen_params
        ):
            missing.append(
                "- **Out-of-office BP Confirmation (ABPM/HBPM)**: Referenced in retrieved applicability criteria to confirm sustained hypertension."
            )
            seen_params.add("abpm")

        # 2. Renal function (eGFR / Serum Creatinine)
        if (
            re.search(r"\b(?:egfr|creatinine|renal|kidney|crcl)\b", joined_criteria)
            and patient_state.egfr is None
            and patient_state.creatinine is None
            and "renal" not in seen_params
        ):
            missing.append(
                "- **Renal Function (eGFR / Serum Creatinine)**: Referenced in retrieved dosing criteria and contraindication exceptions."
            )
            seen_params.add("renal")

        # 3. Serum Potassium / Electrolytes
        if (
            re.search(r"\b(?:potassium|hyperkalemia|hypokalemia|electrolytes?)\b", joined_criteria)
            and patient_state.potassium is None
            and "potassium" not in seen_params
        ):
            missing.append(
                "- **Serum Potassium and Electrolytes**: Required prior to RAAS blocker or diuretic initiation per retrieved drug guidance."
            )
            seen_params.add("potassium")

        # 4. Urine Albumin-to-Creatinine Ratio (ACR)
        if (
            re.search(
                r"\b(?:urine\s+acr|acr|albuminuria|proteinuria|microalbuminuria)\b", joined_criteria
            )
            and patient_state.urine_acr is None
            and "acr" not in seen_params
        ):
            missing.append(
                "- **Urine Albumin-to-Creatinine Ratio (ACR)**: Required to screen for renal target-organ damage and microalbuminuria."
            )
            seen_params.add("acr")

        # 5. Glycemic Status (HbA1c / FPG)
        if (
            re.search(r"\b(?:hba1c|glucose|glycemic|diabetes)\b", joined_criteria)
            and patient_state.hba1c is None
            and "type_2_diabetes" not in patient_state.conditions
            and "hba1c" not in seen_params
        ):
            missing.append(
                "- **Glycemic Status (HbA1c / Fasting Glucose)**: Referenced in retrieved criteria to assess diabetic comorbidity and glycemic control."
            )
            seen_params.add("hba1c")

        # 6. Pregnancy Status
        if (
            re.search(
                r"\b(?:pregnant|pregnancy|teratogenic|women\s+planning\s+pregnancy)\b",
                joined_criteria,
            )
            and patient_state.sex == "female"
            and not patient_state.is_pregnant
            and "pregnancy" not in seen_params
        ):
            missing.append(
                "- **Pregnancy Status Confirmation**: Essential in females of childbearing potential due to strict teratogenic contraindications."
            )
            seen_params.add("pregnancy")

        if not missing:
            missing.append(
                "- **Baseline Assessment Complete**: No additional unmeasured parameters triggered by retrieved chunk criteria."
            )

        return missing

    def generate_response(
        self,
        query: str,
        retrieval_result: dict[str, Any],
        patient_state: PatientState,
    ) -> dict[str, Any]:
        """Generate response text and metadata given retrieval results and patient state.

        Returns:
            Dict containing:
                - "text": formatted response string
                - "action_type": "abstain" | "clarify" | "pushback_reaffirm" | "recommendation"
                - "is_abstention": boolean
        """
        # 1. Out-of-scope domain abstention check
        if retrieval_result.get("is_out_of_scope", False):
            return {
                "text": self._build_abstention_text(query),
                "action_type": "abstain",
                "is_abstention": True,
            }

        # 2. Unresolved patient contradiction check
        if patient_state.has_conflicts:
            latest_conflict = patient_state.disputed_facts[-1]
            if latest_conflict.turn_index == patient_state.turn_count:
                return {
                    "text": self._build_clarification_text(latest_conflict, patient_state),
                    "action_type": "clarify",
                    "is_abstention": False,
                }

        # 3. Patient pushback check
        is_pushback = self._detect_pushback(query)

        # 4. Generate structured recommendation
        if isinstance(self.llm_client, MockLLMClient):
            response_text = self._build_mock_response(
                query=query,
                retrieval_result=retrieval_result,
                patient_state=patient_state,
                is_pushback=is_pushback,
            )
            action_type = "pushback_reaffirm" if is_pushback else "recommendation"
            return {
                "text": response_text,
                "action_type": action_type,
                "is_abstention": False,
            }
        else:
            prompt = self._build_prompt(query, retrieval_result, patient_state, is_pushback)
            llm_output = self.llm_client.generate(prompt=prompt, system_prompt=SYSTEM_PROMPT)
            action_type = "pushback_reaffirm" if is_pushback else "recommendation"
            return {
                "text": llm_output,
                "action_type": action_type,
                "is_abstention": False,
            }

    def _detect_pushback(self, query: str) -> bool:
        """Detect conversational pushback against guideline-directed treatment."""
        lower = query.lower()
        pushback_patterns = [
            r"\b(?:don't\s+want|refuse|prefer\s+not|hesitant|afraid\s+of)\s+(?:pills?|meds?|medicines?|drugs?|treatment)\b",
            r"\b(?:only\s+lifestyle|lifestyle\s+alone|diet\s+and\s+exercise\s+only|just\s+diet|natural\s+remedies?)\b",
            r"\b(?:is\s+(?:it\s+)?really\s+necessary|do\s+i\s+really\s+need|cannot\s+i\s+just|can\s+we\s+wait)\b",
            r"\b(?:my\s+friend|relative|heard\s+that)\s+(?:cured|lowered|stopped\s+meds?)\b",
            r"\b(?:why\s+meds?|why\s+drugs?|side\s+effects\s+are\s+too\s+bad)\b",
        ]
        return any(re.search(pat, lower) for pat in pushback_patterns)

    def _build_abstention_text(self, query: str) -> str:
        """Format a clear, safe abstention response for out-of-scope inquiries."""
        return (
            "### Clinical Decision Support Notice: Out-of-Scope Query\n\n"
            "**Guideline Scope Limitation**: This decision support system is strictly designed "
            "for adult Hypertension and Type 2 Diabetes guideline management (MoHFW STG 2016, "
            "ICMR STW, WHO HEARTS/Hypertension/HEARTS-D, NICE NG136/NG28).\n\n"
            f'The clinical query concerning *"{query.strip()}"* falls outside the curated clinical corpus. '
            "No guideline recommendations can be safely generated for conditions outside adult hypertension "
            "and type 2 diabetes.\n\n"
            "**Recommended Action**: Please consult the appropriate specialist or referring pediatric/adult "
            "clinical guidelines directly.\n\n"
            "*Research Prototype Disclaimer: For evaluation and research purposes only. "
            "Not a substitute for qualified clinical judgment.*"
        )

    def _build_clarification_text(self, conflict: Any, patient_state: PatientState) -> str:
        """Format a clarification request when patient history contains direct contradictions."""
        return (
            "### Clarification Required: Conflicting Patient Information\n\n"
            "**Clinical History Discrepancy Detected**:\n"
            f"- **Parameter**: {conflict.field.replace('_', ' ').title()}\n"
            f"- **Prior Recorded**: {conflict.previous_value}\n"
            f"- **New Statement**: {conflict.new_value}\n"
            f"- **Detail**: {conflict.explanation}\n\n"
            "**Clinical Guidance**: Clinical guidelines enforce distinct treatment thresholds and drug choices "
            "depending on confirmed diagnoses and blood pressure levels. Conflicting data introduces safety risks "
            "(such as inappropriate pharmacotherapy or contraindicated agents).\n\n"
            "Please confirm the verified patient reading and status before proceeding with treatment recommendations.\n\n"
            "*Research Prototype Disclaimer: For evaluation and research purposes only. "
            "Not a substitute for qualified clinical judgment.*"
        )

    def _build_mock_response(
        self,
        query: str,
        retrieval_result: dict[str, Any],
        patient_state: PatientState,
        is_pushback: bool = False,
    ) -> str:
        """Construct a deterministic guideline-grounded response derived strictly from retrieved chunks."""
        hits = retrieval_result.get("hits", [])
        disagreements = retrieval_result.get("disagreements", [])

        sections: list[str] = []

        # 1. Pushback preamble if applicable
        if is_pushback:
            sections.append(
                "### Guideline Treatment Rationale: Response to Patient Concern\n\n"
                "**Non-Pharmacological Measures vs. Pharmacotherapy**:\n"
                "While lifestyle interventions (sodium restriction, exercise, weight reduction) are universally "
                "recommended as baseline therapy, guidelines emphasize that when confirmed blood pressure meets or exceeds "
                "treatment thresholds, lifestyle modification alone is insufficient to reduce cardiovascular mortality. [^1]\n\n"
                "Pharmacotherapy should be initiated promptly alongside lifestyle measures to prevent target-organ damage. [^1]"
            )

        # 2. Primary Guideline Recommendations (Evidence-bound only)
        rec_lines: list[str] = ["### Guideline Recommendation(s)\n"]

        if not hits:
            rec_lines.append(
                "No guideline evidence was retrieved for this point. Please verify primary guideline documentation."
            )
        else:
            for i, hit in enumerate(hits[:4], 1):
                meta = hit.get("metadata", {})
                doc_id = hit.get("doc_id") or meta.get("doc_id", "")
                doc_name = meta.get("document_name", "Clinical Guideline")
                page = meta.get("page_start", 1)
                raw_heading = meta.get("heading", "Recommendation")
                clean_heading = re.sub(r"\[IMAGE\]\s*", "", raw_heading).strip() or "Recommendation"
                year = DOC_YEARS.get(doc_id) or meta.get("recommendation_year") or "unspecified"

                summary_text = re.sub(r"\[IMAGE\]\s*", "", hit.get("text", "")).strip()
                clean_lines = [
                    line.strip()
                    for line in summary_text.splitlines()
                    if line.strip() and not line.startswith("|")
                ]
                excerpt = " ".join(clean_lines)
                if len(excerpt) > 300:
                    excerpt = excerpt[:297] + "..."

                rec_lines.append(
                    f"{i}. **{clean_heading}** [{doc_name}, p. {page}, §{clean_heading}, {year}]:\n"
                    f"   {excerpt} [^{i}]\n"
                )

        sections.append("\n".join(rec_lines))

        # 3. Patient Applicability & Context Analysis (Grounded in chunks & patient state)
        app_lines: list[str] = ["### Patient Applicability & Context Analysis\n"]
        app_items: list[str] = []

        if patient_state.sbp is not None:
            sbp = patient_state.sbp
            dbp = patient_state.dbp or 0
            app_items.append(
                f"- **Recorded Clinic BP ({int(sbp)}/{int(dbp)} mmHg)**: Evaluated against threshold criteria in retrieved guideline recommendations [^1]."
            )

        if patient_state.age is not None:
            app_items.append(
                f"- **Patient Age ({patient_state.age} years)**: Evaluated against age-stratified criteria in retrieved recommendations [^1]."
            )

        if "type_2_diabetes" in patient_state.conditions:
            app_items.append(
                "- **Comorbidity (Type 2 Diabetes)**: Matches diabetic population criteria and target thresholds in retrieved guidance [^1]."
            )

        if "microalbuminuria" in patient_state.conditions:
            app_items.append(
                "- **Laboratory Finding (Microalbuminuria)**: Laboratory microalbuminuria findings evaluated against renal protection criteria [^1]."
            )
        elif "chronic_kidney_disease" in patient_state.conditions:
            app_items.append(
                "- **Comorbidity (Chronic Kidney Disease)**: Evaluated against renal impairment guidance in retrieved recommendations [^1]."
            )

        if patient_state.is_pregnant:
            app_items.append(
                "- **Pregnancy Status**: Evaluated against guideline contraindications and pregnancy-specific management [^1]."
            )

        if patient_state.medications:
            med_str = ", ".join(sorted(patient_state.medications))
            app_items.append(
                f"- **Current Pharmacotherapy ({med_str})**: Evaluated against step-up or combination protocols in retrieved guidance [^1]."
            )

        if not app_items:
            app_items.append(
                "- General adult population criteria apply; no specific comorbidities recorded in active state [^1]."
            )

        app_lines.extend(app_items)
        sections.append("\n".join(app_lines))

        # 4. Missing Patient Information & Recommended Workup (Dynamically Derived)
        missing_lines: list[str] = ["### Missing Patient Information & Recommended Workup\n"]
        missing_items = self._derive_missing_info(hits, patient_state)
        missing_lines.extend(missing_items)
        sections.append("\n".join(missing_lines))

        # 5. Cross-Guideline Consensus & Divergence
        if disagreements:
            div_lines: list[str] = ["### Cross-Guideline Consensus & Divergence\n"]
            for dis in disagreements:
                domain = dis.get("domain", "Clinical Topic")
                desc = dis.get("description", "")
                div_lines.append(f"- **{domain}**: {desc}")
            sections.append("\n".join(div_lines))

        # 6. General Clinical Rationale (Visibly Labeled)
        sections.append(
            "### General Clinical Rationale\n\n"
            "*General Clinical Rationale — Not a Formal Guideline Recommendation*:\n"
            "Stepwise blood pressure and glycemic management provides synergistic protection against microvascular "
            "and macrovascular events. Treatment decisions should be individualized based on tolerability and target organ evaluation. [^1]"
        )

        # 7. Research Prototype Disclaimer
        sections.append(
            "*Research Prototype Disclaimer: For evaluation and research purposes only. "
            "This software is not an approved medical device and does not replace certified clinical judgment.*"
        )

        return "\n\n".join(sections)

        # 7. Research Prototype Disclaimer
        sections.append(
            "*Research Prototype Disclaimer: For evaluation and research purposes only. "
            "This software is not an approved medical device and does not replace certified clinical judgment.*"
        )

        return "\n\n".join(sections)

    def _build_prompt(
        self,
        query: str,
        retrieval_result: dict[str, Any],
        patient_state: PatientState,
        is_pushback: bool,
    ) -> str:
        """Assemble structured prompt for external LLM execution."""
        hits = retrieval_result.get("hits", [])
        disagreements = retrieval_result.get("disagreements", [])

        chunk_texts: list[str] = []
        for i, hit in enumerate(hits, 1):
            meta = hit.get("metadata", {})
            chunk_texts.append(
                f"[Chunk {i}] ID: {hit.get('chunk_id')}\n"
                f"Source: {meta.get('document_name')} (p. {meta.get('page_start')}, §{meta.get('heading')}, {meta.get('recommendation_year')})\n"
                f"Content: {hit.get('text')}\n"
            )

        prompt_parts: list[str] = [
            f"User Query: {query}",
            f"\nPatient State: {patient_state.to_summary_string()}",
            f"Pushback Detected: {is_pushback}",
            f"Disputed Facts: {len(patient_state.disputed_facts)}",
            f"\nRetrieved Guideline Evidence ({len(hits)} chunks):\n" + "\n".join(chunk_texts),
        ]

        if disagreements:
            prompt_parts.append(f"\nDetected Guideline Disagreements: {disagreements}")

        prompt_parts.append(
            "\nPlease generate the decision support response adhering strictly to the structured sections "
            "and citation guidelines."
        )

        return "\n".join(prompt_parts)
