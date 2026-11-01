"""Phase 3 Test Suite: Patient State, Generation, Verification, and Multi-Turn Orchestration.

Verifies:
- Multi-turn patient state extraction (vitals, labs, medications, allergies)
- Contradiction detection (BP conflicts, condition denial, med/allergy disputes, age shifts)
- Agnostic LLM client abstraction and deterministic mock generation
- Citation parsing and validation against retrieved chunk evidence
- Out-of-scope domain abstention gating
- Pushback detection and evidence reaffirmation
- End-to-end multi-turn orchestrator session execution
"""

from __future__ import annotations

import pytest

from guideline_chatbot.chatbot.citation_validator import CitationValidator
from guideline_chatbot.chatbot.generator import ClinicalResponseGenerator
from guideline_chatbot.chatbot.llm_client import MockLLMClient, get_llm_client
from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator
from guideline_chatbot.chatbot.patient_state import PatientStateManager


class TestPatientState:
    """Tests for PatientStateManager extraction and contradiction detection."""

    def test_vitals_and_demographics_extraction(self) -> None:
        mgr = PatientStateManager()
        state, conflicts = mgr.update_from_text(
            "Patient is a 55-year-old female with blood pressure of 145/92 mmHg."
        )

        assert state.age == 55
        assert state.sex == "female"
        assert state.sbp == 145.0
        assert state.dbp == 92.0
        assert "hypertension" in state.conditions
        assert len(conflicts) == 0

    def test_labs_and_condition_inference(self) -> None:
        mgr = PatientStateManager()
        state, conflicts = mgr.update_from_text(
            "Recent labs show HbA1c 8.4%, eGFR 48 mL/min, and microalbuminuria."
        )

        assert state.hba1c == 8.4
        assert state.egfr == 48.0
        assert "type_2_diabetes" in state.conditions
        assert "chronic_kidney_disease" in state.conditions
        assert "microalbuminuria" in state.conditions
        assert len(conflicts) == 0

    def test_medications_and_allergies_extraction(self) -> None:
        mgr = PatientStateManager()
        state, conflicts = mgr.update_from_text(
            "Currently taking amlodipine and metformin. Allergic to penicillin."
        )

        assert "amlodipine" in state.medications
        assert "metformin" in state.medications
        assert "penicillin" in state.allergies
        assert len(conflicts) == 0

    def test_contradiction_bp_normotensive_vs_hypertensive(self) -> None:
        mgr = PatientStateManager()
        # Turn 1: asserts normal blood pressure
        mgr.update_from_text("Patient reports normal blood pressure and no complaints.")
        assert "normotensive_claim" in mgr.state.conditions

        # Turn 2: reports Grade 2 hypertension reading
        state, conflicts = mgr.update_from_text(
            "In clinic today, their blood pressure measured 165/102 mmHg."
        )
        assert len(conflicts) == 1
        assert conflicts[0].field == "blood_pressure"
        assert state.has_conflicts is True
        assert state.sbp == 165.0
        assert "hypertension" in state.conditions

    def test_contradiction_diabetes_presence_vs_denial(self) -> None:
        mgr = PatientStateManager()
        # Turn 1: sets diabetes
        mgr.update_from_text("Diagnosed with type 2 diabetes with HbA1c 7.9%.")
        assert "type_2_diabetes" in mgr.state.conditions

        # Turn 2: denies diabetes
        state, conflicts = mgr.update_from_text("Actually, I don't have diabetes.")
        assert len(conflicts) == 1
        assert conflicts[0].field == "type_2_diabetes"
        assert "type_2_diabetes" not in state.conditions

    def test_contradiction_medication_denial_vs_report(self) -> None:
        mgr = PatientStateManager()
        # Turn 1: claims no medicines
        mgr.update_from_text("Patient takes no medicines at all.")
        assert "no_meds_claim" in mgr.state.conditions

        # Turn 2: reports taking amlodipine
        state, conflicts = mgr.update_from_text("Patient mentions taking amlodipine daily.")
        assert len(conflicts) == 1
        assert conflicts[0].field == "medications"
        assert "amlodipine" in state.medications

    def test_contradiction_allergy_denial_vs_report(self) -> None:
        mgr = PatientStateManager()
        # Turn 1: claims no allergies
        mgr.update_from_text("No drug allergies reported.")
        assert "no_allergies_claim" in mgr.state.conditions

        # Turn 2: reports penicillin allergy
        state, conflicts = mgr.update_from_text("Patient is allergic to penicillin.")
        assert len(conflicts) == 1
        assert conflicts[0].field == "allergies"
        assert "penicillin" in state.allergies

    def test_contradiction_age_shift(self) -> None:
        mgr = PatientStateManager()
        mgr.update_from_text("Patient is 45 years old.")
        assert mgr.state.age == 45

        state, conflicts = mgr.update_from_text("Patient is 72 years old.")
        assert len(conflicts) == 1
        assert conflicts[0].field == "age"
        assert state.age == 72


class TestCitationValidator:
    """Tests for parsing and grounding verification of citations."""

    def test_extract_citations(self) -> None:
        validator = CitationValidator()
        text = (
            "According to guidelines [NICE Guideline NG136, p. 15, §1.4.15, 2019] and "
            "[ICMR STW Hypertension, p. 1, §Pharmacotherapy, 2026], CCB is recommended."
        )
        citations = validator.extract_citations(text)
        assert len(citations) == 2
        assert citations[0].doc_identifier == "NICE Guideline NG136"
        assert citations[0].page == 15
        assert citations[0].year == "2019"
        assert citations[1].doc_identifier == "ICMR STW Hypertension"
        assert citations[1].page == 1

    def test_validate_matching_citations(self) -> None:
        validator = CitationValidator()
        retrieved_chunks = [
            {
                "chunk_id": "nice_htn_001_c0022",
                "metadata": {
                    "doc_id": "nice_htn_001",
                    "document_name": "NICE Guideline NG136: Hypertension in Adults",
                    "issuing_organization": "National Institute for Health and Care Excellence (NICE)",
                    "page_start": 14,
                    "page_end": 16,
                    "heading": "1.4 Initial pharmacotherapy",
                    "recommendation_year": "2019",
                },
            }
        ]
        text = "First line drug recommendation [NICE Guideline NG136, p. 15, §1.4 Initial pharmacotherapy, 2019]."
        result = validator.validate(text, retrieved_chunks)
        assert result.valid is True
        assert len(result.validated_citations) == 1
        assert len(result.unverified_citations) == 0

    def test_validate_unverified_citations(self) -> None:
        validator = CitationValidator()
        retrieved_chunks = [
            {
                "chunk_id": "who_htn_001_c0010",
                "metadata": {
                    "doc_id": "who_htn_001",
                    "document_name": "WHO Guideline on Pharmacological Treatment of Hypertension",
                    "issuing_organization": "World Health Organization (WHO)",
                    "page_start": 20,
                    "page_end": 22,
                },
            }
        ]
        # Text cites a fabricated AHA guideline not in retrieved chunks
        text = "American guidelines state [AHA Hypertension 2024, p. 88] to start immediately."
        result = validator.validate(text, retrieved_chunks)
        assert result.valid is False
        assert len(result.unverified_citations) == 1
        assert result.unsupported_claims_flagged is True


class TestLLMClientAndGenerator:
    """Tests for LLM clients and structured clinical response generator."""

    def test_mock_llm_factory(self) -> None:
        client = get_llm_client(provider="mock")
        assert isinstance(client, MockLLMClient)
        out = client.generate("test prompt")
        assert "Clinical Guideline Recommendation" in out

    def test_generator_out_of_scope_abstention(self) -> None:
        gen = ClinicalResponseGenerator()
        mgr = PatientStateManager()
        res = gen.generate_response(
            query="What is the pediatric amoxicillin dosing for otitis media in a 3-year-old?",
            retrieval_result={"hits": [], "disagreements": [], "is_out_of_scope": True},
            patient_state=mgr.state,
        )
        assert res["is_abstention"] is True
        assert res["action_type"] == "abstain"
        assert "Out-of-Scope Query" in res["text"]

    def test_generator_clarification_on_contradiction(self) -> None:
        gen = ClinicalResponseGenerator()
        mgr = PatientStateManager()
        mgr.update_from_text("Patient has normal blood pressure.")
        mgr.update_from_text("BP measured 170/110 mmHg.")

        res = gen.generate_response(
            query="What should we start?",
            retrieval_result={
                "hits": [{"chunk_id": "dummy"}],
                "disagreements": [],
                "is_out_of_scope": False,
            },
            patient_state=mgr.state,
        )
        assert res["action_type"] == "clarify"
        assert "Clarification Required" in res["text"]

    def test_generator_pushback_handling(self) -> None:
        gen = ClinicalResponseGenerator()
        mgr = PatientStateManager()
        mgr.update_from_text("Blood pressure is 154/96 mmHg.")

        fake_hits = [
            {
                "chunk_id": "nice_htn_001_c0022",
                "text": "Offer antihypertensive drug treatment to people aged under 80 with stage 1 hypertension.",
                "metadata": {
                    "document_name": "NICE Guideline NG136",
                    "page_start": 14,
                    "heading": "1.4 Treatment",
                    "recommendation_year": "2019",
                },
            }
        ]

        res = gen.generate_response(
            query="Patient refuses pills and insists on diet and exercise only. Can we do only lifestyle changes?",
            retrieval_result={"hits": fake_hits, "disagreements": [], "is_out_of_scope": False},
            patient_state=mgr.state,
        )
        assert res["action_type"] == "pushback_reaffirm"
        assert "Non-Pharmacological Measures vs. Pharmacotherapy" in res["text"]
        assert "lifestyle modification alone is insufficient" in res["text"]


@pytest.fixture(scope="module")
def orchestrator() -> ChatbotOrchestrator:
    return ChatbotOrchestrator.create_default()


class TestOrchestratorMultiTurn:
    """End-to-end integration tests for ChatbotOrchestrator."""

    def test_orchestrator_stage1_hypertension_turn(self, orchestrator: ChatbotOrchestrator) -> None:
        sid = "test_orch_s1"
        res = orchestrator.handle_turn(
            session_id=sid,
            user_message="50-year-old male with confirmed clinic BP 146/92 mmHg.",
        )

        assert res.turn_index == 1
        assert res.action_type == "recommendation"
        assert res.is_abstention is False
        assert res.patient_state.age == 50
        assert res.patient_state.sex == "male"
        assert res.patient_state.sbp == 146.0
        assert len(res.retrieved_chunks) > 0
        assert res.citation_validation.valid is True
        assert res.citation_validation.total_citations >= 1

    def test_orchestrator_out_of_scope_rejection(self, orchestrator: ChatbotOrchestrator) -> None:
        sid = "test_orch_s2"
        res = orchestrator.handle_turn(
            session_id=sid,
            user_message="Pediatric chemotherapy dosing for acute lymphoblastic leukemia.",
        )

        assert res.is_abstention is True
        assert res.action_type == "abstain"
        assert "Out-of-Scope Query" in res.response_text

    def test_orchestrator_multi_turn_gradual_disclosure(
        self, orchestrator: ChatbotOrchestrator
    ) -> None:
        sid = "test_orch_s3"
        # Turn 1
        res1 = orchestrator.handle_turn(
            session_id=sid,
            user_message="54-year-old female with BP 152/94 mmHg.",
        )
        assert "hypertension" in res1.patient_state.conditions

        # Turn 2
        res2 = orchestrator.handle_turn(
            session_id=sid,
            user_message="She also has type 2 diabetes with HbA1c 8.1%.",
        )
        assert res2.turn_index == 2
        assert "type_2_diabetes" in res2.patient_state.conditions
        assert res2.patient_state.hba1c == 8.1

        # Turn 3
        res3 = orchestrator.handle_turn(
            session_id=sid,
            user_message="Her urine ACR is 4.5 mg/mmol indicating microalbuminuria.",
        )
        assert res3.turn_index == 3
        assert "microalbuminuria" in res3.patient_state.conditions
        assert "chronic_kidney_disease" not in res3.patient_state.conditions
        assert res3.citation_validation.valid is True

    def test_single_acr_does_not_infer_ckd(self) -> None:
        mgr = PatientStateManager()
        state, conflicts = mgr.update_from_text(
            "Patient with hypertension; recent urine ACR is 4.2 mg/mmol and eGFR is 82 mL/min."
        )
        assert state.urine_acr == 4.2
        assert "microalbuminuria" in state.conditions
        assert "chronic_kidney_disease" not in state.conditions
        assert state.egfr == 82.0

    def test_past_bp_vs_present_bp_not_a_contradiction(self) -> None:
        mgr = PatientStateManager()
        # Turn 1: historical normal BP
        mgr.update_from_text("Patient reports blood pressure was normal in the past.")
        # Turn 2: today's reading
        state, conflicts = mgr.update_from_text("Today in clinic, BP is 152/94 mmHg.")
        assert len(conflicts) == 0
        assert state.sbp == 152.0
        assert state.has_conflicts is False

    def test_contradiction_resolution_marks_resolved(self) -> None:
        mgr = PatientStateManager()
        # Turn 1
        mgr.update_from_text("Patient reports normal blood pressure.")
        # Turn 2: unclarified contradiction
        mgr.update_from_text("BP measured 168/104 mmHg today.")
        assert mgr.state.has_conflicts is True
        assert len(mgr.state.active_conflicts) == 1

        # Turn 3: clinician resolves/confirms
        state, conflicts = mgr.update_from_text(
            "To clarify, the 168/104 mmHg reading today is confirmed on repeat measurement."
        )
        assert state.has_conflicts is False
        assert len(state.active_conflicts) == 0
        assert state.disputed_facts[0].is_resolved is True
        assert state.disputed_facts[0].resolution_turn == 3

    def test_dynamic_missing_info_derivation(self) -> None:
        gen = ClinicalResponseGenerator()
        from guideline_chatbot.chatbot.patient_state import PatientState

        p_state = PatientState(sbp=150.0, dbp=92.0)
        hits = [
            {
                "text": "Offer ABPM to confirm diagnosis. Check serum potassium and eGFR prior to initiating ACEi.",
                "metadata": {
                    "applicability_conditions": "For adults with clinic BP >= 140/90, confirm with ABPM",
                    "exceptions": "Avoid if eGFR < 30 or serum potassium > 5.0",
                },
            }
        ]
        missing = gen._derive_missing_info(hits, p_state)
        assert any("ABPM" in m for m in missing)
        assert any("Renal Function" in m or "eGFR" in m for m in missing)
        assert any("Potassium" in m for m in missing)
