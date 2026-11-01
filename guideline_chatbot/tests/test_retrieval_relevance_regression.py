"""Regression test suite for retrieval relevance, intent boosting, and gate consistency.

Verifies:
1. Target query retrieval for adult hypertension (NICE 1.4.20 <140/90, MoHFW targets) without screening/AGREE II noise.
2. First-line drug query retrieval for diabetes + hypertension (NICE 1.4.32 Step 1 ACEi/ARB).
3. Age 80+ target query retrieval (NICE 1.4.21 <150/90) over <80 targets.
4. Pregnancy contraindication query retrieval (ACEi/ARB safety warnings, MHRA advice, WHO pregnancy).
5. "BP 108" normal reading in-scope domain handling.
6. Gate consistency (CLARIFY response yields CLARIFY gate).
"""

from __future__ import annotations

import pytest

from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator
from guideline_chatbot.chatbot.patient_state import PatientStateManager
from guideline_chatbot.coherence.interfaces import GateDecision
from guideline_chatbot.coherence.pipeline import ArmMode
from guideline_chatbot.retrieval.hybrid import (
    ClinicalIntent,
    HybridRetriever,
    detect_clinical_intent,
)


@pytest.fixture(scope="module")
def retriever() -> HybridRetriever:
    """Load default hybrid retrieval pipeline."""
    return HybridRetriever.load_default()


@pytest.fixture(scope="module")
def orchestrator() -> ChatbotOrchestrator:
    """Initialize default orchestrator under Arm 3 ClinCoherence."""
    return ChatbotOrchestrator.create_default(arm_mode=ArmMode.ARM3_CLINCOHERENCE)


class TestIntentDetection:
    """Verify general clinical intent classification."""

    def test_target_intent_classification(self) -> None:
        q = "58-year-old woman, BP 152/96 on two clinic readings, what is the target?"
        intent = detect_clinical_intent(q)
        assert intent == ClinicalIntent.TARGET

    def test_first_line_drug_intent_classification(self) -> None:
        q = "Patient with type 2 diabetes and hypertension, which drug class first?"
        intent = detect_clinical_intent(q)
        assert intent == ClinicalIntent.FIRST_LINE_DRUG

    def test_contraindication_intent_classification(self) -> None:
        q = "26 weeks pregnant, can I take enalapril?"
        intent = detect_clinical_intent(q)
        assert intent == ClinicalIntent.CONTRAINDICATION_SAFETY

    def test_target_intent_age_84(self) -> None:
        q = "Age 84, what is the BP target?"
        intent = detect_clinical_intent(q)
        assert intent == ClinicalIntent.TARGET


class TestRetrievalRelevanceRegression:
    """Verify top-5 chunk relevance across the benchmark clinical queries."""

    def test_query_a_target_under_80(self, retriever: HybridRetriever) -> None:
        """Query a: '58-year-old woman, BP 152/96 on two clinic readings, what is the target?'"""
        q = "58-year-old woman, BP 152/96 on two clinic readings, what is the target?"
        p = {"age": 58, "sex": "female", "sbp": 152, "dbp": 96}
        res = retriever.retrieve(q, top_k=5, patient_state=p)

        assert not res["is_out_of_scope"]
        hits = res["hits"]
        assert len(hits) == 5
        hit_ids = [h["chunk_id"] for h in hits]

        # Must include blood pressure target chunks (NICE 1.4.20 or MoHFW target)
        target_candidates = {
            "nice_htn_001_c0046",  # NICE 1.4.20
            "nice_htn_001_c0099",  # NICE target rationale
            "mohfw_htn_001_c0038",  # MoHFW 4.4.1 target <140/90
            "mohfw_htn_001_c0175",  # MoHFW 4.4.1 target <140/90
            "mohfw_htn_002_c0085",  # MoHFW target in <80
        }
        assert any(cid in target_candidates for cid in hit_ids)

        # Must NOT include irrelevant measurement/screening noise chunks in top 5
        noise_ids = {
            "mohfw_htn_001_c0133",  # 1.5 Interval between measurements
            "mohfw_htn_001_c0262",  # Screening pathway
            "mohfw_htn_001_c0136",  # Rescreening
            "mohfw_htn_001_c0117",  # AGREE II Instrument
            "mohfw_htn_001_c0135",  # Smoking/cuff size
        }
        assert not any(cid in noise_ids for cid in hit_ids)

    def test_query_b_diabetes_first_line_drug(self, retriever: HybridRetriever) -> None:
        """Query b: 'Patient with type 2 diabetes and hypertension, which drug class first?'"""
        q = "Patient with type 2 diabetes and hypertension, which drug class first?"
        p = {"conditions": ["type_2_diabetes", "hypertension"]}
        res = retriever.retrieve(q, top_k=5, patient_state=p)

        assert not res["is_out_of_scope"]
        hits = res["hits"]
        assert len(hits) == 5
        hit_ids = [h["chunk_id"] for h in hits]

        # Must include NICE Step 1 / WHO first-line recommendations
        t2dm_firstline_candidates = {
            "nice_htn_001_c0057",  # NICE 1.4.32 Step 1 ACEi/ARB in T2DM
            "nice_htn_001_c0068",  # NICE 1.4.43 T2DM
            "nice_htn_001_c0060",  # NICE 1.4.34-35 CCB / avoid dual RAAS
            "who_htn_001_c0017",  # WHO First-line agents
            "who_htn_001_c0044",  # WHO First-line agents
        }
        assert any(cid in t2dm_firstline_candidates for cid in hit_ids)

    def test_query_c_target_age_84(self, retriever: HybridRetriever) -> None:
        """Query c: 'Age 84, what is the BP target?'"""
        q = "Age 84, what is the BP target?"
        p = {"age": 84}
        res = retriever.retrieve(q, top_k=5, patient_state=p)

        assert not res["is_out_of_scope"]
        hits = res["hits"]
        hit_ids = [h["chunk_id"] for h in hits]

        # Must include NICE 1.4.21 (<150/90 for age 80+) or MoHFW HYVET 80+
        assert "nice_htn_001_c0047" in hit_ids or "mohfw_htn_001_c0179" in hit_ids
        # NICE 1.4.21 must be the top ranked or top 2 result
        assert hit_ids[0] == "nice_htn_001_c0047" or hit_ids[1] == "nice_htn_001_c0047"

    def test_query_d_pregnant_enalapril(self, retriever: HybridRetriever) -> None:
        """Query d: '26 weeks pregnant, can I take enalapril?'"""
        q = "26 weeks pregnant, can I take enalapril?"
        p = {"is_pregnant": True, "conditions": ["hypertension"]}
        res = retriever.retrieve(q, top_k=5, patient_state=p)

        assert not res["is_out_of_scope"]
        hits = res["hits"]
        hit_ids = [h["chunk_id"] for h in hits]

        # Must include pregnancy safety or ACEi contraindication chunks
        contraindication_chunks = {
            "who_htn_001_c0065",  # WHO 4.3 Pregnancy and hypertension
            "who_htn_001_c0066",  # WHO 4.3 Pregnancy and hypertension (Part 2)
            "nice_htn_001_c0055",  # NICE 1.4.30 MHRA advice on ACEi in pregnancy
            "nice_htn_001_c0059",  # NICE 1.4.33 MHRA advice on ACEi in pregnancy
            "nice_htn_001_c0073",  # NICE 1.4.48 MHRA safety advice in pregnancy
        }
        assert any(cid in contraindication_chunks for cid in hit_ids)

    def test_query_e_bp_108_in_scope(self, retriever: HybridRetriever) -> None:
        """Query e: 'BP 108' must not be rejected as out-of-scope."""
        q = "BP 108"
        res = retriever.retrieve(q, top_k=5)
        assert not res["is_out_of_scope"]
        assert len(res["hits"]) > 0


class TestGateConsistencyAndFormatting:
    """Verify gate decision badge consistency and synthesized response structure."""

    def test_clarify_gate_consistency(self, orchestrator: ChatbotOrchestrator) -> None:
        """A contradiction leading to action_type 'clarify' must yield GateDecision.CLARIFY."""
        session_id = "test_gate_clarify_session"
        orchestrator.clear_session(session_id)

        # Turn 1: establishes normal blood pressure
        orchestrator.handle_turn(
            session_id, "Patient reports normal blood pressure and no history of hypertension."
        )

        # Turn 2: reports elevated clinic reading without explanation -> contradiction
        res2 = orchestrator.handle_turn(
            session_id, "In clinic today, their blood pressure measured 168/104 mmHg."
        )
        assert res2.action_type == "clarify"
        assert res2.verification_result is not None
        assert res2.verification_result.gate_decision == GateDecision.CLARIFY

    def test_synthesised_summary_header_present(self, orchestrator: ChatbotOrchestrator) -> None:
        """Response must start with short synthesized answer under '### Clinical Summary'."""
        session_id = "test_synth_summary_session"
        orchestrator.clear_session(session_id)

        res = orchestrator.handle_turn(
            session_id,
            "58-year-old woman, BP 152/96 on two clinic readings, what is the target?",
        )
        assert res.response_text.startswith("### Clinical Summary")
        assert "below 140/90 mmHg" in res.response_text
        assert "### Guideline Recommendation(s)" in res.response_text

    def test_pregnancy_state_extraction(self) -> None:
        """PatientStateManager must extract pregnancy status from conversational variants."""
        mgr = PatientStateManager()
        st, _ = mgr.update_from_text("26 weeks pregnant, can I take enalapril?")
        assert st.is_pregnant is True
        assert st.pregnancy_weeks == 26
        assert st.sex == "female"
