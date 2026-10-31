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


class ClinicalResponseGenerator:
    """Generates structured clinical responses from retrieved guideline chunks and patient state."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm_client = llm_client or MockLLMClient()

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
        """Construct a deterministic guideline-grounded response from retrieved chunks."""
        hits = retrieval_result.get("hits", [])
        disagreements = retrieval_result.get("disagreements", [])

        sections: list[str] = []

        # 1. Pushback preamble if applicable
        if is_pushback:
            sections.append(
                "### Guideline Treatment Rationale: Response to Patient Concern\n\n"
                "**Non-Pharmacological Measures vs. Pharmacotherapy**:\n"
                "While lifestyle interventions (sodium reduction < 2 g/day, physical exercise ≥ 150 min/week, "
                "weight loss, and alcohol moderation) are universally recommended as foundational therapy, "
                "established guidelines emphasize that when confirmed blood pressure meets or exceeds Stage 1/Grade 1 "
                "thresholds (SBP ≥ 140 or DBP ≥ 90 mmHg) — particularly with additional cardiovascular risk, diabetes, "
                "or microalbuminuria — lifestyle modification alone is insufficient to prevent cardiovascular morbidity.\n\n"
                "Pharmacotherapy should be initiated promptly alongside continued lifestyle adjustments to reduce the risk "
                "of stroke, myocardial infarction, and progressive renal impairment."
            )

        # 2. Primary Guideline Recommendations
        rec_lines: list[str] = ["### Guideline Recommendation(s)\n"]

        if not hits:
            rec_lines.append(
                "No direct guideline recommendations met the retrieval threshold for this query. "
                "Please refine the query or review primary guideline documentation."
            )
        else:
            for i, hit in enumerate(hits[:3], 1):
                meta = hit.get("metadata", {})
                doc_name = meta.get("document_name", "Clinical Guideline")
                page = meta.get("page_start", 1)
                raw_heading = meta.get("heading", "Recommendation")
                clean_heading = re.sub(r"\[IMAGE\]\s*", "", raw_heading).strip() or "Recommendation"
                year = meta.get("recommendation_year") or "current"
                summary_text = re.sub(r"\[IMAGE\]\s*", "", hit.get("text", "")).strip()

                # Clean text excerpt
                first_lines = " ".join(
                    [line.strip() for line in summary_text.splitlines() if line.strip()]
                )
                if len(first_lines) > 280:
                    first_lines = first_lines[:277] + "..."

                rec_lines.append(
                    f"{i}. **{clean_heading}** [{doc_name}, p. {page}, §{clean_heading}, {year}]:\n"
                    f"   {first_lines}\n"
                )

        sections.append("\n".join(rec_lines))

        # 3. Patient Applicability & Context Analysis
        app_lines: list[str] = ["### Patient Applicability & Context Analysis\n"]
        app_items: list[str] = []

        if patient_state.sbp is not None:
            sbp = patient_state.sbp
            dbp = patient_state.dbp or 0
            if sbp >= 160 or dbp >= 100:
                app_items.append(
                    f"- **Blood Pressure ({int(sbp)}/{int(dbp)} mmHg)**: Grade 2 / Stage 2 hypertension. "
                    "Prompt pharmacotherapy with dual combination (e.g. A+C or A+D) is indicated."
                )
            elif sbp >= 140 or dbp >= 90:
                app_items.append(
                    f"- **Blood Pressure ({int(sbp)}/{int(dbp)} mmHg)**: Grade 1 / Stage 1 hypertension. "
                    "Pharmacotherapy indicated if sustained on ABPM/HBPM or if target organ damage/diabetes is present."
                )
            else:
                app_items.append(
                    f"- **Blood Pressure ({int(sbp)}/{int(dbp)} mmHg)**: Normotensive range."
                )

        if "type_2_diabetes" in patient_state.conditions:
            app_items.append(
                "- **Comorbidity (Type 2 Diabetes)**: Presence of diabetes modifies first-line drug selection "
                "(ACE inhibitors or ARBs strongly preferred for renal protection) and establishes stricter BP targets."
            )

        if (
            "chronic_kidney_disease" in patient_state.conditions
            or "microalbuminuria" in patient_state.conditions
        ):
            app_items.append(
                "- **Renal Status (Microalbuminuria/CKD)**: Renin-angiotensin system blockers (ACEi/ARB) "
                "are the mandatory initial class to slow progression of nephropathy."
            )

        if patient_state.is_pregnant:
            app_items.append(
                "- **Pregnancy Status**: ACE inhibitors, ARBs, and thiazide diuretics are strictly contraindicated. "
                "Labetalol, methyldopa, or nifedipine are the recommended safe alternatives."
            )

        if patient_state.age is not None:
            if patient_state.age >= 80:
                app_items.append(
                    f"- **Age ({patient_state.age} years)**: Relaxed blood pressure targets apply "
                    "(e.g., NICE clinic target < 150/90 mmHg; WHO < 140/90 mmHg with clinical judgment)."
                )
            elif patient_state.age >= 55:
                app_items.append(
                    f"- **Age ({patient_state.age} years)**: NICE recommends Calcium Channel Blocker (CCB) "
                    "as initial monotherapy for uncomplicated hypertension in patients aged ≥ 55."
                )

        if not app_items:
            app_items.append(
                "- Patient clinical parameters not yet specified. Recommendations reflect general adult population."
            )

        app_lines.extend(app_items)
        sections.append("\n".join(app_lines))

        # 4. Missing Patient Information & Recommended Workup
        missing_lines: list[str] = ["### Missing Patient Information & Recommended Workup\n"]
        missing_items: list[str] = []

        if patient_state.sbp is not None and patient_state.abpm_daytime_sbp is None:
            missing_items.append(
                "- **Out-of-office BP Confirmation**: Ambulatory Blood Pressure Monitoring (ABPM) "
                "or Home Blood Pressure Monitoring (HBPM) to confirm sustained hypertension and rule out white-coat effect."
            )
        if patient_state.hba1c is None and "type_2_diabetes" not in patient_state.conditions:
            missing_items.append(
                "- **Glycemic Evaluation**: Fasting plasma glucose and HbA1c to screen for occult diabetes."
            )
        if patient_state.egfr is None:
            missing_items.append(
                "- **Renal Function**: Serum creatinine, estimated GFR (eGFR), and serum electrolytes (potassium/sodium)."
            )
        if patient_state.urine_acr is None:
            missing_items.append(
                "- **Urinary Albumin**: Urine Albumin-to-Creatinine Ratio (ACR) to detect early diabetic nephropathy."
            )

        if not missing_items:
            missing_items.append("- Essential laboratory baseline workup completed.")

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
            "Hypertension and type 2 diabetes represent synergistic cardiovascular risk factors. "
            "Antihypertensive pharmacotherapy provides dual protection by reducing vascular sheer stress "
            "and preserving glomerular capillary integrity. Stepwise or initial combination therapy should "
            "be titrated at 4–6 week intervals until therapeutic target is reached."
        )

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
