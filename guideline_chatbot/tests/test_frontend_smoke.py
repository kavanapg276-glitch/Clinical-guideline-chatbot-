"""Smoke test for the Streamlit clinical frontend and theme rendering."""

from __future__ import annotations

import os

from frontend.app import get_llm_mode_label
from frontend.theme import render_gate_badge
from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator
from guideline_chatbot.coherence.pipeline import ArmMode


def test_theme_gate_badges_rendering() -> None:
    """Verify that gate badge HTML generator outputs correct classes and labels."""
    badge_pass = render_gate_badge("pass")
    assert "gate-pill-pass" in badge_pass
    assert "PASS" in badge_pass

    badge_warn = render_gate_badge("warn", reason="Borderline guideline dosage")
    assert "gate-pill-warn" in badge_warn
    assert "WARN" in badge_warn
    assert "Borderline guideline dosage" in badge_warn

    badge_clarify = render_gate_badge("clarify")
    assert "gate-pill-clarify" in badge_clarify
    assert "CLARIFY" in badge_clarify

    badge_refuse = render_gate_badge("refuse", reason="Contraindicated in pregnancy")
    assert "gate-pill-refuse" in badge_refuse
    assert "REFUSE" in badge_refuse
    assert "Contraindicated in pregnancy" in badge_refuse


def test_llm_mode_label() -> None:
    """Verify LLM mode banner reflects environment state without throwing."""
    # Without real API keys
    os.environ.pop("OPENAI_API_KEY", None)
    os.environ.pop("LLM_API_KEY", None)
    label = get_llm_mode_label()
    assert "Mock LLM" in label or "Deterministic" in label


def test_orchestrator_turn_for_ui() -> None:
    """Verify orchestrator handles a turn and produces a TurnResult consumable by UI."""
    orc = ChatbotOrchestrator.create_default(arm_mode=ArmMode.ARM3_CLINCOHERENCE)
    res = orc.handle_turn("smoke_test_session", "Patient is 50yo with confirmed BP 152/94 mmHg.")

    assert res.turn_index >= 1
    assert res.response_text != ""
    assert res.verification_result is not None
    assert res.verification_result.gate_decision in ("pass", "warn", "clarify", "refuse")
    assert res.patient_state.sbp == 152.0
    assert res.patient_state.dbp == 94.0
