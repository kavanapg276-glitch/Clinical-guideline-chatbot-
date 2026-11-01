"""Public interfaces and schemas for the ClinCoherence verification layer.

Defines:
- GateDecision: "pass" | "clarify" | "warn" | "refuse"
- ViolationType: The 6 clinical failure modes (Target Mismatch, Patient Context,
  Belief Reversal, Reasoning-Action, Evidence Mismatch, Correction Persistence)
- CaseState: Immutable snapshot of patient clinical context
- Turn: Single conversational turn history record
- VerificationResult: Comprehensive verification outcome with decision gate
- CoherenceVerifier: Abstract base class for verification implementations
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from guideline_chatbot.chunking.schemas import GuidelineChunk

if TYPE_CHECKING:
    from guideline_chatbot.chatbot.patient_state import PatientState


class GateDecision(str, Enum):
    """Gating decision produced by the verification layer."""

    PASS = "pass"
    CLARIFY = "clarify"
    WARN = "warn"
    REFUSE = "refuse"


class ViolationType(str, Enum):
    """The 6 clinical failure modes evaluated by ClinCoherence."""

    TARGET_MISMATCH = "target_mismatch"
    PATIENT_CONTEXT_MISMATCH = "patient_context_mismatch"
    UNJUSTIFIED_BELIEF_REVERSAL = "unjustified_belief_reversal"
    REASONING_ACTION_INCONSISTENCY = "reasoning_action_inconsistency"
    EVIDENCE_MISMATCH = "evidence_mismatch"
    CORRECTION_PERSISTENCE = "correction_persistence"


class ViolationSeverity(str, Enum):
    """Severity level of an identified coherence violation."""

    CRITICAL = "critical"  # Triggers REFUSE gate
    WARNING = "warning"  # Triggers WARN gate
    ADVISORY = "advisory"  # Logged but allows PASS


class Violation(BaseModel):
    """Specific clinical violation identified during response verification."""

    category: ViolationType
    severity: ViolationSeverity
    description: str
    trigger_text: str = ""
    suggested_action: str = ""


class CaseState(BaseModel):
    """Structured patient case context passed to the verifier."""

    age: int | None = None
    sex: str | None = None
    is_pregnant: bool = False
    is_breastfeeding: bool = False
    sbp: float | None = None
    dbp: float | None = None
    abpm_daytime_sbp: float | None = None
    abpm_daytime_dbp: float | None = None
    bmi: float | None = None
    conditions: set[str] = Field(default_factory=set)
    medications: set[str] = Field(default_factory=set)
    allergies: set[str] = Field(default_factory=set)
    egfr: float | None = None
    creatinine: float | None = None
    hba1c: float | None = None
    urine_acr: float | None = None
    turn_count: int = 0
    disputed_facts_count: int = 0

    @classmethod
    def from_patient_state(cls, p: PatientState) -> CaseState:
        """Construct CaseState snapshot from active PatientState."""
        return cls(
            age=p.age,
            sex=p.sex,
            is_pregnant=p.is_pregnant,
            is_breastfeeding=p.is_breastfeeding,
            sbp=p.sbp,
            dbp=p.dbp,
            abpm_daytime_sbp=p.abpm_daytime_sbp,
            abpm_daytime_dbp=p.abpm_daytime_dbp,
            bmi=p.bmi,
            conditions=set(p.conditions),
            medications=set(p.medications),
            allergies=set(p.allergies),
            egfr=p.egfr,
            creatinine=p.creatinine,
            hba1c=p.hba1c,
            urine_acr=p.urine_acr,
            turn_count=p.turn_count,
            disputed_facts_count=len(p.active_conflicts),
        )


class Turn(BaseModel):
    """Historical conversational turn representation."""

    turn_index: int
    user_message: str
    response_text: str
    patient_state_summary: str = ""
    retrieved_chunk_ids: list[str] = Field(default_factory=list)


class VerificationResult(BaseModel):
    """Result of clinical coherence verification."""

    gate_decision: GateDecision
    violations: list[Violation] = Field(default_factory=list)
    modified_response: str | None = None
    explanation: str = ""
    verifier_name: str = "clincoherence"

    @property
    def passed(self) -> bool:
        """Return True if decision is PASS."""
        return self.gate_decision == GateDecision.PASS

    @property
    def has_critical_violations(self) -> bool:
        """Return True if any critical violations are present."""
        return any(v.severity == ViolationSeverity.CRITICAL for v in self.violations)


class CoherenceVerifier(ABC):
    """Abstract interface for clinical conversation coherence verifiers."""

    @abstractmethod
    def verify(
        self,
        case_state: CaseState,
        draft_response: str,
        retrieved_chunks: list[GuidelineChunk] | list[dict[str, Any]],
        conversation_history: list[Turn],
        current_user_message: str = "",
    ) -> VerificationResult:
        """Verify the draft clinical response against case state, guidelines, and history."""
        pass
