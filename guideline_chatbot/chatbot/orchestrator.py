"""Single entry point orchestrator for multi-turn clinical decision support.

Integrates:
- Multi-turn PatientStateManager
- HybridRetriever (dense + sparse + patient-aware re-ranking)
- ClinicalResponseGenerator (structured recommendations, abstention, pushback)
- CitationValidator (grounding verification)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from guideline_chatbot.chatbot.citation_validator import (
    CitationValidationResult,
    CitationValidator,
)
from guideline_chatbot.chatbot.generator import ClinicalResponseGenerator
from guideline_chatbot.chatbot.llm_client import LLMClient, get_llm_client
from guideline_chatbot.chatbot.patient_state import DisputedFact, PatientState, PatientStateManager
from guideline_chatbot.retrieval.hybrid import HybridRetriever

logger = logging.getLogger(__name__)


def _utc_timestamp() -> str:
    """Return ISO 8601 formatted UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TurnResult:
    """Structured result of a single conversational turn."""

    session_id: str
    turn_index: int
    user_message: str
    response_text: str
    patient_state: PatientState
    retrieved_chunks: list[dict[str, Any]]
    disagreements: list[dict[str, Any]]
    disputed_facts: list[DisputedFact]
    citation_validation: CitationValidationResult
    is_abstention: bool
    action_type: str  # "recommendation" | "clarify" | "abstain" | "pushback_reaffirm"
    state_delta: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=_utc_timestamp)


class ChatbotOrchestrator:
    """Orchestrates multi-turn clinical interactions, patient state, retrieval, and generation."""

    @classmethod
    def create_default(
        cls,
        chunks_path: str = "guideline_chatbot/data/processed/guideline_chunks.json",
        chroma_dir: str = "chroma",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        llm_client: LLMClient | None = None,
    ) -> ChatbotOrchestrator:
        """Create orchestrator with default pre-indexed hybrid retriever and mock or configured LLM."""
        retriever = HybridRetriever.load_default(
            chunks_path=chunks_path,
            chroma_dir=chroma_dir,
            model_name=model_name,
        )
        client = llm_client or get_llm_client()
        generator = ClinicalResponseGenerator(llm_client=client)
        citation_validator = CitationValidator()
        return cls(
            retriever=retriever,
            generator=generator,
            citation_validator=citation_validator,
        )

    def __init__(
        self,
        retriever: HybridRetriever,
        generator: ClinicalResponseGenerator,
        citation_validator: CitationValidator | None = None,
    ) -> None:
        self.retriever = retriever
        self.generator = generator
        self.citation_validator = citation_validator or CitationValidator()
        self.sessions: dict[str, PatientStateManager] = {}
        self.session_histories: dict[str, list[TurnResult]] = {}

    def get_or_create_session(self, session_id: str) -> PatientStateManager:
        """Retrieve existing session state manager or initialize a new one."""
        if session_id not in self.sessions:
            self.sessions[session_id] = PatientStateManager()
            self.session_histories[session_id] = []
        return self.sessions[session_id]

    def clear_session(self, session_id: str) -> None:
        """Reset session state and history."""
        self.sessions.pop(session_id, None)
        self.session_histories.pop(session_id, None)

    def get_session_state(self, session_id: str) -> PatientState:
        """Get the current PatientState for a given session."""
        manager = self.get_or_create_session(session_id)
        return manager.state

    def handle_turn(self, session_id: str, user_message: str) -> TurnResult:
        """Process a single conversational turn end-to-end.

        Args:
            session_id: Unique identifier for the conversation session.
            user_message: Raw user input text.

        Returns:
            TurnResult containing verified response, state, citations, and metadata.
        """
        state_mgr = self.get_or_create_session(session_id)
        prev_ctx = (
            state_mgr.state.to_retrieval_context() if state_mgr.state.turn_count > 0 else None
        )

        # 1. Update patient state from message text and detect conflicts
        current_state, new_conflicts = state_mgr.update_from_text(user_message)
        turn_idx = current_state.turn_count
        state_delta = PatientStateManager.compute_state_delta(
            prev_ctx, current_state.to_retrieval_context()
        )

        # 2. Retrieve guideline evidence
        retrieval_res = self.retriever.retrieve(
            query=user_message,
            top_k=5,
            patient_state=current_state.to_retrieval_context(),
        )

        # 3. Generate response
        gen_res = self.generator.generate_response(
            query=user_message,
            retrieval_result=retrieval_res,
            patient_state=current_state,
        )

        response_text = gen_res["text"]
        action_type = gen_res["action_type"]
        is_abstention = gen_res["is_abstention"]

        # 4. Validate citations against retrieved evidence
        citation_val = self.citation_validator.validate(
            text=response_text,
            retrieved_chunks=retrieval_res.get("hits", []),
        )

        turn_result = TurnResult(
            session_id=session_id,
            turn_index=turn_idx,
            user_message=user_message,
            response_text=response_text,
            patient_state=current_state,
            retrieved_chunks=retrieval_res.get("hits", []),
            disagreements=retrieval_res.get("disagreements", []),
            disputed_facts=list(current_state.disputed_facts),
            citation_validation=citation_val,
            is_abstention=is_abstention,
            action_type=action_type,
            state_delta=state_delta,
        )

        self.session_histories[session_id].append(turn_result)
        return turn_result
