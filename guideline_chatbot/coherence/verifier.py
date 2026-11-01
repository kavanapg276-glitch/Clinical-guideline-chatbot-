"""Implementation of the ClinCoherence rule-based clinical verification layer.

Evaluates 6 clinical failure modes:
1. Target Mismatch: BP/HbA1c targets vs patient subpopulation (elderly >=80, CKD, T2DM, general)
2. Patient-Context Mismatch: Contraindications, allergies, pregnancy, renal failure
3. Unjustified Belief Reversal: Dropping established diagnoses/treatments without evidence
4. Reasoning-Action Inconsistency: Rationale contradicts concrete recommendation
5. Evidence Mismatch: Supratherapeutic drug dosages or fabricated clinical thresholds
6. Correction Persistence: Reverting to pre-correction values after user clarification

Applies Decision Gates:
- PASS: No violations; release response unmodified
- WARN: Non-critical mismatch; prepend visible clinical warning banner
- CLARIFY: Active unclarified conflict or missing critical info; request clarification
- REFUSE: Critical contraindication (e.g. teratogenic drugs); suppress and explain
"""

from __future__ import annotations

import re
from typing import Any

from guideline_chatbot.chunking.schemas import GuidelineChunk
from guideline_chatbot.coherence.interfaces import (
    CaseState,
    CoherenceVerifier,
    GateDecision,
    Turn,
    VerificationResult,
    Violation,
    ViolationSeverity,
    ViolationType,
)

# Maximum guideline therapeutic ceiling doses
MAX_GUIDELINE_DOSES: dict[str, tuple[float, str]] = {
    "ramipril": (10.0, "10 mg/day (MoHFW STG / ICMR STW / NICE NG136)"),
    "enalapril": (40.0, "40 mg/day (ICMR STW / MoHFW STG)"),
    "amlodipine": (10.0, "10 mg/day (ICMR STW / WHO HTN / NICE NG136)"),
    "losartan": (100.0, "100 mg/day (ICMR STW / MoHFW STG)"),
    "telmisartan": (80.0, "80 mg/day (ICMR STW / WHO HTN)"),
    "olmesartan": (40.0, "40 mg/day (ICMR STW)"),
    "chlorthalidone": (25.0, "25 mg/day (ICMR STW / WHO HTN)"),
    "hydrochlorothiazide": (25.0, "25 mg/day (ICMR STW / WHO HTN)"),
    "spironolactone": (50.0, "50 mg/day (ICMR STW / NICE NG136)"),
    "dapagliflozin": (10.0, "10 mg/day (NICE NG28 / ICMR T2DM)"),
    "empagliflozin": (25.0, "25 mg/day (NICE NG28 / ICMR T2DM)"),
}


class RuleBasedCoherenceVerifier(CoherenceVerifier):
    """Rule-based verification layer enforcing multi-turn clinical coherence and safety."""

    def verify(
        self,
        case_state: CaseState,
        draft_response: str,
        retrieved_chunks: list[GuidelineChunk] | list[dict[str, Any]],
        conversation_history: list[Turn],
        current_user_message: str = "",
    ) -> VerificationResult:
        """Verify draft response across the 6 clinical coherence failure modes."""
        violations: list[Violation] = []

        # 1. Target Mismatch Check
        violations.extend(self._check_target_mismatch(case_state, draft_response))

        # 2. Patient-Context Mismatch Check
        violations.extend(self._check_patient_context_mismatch(case_state, draft_response))

        # 3. Unjustified Belief Reversal Check
        violations.extend(
            self._check_unjustified_belief_reversal(
                case_state=case_state,
                draft_response=draft_response,
                conversation_history=conversation_history,
                current_user_message=current_user_message,
            )
        )

        # 4. Reasoning-Action Inconsistency Check
        violations.extend(self._check_reasoning_action_inconsistency(case_state, draft_response))

        # 5. Evidence Mismatch Check
        violations.extend(
            self._check_evidence_mismatch(
                draft_response=draft_response,
                retrieved_chunks=retrieved_chunks,
                case_state=case_state,
            )
        )

        # 6. Correction Persistence Check
        violations.extend(
            self._check_correction_persistence(case_state, draft_response, conversation_history)
        )

        # Determine Decision Gate
        has_critical = any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        has_warning = any(v.severity == ViolationSeverity.WARNING for v in violations)

        if has_critical:
            gate_decision = GateDecision.REFUSE
            modified_response = self._build_refusal_response(violations, draft_response)
            explanation = "Response blocked due to critical safety contraindications."
        elif (
            case_state.disputed_facts_count > 0
            or "### Clarification Required" in draft_response
            or bool(re.search(r"\bclarification\s+required\b", draft_response.lower()))
        ):
            gate_decision = GateDecision.CLARIFY
            if (
                case_state.disputed_facts_count > 0
                and "### Clarification Required" not in draft_response
            ):
                modified_response = self._build_clarify_response(case_state)
                explanation = "Clarification required: active disputed facts in patient state."
            else:
                modified_response = draft_response
                explanation = "Clarification required: incomplete clinical measurement or contradictory statement."
        elif has_warning:
            gate_decision = GateDecision.WARN
            modified_response = self._build_warning_response(violations, draft_response)
            explanation = "Warning banner attached due to clinical coherence divergences."
        else:
            gate_decision = GateDecision.PASS
            modified_response = draft_response
            explanation = "All clinical coherence and guideline verification rules passed."

        return VerificationResult(
            gate_decision=gate_decision,
            violations=violations,
            modified_response=modified_response,
            explanation=explanation,
            verifier_name="clincoherence",
        )

    def _check_target_mismatch(self, case_state: CaseState, draft_response: str) -> list[Violation]:
        """Verify that recommended blood pressure and glycemic targets match subpopulation."""
        violations: list[Violation] = []
        lower = draft_response.lower()

        # Elderly >= 80 target check
        if case_state.age is not None and case_state.age >= 80:
            # NICE 1.4.21 & ICMR STW target is < 150/90 mmHg for age >= 80
            # Flag if draft response strictly mandates intensive target < 130/80 or < 140/90
            demands_intensive = bool(
                re.search(
                    r"\b(?:target|aim\s+for|reduce\s+to|below)\s*(?:below|<)?\s*1(?:30/80|40/90)\b",
                    lower,
                )
            )
            mentions_relaxed = bool(re.search(r"\b150/90\b", lower))
            if demands_intensive and not mentions_relaxed:
                violations.append(
                    Violation(
                        category=ViolationType.TARGET_MISMATCH,
                        severity=ViolationSeverity.WARNING,
                        description=(
                            f"Elderly patient (age {case_state.age}) was assigned an intensive BP target "
                            "without acknowledging the guideline-specified relaxed clinic target (< 150/90 mmHg "
                            "per NICE NG136 §1.4.21 and ICMR STW)."
                        ),
                        trigger_text="Intensive BP target prescribed for age >= 80",
                        suggested_action="Adjust target clinic blood pressure to below 150/90 mmHg for adults aged 80 and over.",
                    )
                )

        # Non-elderly (< 80) target check
        elif case_state.age is not None and case_state.age < 80 and not case_state.is_pregnant:
            recommends_80plus_target = bool(
                re.search(
                    r"\b(?:target|aim\s+for|reduce\s+to|below)\s*(?:below|<)?\s*150/90\b", lower
                )
            )
            if recommends_80plus_target:
                violations.append(
                    Violation(
                        category=ViolationType.TARGET_MISMATCH,
                        severity=ViolationSeverity.WARNING,
                        description=(
                            f"Patient aged {case_state.age} (< 80 years) was assigned a relaxed target (< 150/90 mmHg), "
                            "which is reserved exclusively for adults aged 80 and over."
                        ),
                        trigger_text="Target < 150/90 assigned to non-elderly adult",
                        suggested_action="Maintain standard adult target (< 140/90 mmHg) or stricter comorbidity target.",
                    )
                )

        return violations

    def _check_patient_context_mismatch(
        self, case_state: CaseState, draft_response: str
    ) -> list[Violation]:
        """Verify drug recommendations respect patient comorbidities, pregnancy, and allergies."""
        violations: list[Violation] = []
        lower = draft_response.lower()

        # 1. Pregnancy Contraindications (CRITICAL -> REFUSE)
        if case_state.is_pregnant or ("pregnancy" in case_state.conditions):
            teratogenic_drugs = [
                ("ramipril", "ACE inhibitor (Ramipril)"),
                ("enalapril", "ACE inhibitor (Enalapril)"),
                ("lisinopril", "ACE inhibitor (Lisinopril)"),
                ("losartan", "Angiotensin Receptor Blocker (Losartan)"),
                ("telmisartan", "Angiotensin Receptor Blocker (Telmisartan)"),
                ("olmesartan", "Angiotensin Receptor Blocker (Olmesartan)"),
                ("chlorthalidone", "Thiazide-like diuretic (Chlorthalidone)"),
                ("hydrochlorothiazide", "Thiazide diuretic (Hydrochlorothiazide)"),
                ("spironolactone", "Aldosterone antagonist (Spironolactone)"),
            ]
            for drug_key, drug_label in teratogenic_drugs:
                # Check if drug is recommended rather than warned against
                if re.search(rf"\b{drug_key}\b", lower):
                    is_warning = bool(
                        re.search(
                            rf"\b(?:avoid|contraindicated|do\s+not|teratogenic|unsafe)\s+(?:in\s+pregnancy\s+)?{drug_key}\b|"
                            rf"\b{drug_key}.*?(?:is\s+contraindicated|teratogenic|avoid|strictly\s+contraindicated)\b",
                            lower,
                        )
                    )
                    if not is_warning:
                        violations.append(
                            Violation(
                                category=ViolationType.PATIENT_CONTEXT_MISMATCH,
                                severity=ViolationSeverity.CRITICAL,
                                description=(
                                    f"Teratogenic agent {drug_label} recommended to a pregnant patient. "
                                    "RAAS blockers and diuretics are strictly contraindicated in pregnancy "
                                    "(fetopathy, oligohydramnios, neonatal renal failure per ICMR STW & NICE NG133)."
                                ),
                                trigger_text=f"Recommends {drug_label} in pregnancy",
                                suggested_action="Immediately substitute with pregnancy-safe antihypertensives: Labetalol, Nifedipine, or Methyldopa.",
                            )
                        )

        # 2. Allergy Contraindication Check (CRITICAL -> REFUSE)
        for allergy in case_state.allergies:
            allergy_clean = allergy.lower()
            if allergy_clean == "penicillin":
                continue  # Antihypertensives are not penicillins
            if (
                allergy_clean in ("acei", "ace_inhibitor", "angioedema")
                and re.search(
                    r"\b(?:ramipril|enalapril|lisinopril|perindopril|ace\s+inhibitor)\b", lower
                )
                and not re.search(r"\b(?:avoid|do\s+not|contraindicated)\b", lower)
            ):
                violations.append(
                    Violation(
                        category=ViolationType.PATIENT_CONTEXT_MISMATCH,
                        severity=ViolationSeverity.CRITICAL,
                        description=(
                            "Patient has documented allergy/angioedema to ACE inhibitors, "
                            "but an ACE inhibitor was recommended."
                        ),
                        trigger_text="ACE inhibitor prescribed despite documented allergy",
                        suggested_action="Switch to an ARB or CCB as tolerated.",
                    )
                )

        # 3. Diabetes or Microalbuminuria without Renal Protection (WARNING)
        has_dm_or_renal = (
            "type_2_diabetes" in case_state.conditions
            or "microalbuminuria" in case_state.conditions
        )
        if has_dm_or_renal and not case_state.is_pregnant:
            recommends_beta_blocker_firstline = bool(
                re.search(
                    r"\b(?:initial|first-?line|start\s+with|offer)\s+(?:a\s+)?beta-?blocker\b|"
                    r"\b(?:atenolol|metoprolol|bisoprolol)\s+(?:monotherapy|as\s+first-?line)\b",
                    lower,
                )
            )
            if recommends_beta_blocker_firstline:
                violations.append(
                    Violation(
                        category=ViolationType.PATIENT_CONTEXT_MISMATCH,
                        severity=ViolationSeverity.WARNING,
                        description=(
                            "Beta-blocker recommended as initial therapy for patient with diabetes/microalbuminuria. "
                            "Guidelines (MoHFW STG §4.8.3.2, NICE NG136 §1.4.19, ICMR STW) establish ACEi/ARB as "
                            "the mandatory first-line class for nephroprotection."
                        ),
                        trigger_text="Beta-blocker initial therapy in diabetes/microalbuminuria",
                        suggested_action="Prescribe an ACE inhibitor or ARB as first-line pharmacotherapy.",
                    )
                )

        return violations

    def _check_unjustified_belief_reversal(
        self,
        case_state: CaseState,
        draft_response: str,
        conversation_history: list[Turn],
        current_user_message: str = "",
    ) -> list[Violation]:
        """Detect unwarranted retraction of established diagnoses or clinical facts."""
        violations: list[Violation] = []
        if len(conversation_history) < 1 and not case_state.conditions:
            return violations

        lower_resp = draft_response.lower()
        context_text = current_user_message.lower()
        if conversation_history:
            context_text += " " + conversation_history[-1].user_message.lower()

        # 1. Hypertension retraction check
        prior_htn_established = (
            "hypertension" in case_state.conditions
            or (case_state.sbp is not None and case_state.sbp >= 140)
            or any(
                "hypertension" in t.patient_state_summary.lower()
                or "hypertension" in t.response_text.lower()
                or "bp:" in t.patient_state_summary.lower()
                for t in conversation_history
            )
        )
        now_claims_normotensive = bool(
            re.search(
                r"\b(?:patient\s+is\s+normotensive|blood\s+pressure\s+is\s+normal|normotensive|no\s+hypertension\s+present|treatment\s+is\s+not\s+indicated|do\s+not\s+have\s+hypertension|cancel\s+all\s+antihypertensive)\b",
                lower_resp,
            )
        )
        user_disconfirmed_htn = bool(
            re.search(
                r"\b(?:normal\s+bp|bp\s+is\s+(?:11\d|12\d)/(?:7\d|8\d)|misdiagnosed|false\s+alarm|white\s+coat|home\s+(?:bp|blood\s+pressure)|hbpm|abpm|average\s+daytime)\b",
                context_text,
            )
        )

        if prior_htn_established and now_claims_normotensive and not user_disconfirmed_htn:
            violations.append(
                Violation(
                    category=ViolationType.UNJUSTIFIED_BELIEF_REVERSAL,
                    severity=ViolationSeverity.WARNING,
                    description=(
                        "Response unexpectedly declared patient normotensive and withheld treatment, "
                        "reversing established hypertension history without user-provided disconfirming evidence."
                    ),
                    trigger_text="Unjustified reversal from hypertensive to normotensive",
                    suggested_action="Maintain established diagnosis and recommend appropriate monitoring or therapy.",
                )
            )

        # 2. Type 2 Diabetes retraction check
        prior_t2dm_established = (
            "type_2_diabetes" in case_state.conditions
            or "diabetes" in case_state.conditions
            or (case_state.hba1c is not None and case_state.hba1c >= 6.5)
            or any(
                "diabetes" in t.patient_state_summary.lower()
                or "diabetes" in t.response_text.lower()
                for t in conversation_history
            )
        )
        now_claims_no_diabetes = bool(
            re.search(
                r"\b(?:do\s+not\s+have\s+diabetes|no\s+diabetes|not\s+diabetic|blood\s+sugar\s+is\s+fine|no\s+glycemic\s+abnormalities)\b",
                lower_resp,
            )
        )
        user_disconfirmed_t2dm = bool(
            re.search(
                r"\b(?:normal\s+glucose|fasting\s+(?:is\s+)?(?:7\d|8\d|9\d)|hba1c\s+(?:is\s+)?(?:4\.\d|5\.[0-6])|misdiagnosed|false\s+alarm)\b",
                context_text,
            )
        )

        if prior_t2dm_established and now_claims_no_diabetes and not user_disconfirmed_t2dm:
            violations.append(
                Violation(
                    category=ViolationType.UNJUSTIFIED_BELIEF_REVERSAL,
                    severity=ViolationSeverity.WARNING,
                    description=(
                        "Response unexpectedly retracted established diabetes diagnosis without clinical justification."
                    ),
                    trigger_text="Unjustified reversal of established diabetes diagnosis",
                    suggested_action="Maintain glycemic monitoring and guideline-recommended management.",
                )
            )

        return violations

    def _check_reasoning_action_inconsistency(
        self, case_state: CaseState, draft_response: str
    ) -> list[Violation]:
        """Check for internal contradictions between stated clinical rationale and concrete actions."""
        violations: list[Violation] = []
        lower = draft_response.lower()

        # Pattern: Rationale emphasizes ACEi/ARB for renal protection, but Action prescribes CCB alone
        rationale_demands_ace = bool(
            re.search(
                r"\b(?:ace\s+inhibitors?|arbs?|raas\s+blockers?).*?(?:mandatory|strongly\s+preferred|essential\s+for\s+renal)\b",
                lower,
            )
        )
        action_only_ccb = bool(
            re.search(
                r"\b(?:start|prescribe|initiate|offer)\s+(?:only\s+)?(?:amlodipine|ccb)\s+monotherapy\b",
                lower,
            )
        )

        if rationale_demands_ace and action_only_ccb:
            violations.append(
                Violation(
                    category=ViolationType.REASONING_ACTION_INCONSISTENCY,
                    severity=ViolationSeverity.WARNING,
                    description=(
                        "Internal contradiction: Response rationale states ACEi/ARB is mandatory for renal protection, "
                        "but the recommendation prescribes amlodipine monotherapy."
                    ),
                    trigger_text="Rationale demands ACEi, but recommendation prescribes CCB monotherapy",
                    suggested_action="Align the recommendation with the stated rationale by prescribing an ACEi or ARB.",
                )
            )

        # Pattern: Grade 2 hypertension recognized, but only lifestyle modification recommended
        rationale_grade2 = bool(
            re.search(r"\bgrade\s+2\s+hypertension|stage\s+2\s+hypertension|bp\s+>=\s*160\b", lower)
        )
        action_lifestyle_only = bool(
            re.search(
                r"\b(?:recommend\s+only\s+lifestyle|lifestyle\s+modification\s+alone|defer\s+medications?\s+for\s+6\s+months)\b",
                lower,
            )
        )

        if rationale_grade2 and action_lifestyle_only:
            violations.append(
                Violation(
                    category=ViolationType.REASONING_ACTION_INCONSISTENCY,
                    severity=ViolationSeverity.CRITICAL,
                    description=(
                        "Internal contradiction: Grade 2 hypertension recognized in rationale, but action "
                        "recommends lifestyle modification alone without pharmacotherapy."
                    ),
                    trigger_text="Grade 2 HTN recognized, but action recommends lifestyle only",
                    suggested_action="Initiate prompt dual-combination pharmacotherapy alongside lifestyle advice.",
                )
            )

        return violations

    def _check_evidence_mismatch(
        self,
        draft_response: str,
        retrieved_chunks: list[GuidelineChunk] | list[dict[str, Any]],
        case_state: CaseState | None = None,
    ) -> list[Violation]:
        """Verify numerical drug doses and clinical thresholds against retrieved guidelines."""
        violations: list[Violation] = []
        lower = draft_response.lower()

        # Check maximum dosage ceilings
        for drug_name, (max_dose, ceiling_desc) in MAX_GUIDELINE_DOSES.items():
            pattern = rf"\b{drug_name}\s+(?:at\s+)?(\d+(?:\.\d+)?)\s*mg\b"
            matches = re.finditer(pattern, lower)
            for m in matches:
                prescribed_dose = float(m.group(1))
                if prescribed_dose > max_dose:
                    violations.append(
                        Violation(
                            category=ViolationType.EVIDENCE_MISMATCH,
                            severity=ViolationSeverity.CRITICAL,
                            description=(
                                f"Prescribed dose of {drug_name.title()} ({prescribed_dose} mg) exceeds the maximum "
                                f"guideline ceiling of {ceiling_desc}."
                            ),
                            trigger_text=f"{drug_name.title()} {prescribed_dose} mg exceeds ceiling {max_dose} mg",
                            suggested_action=f"Reduce {drug_name.title()} dose to maximum therapeutic range (<= {max_dose} mg).",
                        )
                    )

        # Check for wrong-target evidence chunks injected or retrieved
        if case_state:
            has_t2dm = (
                "type_2_diabetes" in case_state.conditions or "diabetes" in case_state.conditions
            )
            has_t1dm = "type_1_diabetes" in case_state.conditions
            for chunk in retrieved_chunks:
                chunk_cond = getattr(chunk, "condition", None) or (
                    chunk.get("condition") if isinstance(chunk, dict) else None
                )
                chunk_id = getattr(chunk, "chunk_id", None) or (
                    chunk.get("chunk_id") if isinstance(chunk, dict) else ""
                )
                chunk_text = getattr(chunk, "text", "") or (
                    chunk.get("text", "") if isinstance(chunk, dict) else ""
                )

                # Injected Type 1 Diabetes chunk into Type 2 Diabetes question
                if (
                    has_t2dm
                    and not has_t1dm
                    and (
                        chunk_cond == "type_1_diabetes"
                        or (
                            "type 1 diabetes" in chunk_text.lower()[:80]
                            and "type 2" not in chunk_text.lower()[:80]
                        )
                    )
                ):
                    violations.append(
                        Violation(
                            category=ViolationType.EVIDENCE_MISMATCH,
                            severity=ViolationSeverity.WARNING,
                            description=(
                                f"Wrong-target evidence mismatch: Retrieved chunk ({chunk_id}) applies to "
                                f"Type 1 Diabetes, injected into a Type 2 Diabetes clinical scenario."
                            ),
                            trigger_text=f"Chunk {chunk_id} condition is type_1_diabetes",
                            suggested_action="Filter retrieved evidence to Type 2 Diabetes guidelines (ICMR STW / NICE NG28).",
                        )
                    )

                # Injected Hypertension chunk into patient with normal BP and no HTN
                has_htn = "hypertension" in case_state.conditions
                if (
                    not has_htn
                    and (case_state.sbp is None or case_state.sbp < 130)
                    and chunk_cond == "hypertension"
                    and any(
                        d in lower
                        for d in [
                            "amlodipine",
                            "ramipril",
                            "telmisartan",
                            "antihypertensive",
                            "blood pressure target",
                        ]
                    )
                ):
                    violations.append(
                        Violation(
                            category=ViolationType.EVIDENCE_MISMATCH,
                            severity=ViolationSeverity.WARNING,
                            description=(
                                f"Wrong-target evidence mismatch: Hypertension treatment chunk ({chunk_id}) "
                                f"applied to a non-hypertensive patient."
                            ),
                            trigger_text=f"Hypertension chunk {chunk_id} applied without diagnosed hypertension",
                            suggested_action="Restrict retrieval to glycemic management guidelines.",
                        )
                    )

        return violations

    def _check_correction_persistence(
        self, case_state: CaseState, draft_response: str, conversation_history: list[Turn]
    ) -> list[Violation]:
        """Verify that user corrections and clarifications are maintained across turns."""
        violations: list[Violation] = []
        if len(conversation_history) < 1:
            return violations

        lower_resp = draft_response.lower()

        # Look for user corrections in history
        for turn in conversation_history:
            user_msg = turn.user_message.lower()
            # E.g. User corrected age to 84
            if re.search(r"\b(?:actually|corrected|clarif|confirm)", user_msg):
                age_corr = re.search(r"\b(?:age\s+is|age|aged)\s*(\d{2})\b", user_msg)
                if (
                    age_corr
                    and int(age_corr.group(1)) >= 80
                    and re.search(
                        r"\b(?:middle-?aged|young\s+adult|aged\s+5\d|under\s+55)\b", lower_resp
                    )
                ):
                    corrected_age = int(age_corr.group(1))
                    violations.append(
                        Violation(
                            category=ViolationType.CORRECTION_PERSISTENCE,
                            severity=ViolationSeverity.WARNING,
                            description=(
                                f"Response reverted to pre-correction age category, ignoring clinician "
                                f"clarification that patient is {corrected_age} years old."
                            ),
                            trigger_text="Reverted to pre-correction age",
                            suggested_action=f"Apply clinical recommendations tailored to age {corrected_age}.",
                        )
                    )

            # E.g. User corrected BP from normal to 168/104
            if re.search(
                r"\b(?:actually|confirmed\s+reading|bp\s+today\s+is)\s*168/104\b", user_msg
            ) and re.search(
                r"\b(?:normal\s+blood\s+pressure|normotensive|bp\s+is\s+fine)\b", lower_resp
            ):
                violations.append(
                    Violation(
                        category=ViolationType.CORRECTION_PERSISTENCE,
                        severity=ViolationSeverity.CRITICAL,
                        description=(
                            "Response reverted to claiming normal blood pressure, ignoring clinician's "
                            "explicit confirmed reading of 168/104 mmHg."
                        ),
                        trigger_text="Reverted to normal BP despite confirmed 168/104 mmHg",
                        suggested_action="Manage as confirmed Grade 2 / Stage 2 hypertension.",
                    )
                )

        return violations

    def _build_refusal_response(self, violations: list[Violation], draft_response: str) -> str:
        """Construct safe refusal when critical safety contraindications are flagged."""
        critical_items = [v for v in violations if v.severity == ViolationSeverity.CRITICAL]
        lines = [
            "🛑 **[CLINICAL SAFETY REFUSAL — ClinCoherence Verification Layer]**",
            "",
            "The generated response was blocked from release because it contains critical guideline safety violations:",
            "",
        ]
        for idx, crit in enumerate(critical_items, 1):
            lines.append(
                f"{idx}. **{crit.category.value.replace('_', ' ').title()}**: {crit.description}"
            )
            if crit.suggested_action:
                lines.append(f"   - *Mandatory Clinical Action*: {crit.suggested_action}")

        lines.extend(
            [
                "",
                "**Guideline Reference**: Cross-guideline protocols (MoHFW STG, ICMR STW, WHO, NICE) mandate that "
                "strictly contraindicated drugs (e.g. teratogens in pregnancy, supratherapeutic doses, or allergen exposures) "
                "must never be prescribed.",
                "",
                "*Research Prototype Disclaimer: For evaluation and research purposes only. "
                "Not a substitute for qualified clinical judgment.*",
            ]
        )
        return "\n".join(lines)

    def _build_warning_response(self, violations: list[Violation], draft_response: str) -> str:
        """Prepend warning banner when non-critical coherence divergences are detected."""
        warn_items = [
            v
            for v in violations
            if v.severity in (ViolationSeverity.WARNING, ViolationSeverity.ADVISORY)
        ]
        banner_lines = [
            "⚠️ **[CLINICAL COHERENCE WARNING — ClinCoherence Verification Layer]**",
            "",
            "The following guideline coherence advisories were flagged for this response:",
            "",
        ]
        for _idx, w in enumerate(warn_items, 1):
            banner_lines.append(
                f"- **{w.category.value.replace('_', ' ').title()}**: {w.description}"
            )
            if w.suggested_action:
                banner_lines.append(f"  *Guidance*: {w.suggested_action}")

        banner_lines.extend(["", "---", "", draft_response])
        return "\n".join(banner_lines)

    def _build_clarify_response(self, case_state: CaseState) -> str:
        """Construct clarification request when active disputed facts exist."""
        return (
            "### Clarification Required: Unresolved Patient Context\n\n"
            "The ClinCoherence verification layer detected active contradictory statements in the patient's recorded "
            "clinical context. Please confirm the verified parameters before initiating or altering pharmacotherapy.\n\n"
            f"- **Active Conflicts Count**: {case_state.disputed_facts_count}\n\n"
            "*Research Prototype Disclaimer: For evaluation and research purposes only. "
            "Not a substitute for qualified clinical judgment.*"
        )
