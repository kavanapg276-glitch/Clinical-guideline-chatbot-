"""Tests for sidebar patient state synchronization and single-line HTML rendering.

Verifies:
1. Multi-turn state progression across 3 sequential turns (Age/Sex/BP -> Diabetes/HbA1c -> Urine ACR).
2. The patient state card in the sidebar reflects the current turn immediately without lag.
3. The rendered card HTML is a single contiguous string with no newlines or blank lines,
   guaranteeing CommonMark never parses it as an indented code block (<pre><code>).
"""

from __future__ import annotations

from frontend.app import format_patient_card_html
from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator
from guideline_chatbot.coherence.pipeline import ArmMode


def test_sidebar_state_sync_three_turns() -> None:
    """Verify that 3 sequential clinical messages update the patient state and sidebar card immediately."""
    orchestrator = ChatbotOrchestrator.create_default(arm_mode=ArmMode.ARM3_CLINCOHERENCE)
    session_id = "test_sidebar_sync_session"

    # Initial state before any turns
    initial_state = orchestrator.get_session_state(session_id)
    initial_card = format_patient_card_html(initial_state)
    assert "\n" not in initial_card, "Patient card must contain no newlines"
    assert "<pre>" not in initial_card
    assert "Age: Unspecified" in initial_card
    assert "BP: Unrecorded" in initial_card

    # Turn 1: Demographics + BP
    turn1_msg = "58-year-old woman, BP 152/96 on two clinic readings, what is the target?"
    turn1_res = orchestrator.handle_turn(session_id=session_id, user_message=turn1_msg)
    state1 = turn1_res.patient_state

    # Verify Turn 1 state
    assert state1.age == 58, f"Expected age 58, got {state1.age}"
    assert state1.sex == "female", f"Expected female, got {state1.sex}"
    assert state1.sbp == 152.0 and state1.dbp == 96.0, (
        f"Expected 152/96, got {state1.sbp}/{state1.dbp}"
    )
    assert state1.is_pregnant is False

    # Verify Turn 1 card HTML
    card1 = format_patient_card_html(state1)
    assert "\n" not in card1, "Patient card must contain no newlines"
    assert "<pre>" not in card1 and "<code>" not in card1
    assert "Age: 58 yrs" in card1
    assert "Sex: Female" in card1
    assert "BP: 152/96 mmHg" in card1
    assert "HbA1c: Unrecorded" in card1
    assert "ACR: Unrecorded" in card1

    # Turn 2: Type 2 Diabetes + HbA1c
    turn2_msg = "Patient was diagnosed with type 2 diabetes with HbA1c 8.4%."
    turn2_res = orchestrator.handle_turn(session_id=session_id, user_message=turn2_msg)
    state2 = turn2_res.patient_state

    # Verify Turn 2 state accumulates Turn 1
    assert state2.age == 58
    assert state2.sex == "female"
    assert state2.sbp == 152.0
    assert "type_2_diabetes" in state2.conditions
    assert state2.hba1c == 8.4, f"Expected HbA1c 8.4, got {state2.hba1c}"

    # Verify Turn 2 card HTML
    card2 = format_patient_card_html(state2)
    assert "\n" not in card2
    assert "<pre>" not in card2 and "<code>" not in card2
    assert "Age: 58 yrs" in card2
    assert "Sex: Female" in card2
    assert "BP: 152/96 mmHg" in card2
    assert "HbA1c: 8.4%" in card2
    assert "Type 2 Diabetes" in card2
    assert "ACR: Unrecorded" in card2

    # Turn 3: Urine ACR Lab
    turn3_msg = "Recent lab shows urine ACR is 4.5 mg/mmol."
    turn3_res = orchestrator.handle_turn(session_id=session_id, user_message=turn3_msg)
    state3 = turn3_res.patient_state

    # Verify Turn 3 state accumulates all previous turns
    assert state3.age == 58
    assert state3.sex == "female"
    assert state3.sbp == 152.0
    assert "type_2_diabetes" in state3.conditions
    assert "microalbuminuria" in state3.conditions
    assert state3.hba1c == 8.4
    assert state3.urine_acr == 4.5, f"Expected urine ACR 4.5, got {state3.urine_acr}"

    # Verify Turn 3 card HTML
    card3 = format_patient_card_html(state3)
    assert "\n" not in card3
    assert "<pre>" not in card3 and "<code>" not in card3
    assert "Age: 58 yrs" in card3
    assert "Sex: Female" in card3
    assert "BP: 152/96 mmHg" in card3
    assert "HbA1c: 8.4%" in card3
    assert "ACR: 4.5 mg/mmol" in card3
    assert "Type 2 Diabetes" in card3
    assert "Microalbuminuria" in card3


def test_patient_card_no_raw_html_codeblock() -> None:
    """Ensure the patient card HTML has zero multiline blocks or indented text."""
    orchestrator = ChatbotOrchestrator.create_default(arm_mode=ArmMode.ARM3_CLINCOHERENCE)
    state = orchestrator.get_session_state("test_raw_html")
    state.age = 65
    state.sex = "male"
    state.sbp = 148.0
    state.dbp = 92.0
    state.conditions.add("hypertension")
    state.conditions.add("type_2_diabetes")

    card_html = format_patient_card_html(state)

    # 1. No newlines
    assert "\n" not in card_html
    assert "\r" not in card_html

    # 2. Well-formed HTML structure
    assert card_html.startswith('<div class="patient-card">')
    assert card_html.endswith("</div>")
    assert card_html.count("<div") == card_html.count("</div>")

    # 3. No backticks or markdown code fences
    assert "```" not in card_html
    assert "`" not in card_html
