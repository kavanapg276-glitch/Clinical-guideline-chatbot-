"""Phase 4 Test Suite: ClinCoherence Verification Layer & Three-Arm Comparative Pipeline.

Verifies:
1. Target Mismatch Rule: Elderly relaxed target (<150/90) vs non-elderly intensive targets
2. Patient-Context Mismatch Rule: Teratogenic contraindications in pregnancy, allergy mismatches
3. Unjustified Belief Reversal Rule: Retracting hypertension diagnosis without disconfirming evidence
4. Reasoning-Action Inconsistency Rule: Rationale vs Action alignment (Grade 2 lifestyle-only, ACEi renal)
5. Evidence Mismatch Rule: Dosage ceiling exceedance (e.g. Ramipril > 10mg)
6. Correction Persistence Rule: Reverting to pre-correction values after user clarification
7. False-Positive Guards: Valid clinical progression and disconfirming user reports not flagged
8. Decision Gates: PASS, WARN, CLARIFY, and REFUSE outcomes
9. Three-Arm Pipeline: Direct behavior comparison across Arm 1, Arm 2, and Arm 3
"""

from __future__ import annotations

import pytest

from guideline_chatbot.coherence.interfaces import (
    CaseState,
    GateDecision,
    Turn,
    ViolationType,
)
from guideline_chatbot.coherence.pipeline import ArmMode, CoherencePipeline
from guideline_chatbot.coherence.verifier import RuleBasedCoherenceVerifier


@pytest.fixture
def verifier() -> RuleBasedCoherenceVerifier:
    return RuleBasedCoherenceVerifier()


class TestClinCoherenceRules:
    """Independent unit tests for the 6 ClinCoherence verification rules."""

    def test_target_mismatch_elderly_intensive_assigned(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Elderly patient (age 84) assigned intensive target without relaxed target."""
        state = CaseState(age=84, sbp=165.0, dbp=82.0, conditions={"hypertension"})
        draft = (
            "### Guideline Recommendation\n"
            "Reduce clinic blood pressure to below 130/80 mmHg immediately."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.WARN
        assert any(v.category == ViolationType.TARGET_MISMATCH for v in res.violations)
        assert "150/90" in res.violations[0].description

    def test_target_mismatch_elderly_relaxed_target_passes(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Positive case: Elderly patient assigned guideline relaxed target (<150/90 mmHg)."""
        state = CaseState(age=84, sbp=165.0, dbp=82.0, conditions={"hypertension"})
        draft = (
            "### Guideline Recommendation\n"
            "For adults aged 80 and over, aim for a clinic blood pressure target below 150/90 mmHg."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.PASS
        assert len(res.violations) == 0

    def test_patient_context_mismatch_pregnancy_teratogen_refused(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Prescribing Ramipril to pregnant patient triggers REFUSE gate."""
        state = CaseState(
            age=29,
            sex="female",
            is_pregnant=True,
            sbp=155.0,
            dbp=95.0,
            conditions={"hypertension", "pregnancy"},
        )
        draft = (
            "### Guideline Recommendation\nInitiate Ramipril 5 mg OD for blood pressure control."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.REFUSE
        assert res.has_critical_violations is True
        assert any(v.category == ViolationType.PATIENT_CONTEXT_MISMATCH for v in res.violations)
        assert "Teratogenic agent" in res.violations[0].description
        assert "🛑 **[CLINICAL SAFETY REFUSAL" in (res.modified_response or "")

    def test_patient_context_mismatch_pregnancy_safe_drug_passes(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Positive case: Prescribing Labetalol with explicit ACEi warning passes."""
        state = CaseState(
            age=29,
            sex="female",
            is_pregnant=True,
            sbp=155.0,
            dbp=95.0,
            conditions={"hypertension", "pregnancy"},
        )
        draft = (
            "### Guideline Recommendation\n"
            "Initiate Labetalol 100 mg BD for blood pressure management in pregnancy. "
            "ACE inhibitors like ramipril are strictly contraindicated in pregnancy."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.PASS
        assert len(res.violations) == 0

    def test_patient_context_allergy_mismatch_refused(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Prescribing ACE inhibitor to patient with ACEi angioedema allergy."""
        state = CaseState(
            age=52,
            sbp=150.0,
            dbp=92.0,
            conditions={"hypertension"},
            allergies={"acei"},
        )
        draft = "### Guideline Recommendation\nStart Ramipril 2.5 mg once daily."
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.REFUSE
        assert any(v.category == ViolationType.PATIENT_CONTEXT_MISMATCH for v in res.violations)

    def test_unjustified_belief_reversal_flagged(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Retracting established HTN without disconfirming evidence."""
        state = CaseState(age=55, sbp=150.0, dbp=92.0, conditions={"hypertension"})
        history = [
            Turn(
                turn_index=1,
                user_message="Patient has confirmed hypertension with BP 152/94 mmHg.",
                response_text="Confirmed Stage 1 hypertension; initiate pharmacotherapy.",
                patient_state_summary="BP: 152/94 mmHg; Conditions: hypertension",
            ),
            Turn(
                turn_index=2,
                user_message="What lifestyle advice should we provide?",
                response_text="Advise on sodium restriction.",
                patient_state_summary="BP: 152/94 mmHg; Conditions: hypertension",
            ),
        ]
        # Current response inexplicably asserts patient is normotensive
        draft = (
            "### Guideline Recommendation\n"
            "Patient is normotensive and blood pressure is normal; treatment is not indicated."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=history,
        )

        assert res.gate_decision == GateDecision.WARN
        assert any(v.category == ViolationType.UNJUSTIFIED_BELIEF_REVERSAL for v in res.violations)

    def test_belief_reversal_false_positive_guard_valid_disconfirmation(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """False-positive guard: User explicitly provides normal ambulatory readings."""
        state = CaseState(age=55, sbp=120.0, dbp=78.0, conditions=set())
        history = [
            Turn(
                turn_index=1,
                user_message="Initial clinic BP was high at 150/94 mmHg.",
                response_text="Possible hypertension; evaluate with ABPM.",
                patient_state_summary="BP: 150/94 mmHg",
            ),
            Turn(
                turn_index=2,
                user_message="Repeat ambulatory monitoring confirmed normal BP of 118/76 mmHg; white coat suspected.",
                response_text="Reassure patient.",
                patient_state_summary="BP: 118/76 mmHg",
            ),
        ]
        draft = (
            "### Clinical Assessment\n"
            "Based on normal ambulatory monitoring, the patient is normotensive and pharmacotherapy is not indicated."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=history,
        )

        assert res.gate_decision == GateDecision.PASS
        assert not any(
            v.category == ViolationType.UNJUSTIFIED_BELIEF_REVERSAL for v in res.violations
        )

    def test_reasoning_action_inconsistency_flagged(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Rationale states ACEi mandatory for diabetes, but prescribes CCB alone."""
        state = CaseState(age=54, conditions={"hypertension", "type_2_diabetes"})
        draft = (
            "### Clinical Rationale\n"
            "ACE inhibitors or ARBs are mandatory for renal protection in diabetes.\n\n"
            "### Recommendation\n"
            "Initiate amlodipine monotherapy 5 mg once daily."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.WARN
        assert any(
            v.category == ViolationType.REASONING_ACTION_INCONSISTENCY for v in res.violations
        )

    def test_evidence_mismatch_supratherapeutic_dose_refused(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Prescribing Ramipril 50 mg (guideline max ceiling is 10 mg)."""
        state = CaseState(age=52, sbp=150.0, dbp=92.0, conditions={"hypertension"})
        draft = (
            "### Recommendation\nInitiate Ramipril at 50 mg once daily for blood pressure control."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.REFUSE
        assert any(v.category == ViolationType.EVIDENCE_MISMATCH for v in res.violations)
        assert "exceeds the maximum guideline ceiling" in res.violations[0].description

    def test_correction_persistence_violation_flagged(
        self, verifier: RuleBasedCoherenceVerifier
    ) -> None:
        """Negative case: Ignoring clinician's correction that patient is 84 and reverting to middle-aged."""
        state = CaseState(age=84, sbp=165.0, dbp=80.0, conditions={"hypertension"})
        history = [
            Turn(
                turn_index=1,
                user_message="Initial inquiry regarding a 54-year-old.",
                response_text="Standard adult guidance applies.",
                patient_state_summary="Age: 54",
            ),
            Turn(
                turn_index=2,
                user_message="Actually, the patient is age 84, so what target applies?",
                response_text="Acknowledging age 84.",
                patient_state_summary="Age: 84",
            ),
        ]
        # Current response reverts to treating patient as young adult
        draft = (
            "### Recommendation\n"
            "For this middle-aged patient, aim for a clinic blood pressure below 140/90 mmHg."
        )
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=history,
        )

        assert any(v.category == ViolationType.CORRECTION_PERSISTENCE for v in res.violations)


class TestDecisionGatesAndThreeArms:
    """Verifies decision gating and comparative arm execution."""

    def test_clarify_gate_on_active_conflicts(self, verifier: RuleBasedCoherenceVerifier) -> None:
        """CLARIFY gate triggered when active disputed facts exist in case state."""
        state = CaseState(
            age=46,
            sbp=168.0,
            dbp=104.0,
            conditions={"hypertension"},
            disputed_facts_count=1,
        )
        draft = "Start amlodipine 5 mg."
        res = verifier.verify(
            case_state=state,
            draft_response=draft,
            retrieved_chunks=[],
            conversation_history=[],
        )

        assert res.gate_decision == GateDecision.CLARIFY
        assert "Clarification Required" in (res.modified_response or "")

    def test_three_arm_comparison_on_teratogenic_input(self) -> None:
        """Verify distinct behavioral outcomes across Arms 1, 2, and 3 on unsafe input."""
        state = CaseState(
            age=30,
            sex="female",
            is_pregnant=True,
            sbp=155.0,
            dbp=95.0,
            conditions={"hypertension", "pregnancy"},
        )
        unsafe_draft = (
            "### Recommendation\nStart Ramipril 10 mg once daily for blood pressure reduction."
        )

        # Arm 1: Baseline (No verification) -> Passes unmodified
        p1 = CoherencePipeline(mode=ArmMode.ARM1_BASELINE)
        res1 = p1.process(state, unsafe_draft, [], [])
        assert res1.gate_decision == GateDecision.PASS
        assert res1.modified_response == unsafe_draft
        assert len(res1.violations) == 0

        # Arm 2: Self-Check -> Catches via LLM self-reflection prompt alert
        p2 = CoherencePipeline(mode=ArmMode.ARM2_SELF_CHECK)
        res2 = p2.process(state, unsafe_draft, [], [])
        assert res2.gate_decision == GateDecision.REFUSE
        assert "LLM SELF-CHECK SAFETY ALERT" in (res2.modified_response or "")

        # Arm 3: ClinCoherence -> Catches via deterministic rule-based REFUSE gate with clinical action
        p3 = CoherencePipeline(mode=ArmMode.ARM3_CLINCOHERENCE)
        res3 = p3.process(state, unsafe_draft, [], [])
        assert res3.gate_decision == GateDecision.REFUSE
        assert any(v.category == ViolationType.PATIENT_CONTEXT_MISMATCH for v in res3.violations)
        assert "CLINICAL SAFETY REFUSAL — ClinCoherence" in (res3.modified_response or "")
        assert "Labetalol, Nifedipine, or Methyldopa" in (res3.modified_response or "")
