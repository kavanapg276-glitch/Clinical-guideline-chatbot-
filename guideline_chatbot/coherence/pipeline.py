"""Three-Arm Verification Pipeline for comparative evaluation.

Supports:
- Arm 1 (Baseline): Direct unverified output from clinical generator
- Arm 2 (Self-Check): Prompt-based LLM self-reflection simulation
- Arm 3 (ClinCoherence): Real-time, state-aware rule-based verification layer with decision gates
"""

from __future__ import annotations

import re
from enum import Enum
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
from guideline_chatbot.coherence.verifier import RuleBasedCoherenceVerifier


class ArmMode(str, Enum):
    """The three evaluation arms defined in the thesis."""

    ARM1_BASELINE = "arm1_baseline"
    ARM2_SELF_CHECK = "arm2_self_check"
    ARM3_CLINCOHERENCE = "arm3_clincoherence"


class CoherencePipeline:
    """Manages multi-arm clinical verification execution."""

    def __init__(
        self,
        verifier: CoherenceVerifier | None = None,
        mode: ArmMode = ArmMode.ARM3_CLINCOHERENCE,
    ) -> None:
        self.verifier = verifier or RuleBasedCoherenceVerifier()
        self.mode = mode

    def process(
        self,
        case_state: CaseState,
        draft_response: str,
        retrieved_chunks: list[GuidelineChunk] | list[dict[str, Any]],
        conversation_history: list[Turn],
        current_user_message: str = "",
    ) -> VerificationResult:
        """Route verification through the configured experimental arm."""
        if self.mode == ArmMode.ARM1_BASELINE:
            return VerificationResult(
                gate_decision=GateDecision.PASS,
                violations=[],
                modified_response=draft_response,
                explanation="Arm 1 Baseline: Direct release without verification.",
                verifier_name="arm1_baseline",
            )

        elif self.mode == ArmMode.ARM2_SELF_CHECK:
            return self._run_self_check_arm(
                case_state=case_state,
                draft_response=draft_response,
            )

        else:  # Arm 3: ClinCoherence
            res = self.verifier.verify(
                case_state=case_state,
                draft_response=draft_response,
                retrieved_chunks=retrieved_chunks,
                conversation_history=conversation_history,
                current_user_message=current_user_message,
            )
            return res

    def _run_self_check_arm(self, case_state: CaseState, draft_response: str) -> VerificationResult:
        """Simulate prompt-based self-verification (standard LLM self-reflection).

        Self-checking LLM prompts can catch overt lexical markers (e.g. explicit 'pregnant'
        and 'ramipril' in same sentence), but struggle with multi-turn state persistence,
        temporal progression distinction, or exact guideline dosing ceilings.
        """
        lower = draft_response.lower()
        violations: list[Violation] = []

        # Self-reflection check 1: Overt pregnancy drug mention
        if (
            case_state.is_pregnant
            and re.search(r"\b(?:ramipril|enalapril|losartan|telmisartan)\b", lower)
            and not re.search(r"\b(?:contraindicated|avoid|do\s+not)\b", lower)
        ):
            violations.append(
                Violation(
                    category=ViolationType.PATIENT_CONTEXT_MISMATCH,
                    severity=ViolationSeverity.CRITICAL,
                    description="Self-check prompt flagged potential teratogenic drug in pregnancy.",
                    trigger_text="ACEi/ARB mentioned in pregnancy context",
                    suggested_action="Review pregnancy guidelines.",
                )
            )

        # Self-reflection check 2: Supratherapeutic obvious dose
        if re.search(r"\bramipril\s+(?:20|50)\s*mg\b", lower):
            violations.append(
                Violation(
                    category=ViolationType.EVIDENCE_MISMATCH,
                    severity=ViolationSeverity.CRITICAL,
                    description="Self-check prompt flagged high Ramipril dose.",
                    trigger_text="Ramipril dose above standard range",
                    suggested_action="Adjust dose.",
                )
            )

        if any(v.severity == ViolationSeverity.CRITICAL for v in violations):
            modified = (
                "🛑 **[LLM SELF-CHECK SAFETY ALERT]**\n\n"
                "The system self-check identified a safety concern with the draft recommendation:\n"
                + "\n".join(f"- {v.description}" for v in violations)
            )
            return VerificationResult(
                gate_decision=GateDecision.REFUSE,
                violations=violations,
                modified_response=modified,
                explanation="Arm 2 Self-Check: Flagged overt safety issue.",
                verifier_name="arm2_self_check",
            )

        return VerificationResult(
            gate_decision=GateDecision.PASS,
            violations=[],
            modified_response=draft_response,
            explanation="Arm 2 Self-Check: Passed self-reflection prompt.",
            verifier_name="arm2_self_check",
        )
