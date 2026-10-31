"""Multi-turn interactive terminal REPL for clinical guideline decision support.

Provides terminal chat with commands:
  /state     - Inspect active patient state
  /conflicts - View detected clinical contradictions
  /clear     - Reset conversation and patient state
  /help      - View available commands
  /quit      - Exit the REPL
"""

from __future__ import annotations

import argparse
import uuid

from guideline_chatbot.chatbot.llm_client import get_llm_client
from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator


def print_banner() -> None:
    """Print welcome header and clinical scope information."""
    print("=" * 76)
    print(" CLINCOHERENCE GUIDELINE DECISION SUPPORT SYSTEM (Phase 3 REPL)")
    print(" Jurisdictions: MoHFW (India STG 2016), ICMR (STW), WHO, NICE (UK)")
    print(" Clinical Scope: Adult Essential Hypertension & Type 2 Diabetes")
    print("=" * 76)
    print("Commands: /state, /conflicts, /clear, /help, /quit\n")


def print_help() -> None:
    """Print help instructions."""
    print("\nAvailable Commands:")
    print("  /state     : Display current structured patient profile (vitals, labs, meds)")
    print("  /conflicts : Display any clinical contradictions / disputed facts")
    print("  /clear     : Reset current session state and conversation history")
    print("  /help      : Show this help message")
    print("  /quit      : Exit the clinical REPL\n")


def run_cli(
    provider: str = "mock",
    model: str | None = None,
    session_id: str | None = None,
) -> None:
    """Start interactive clinical chat session."""
    active_session_id = session_id or str(uuid.uuid4())[:8]

    llm = get_llm_client(provider=provider, model=model)
    print("Initializing Guideline Retrieval & Verification Engine...")
    orchestrator = ChatbotOrchestrator.create_default(llm_client=llm)

    print_banner()
    print(f"Session started: {active_session_id} (Provider: {provider})\n")

    while True:
        try:
            user_input = input("Clinician/User > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession terminated.")
            break

        if not user_input:
            continue

        cmd = user_input.lower()
        if cmd in {"/quit", "/exit", "quit", "exit"}:
            print("Exiting decision support session. Goodbye.")
            break
        elif cmd == "/help":
            print_help()
            continue
        elif cmd == "/state":
            state = orchestrator.get_session_state(active_session_id)
            print("\n--- Active Patient State ---")
            print(state.to_summary_string())
            print("----------------------------\n")
            continue
        elif cmd == "/conflicts":
            state = orchestrator.get_session_state(active_session_id)
            if not state.disputed_facts:
                print("\nNo clinical contradictions recorded in this session.\n")
            else:
                print(f"\n--- Disputed Facts ({len(state.disputed_facts)}) ---")
                for i, df in enumerate(state.disputed_facts, 1):
                    print(f"{i}. Turn {df.turn_index} [{df.field}]: {df.explanation}")
                print("------------------------------------\n")
            continue
        elif cmd == "/clear":
            orchestrator.clear_session(active_session_id)
            print(f"\nSession {active_session_id} cleared. Patient profile reset.\n")
            continue

        # Execute normal conversational turn
        turn_result = orchestrator.handle_turn(
            session_id=active_session_id,
            user_message=user_input,
        )

        print(f"\nAssistant (Turn {turn_result.turn_index}) [Action: {turn_result.action_type}]:")
        print("-" * 60)
        print(turn_result.response_text)
        print("-" * 60)
        print(f"[{turn_result.citation_validation.summary()}]")

        if turn_result.disputed_facts and turn_result.action_type == "clarify":
            print("[ALERT: Clinical contradiction detected in history]")
        if turn_result.disagreements:
            print(
                f"[NOTE: {len(turn_result.disagreements)} cross-guideline disagreement(s) surfaced]"
            )
        print()


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="ClinCoherence Guideline Chatbot REPL")
    parser.add_argument(
        "--provider",
        choices=["mock", "ollama", "openai", "openai_compatible"],
        default="mock",
        help="LLM provider (default: mock)",
    )
    parser.add_argument("--model", type=str, default=None, help="LLM model name")
    parser.add_argument("--session-id", type=str, default=None, help="Optional session ID")

    args = parser.parse_args()
    run_cli(provider=args.provider, model=args.model, session_id=args.session_id)


if __name__ == "__main__":
    main()
