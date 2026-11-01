"""ClinCoherence verification layer package."""

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
from guideline_chatbot.coherence.pipeline import ArmMode, CoherencePipeline
from guideline_chatbot.coherence.verifier import RuleBasedCoherenceVerifier

__all__ = [
    "ArmMode",
    "CaseState",
    "CoherencePipeline",
    "CoherenceVerifier",
    "GateDecision",
    "RuleBasedCoherenceVerifier",
    "Turn",
    "VerificationResult",
    "Violation",
    "ViolationSeverity",
    "ViolationType",
]
