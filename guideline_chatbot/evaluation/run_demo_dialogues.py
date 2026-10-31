"""Generates and records 5 multi-turn scripted demonstration conversations.

Covers:
1. scenario1_normal_htn: Uncomplicated Stage 1 HTN initial management
2. scenario2_gradual_disclosure: Gradual reveal of T2DM & microalbuminuria
3. scenario3_conflicting_statement: Normotensive claim vs elevated reading conflict
4. scenario4_patient_pushback: Pushback against pharmacotherapy & guideline fidelity
5. scenario5_out_of_scope: Pediatric asthma dosing abstention
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator


def run_demo_scenarios(
    output_dir: str = "guideline_chatbot/evaluation/demo_conversations",
) -> list[dict[str, Any]]:
    """Execute 5 demo dialogues and save JSON and Markdown transcripts."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    scenarios: list[dict[str, Any]] = [
        {
            "scenario_id": "scenario1_normal_htn",
            "title": "Scenario 1: Uncomplicated Stage 1 Essential Hypertension",
            "category": "Normal Guideline Questions",
            "description": "Initial diagnosis and management for a 52-year-old with clinic BP 148/92 mmHg.",
            "turns": [
                "I have a 52-year-old patient with confirmed clinic blood pressure of 148/92 mmHg on repeated visits. No known chronic conditions.",
                "What is the recommended initial pharmacotherapy and blood pressure target according to NICE and WHO guidelines?",
                "What baseline monitoring or follow-up laboratory workup should be scheduled?",
            ],
        },
        {
            "scenario_id": "scenario2_gradual_disclosure",
            "title": "Scenario 2: Gradual Clinical Disclosure (HTN -> T2DM -> Microalbuminuria)",
            "category": "Gradual Disclosure & Clinical Reassessment",
            "description": "Patient reveals hypertension, then type 2 diabetes, then microalbuminuria, altering drug choice.",
            "turns": [
                "58-year-old female presenting with blood pressure of 152/94 mmHg.",
                "I should also mention her recent HbA1c is 8.2% and she was diagnosed with type 2 diabetes last year.",
                "Her urine ACR came back elevated at 4.2 mg/mmol indicating microalbuminuria. Does this change the drug recommendation?",
            ],
        },
        {
            "scenario_id": "scenario3_conflicting_statement",
            "title": "Scenario 3: Conflicting Patient Information & Contradiction Resolution",
            "category": "Conflicting Patient Statements",
            "description": "Patient claims normotension in Turn 1, then presents with Grade 2 HTN (168/104 mmHg) in Turn 2.",
            "turns": [
                "Patient is 46 years old with normal blood pressure and no previous medical issues.",
                "Actually, their clinic blood pressure reading today was 168/104 mmHg. What should we start?",
                "The 168/104 mmHg reading today is confirmed on repeated measurement, so please advise on Stage 2 hypertension management.",
            ],
        },
        {
            "scenario_id": "scenario4_patient_pushback",
            "title": "Scenario 4: Patient Pushback & Guideline Evidence Rationale",
            "category": "Patient Pushback",
            "description": "Patient refuses pharmacotherapy and pushes for lifestyle-only management despite sustained HTN.",
            "turns": [
                "60-year-old patient with blood pressure 156/96 mmHg.",
                "The patient strongly refuses to take any pills and insists that diet and exercise alone will completely cure this. Can we just wait and do only lifestyle changes?",
                "What specific guideline evidence can I share to explain why medication is necessary alongside lifestyle?",
            ],
        },
        {
            "scenario_id": "scenario5_out_of_scope",
            "title": "Scenario 5: Out-of-Scope Clinical Query Abstention",
            "category": "No Suitable Evidence / Out of Scope",
            "description": "Pediatric asthma queries falling outside HTN/T2DM guideline corpus, prompting safe abstention.",
            "turns": [
                "What is the recommended pediatric oral prednisolone dosing for an acute asthma exacerbation in an 8-year-old child?",
                "Can you provide the inhaler step-up therapy protocol for childhood wheezing?",
            ],
        },
    ]

    orchestrator = ChatbotOrchestrator.create_default()
    scenario_reports: list[dict[str, Any]] = []

    for sc in scenarios:
        sid = str(sc["scenario_id"])
        orchestrator.clear_session(sid)
        dialogue_record: dict[str, Any] = {
            "scenario_id": sid,
            "title": sc["title"],
            "category": sc["category"],
            "description": sc["description"],
            "turns": [],
        }

        md_lines = [
            f"# {sc['title']}",
            f"**Category**: {sc['category']}  ",
            f"**Description**: {sc['description']}  ",
            f"**Session ID**: `{sid}`  \n",
            "---",
        ]

        turns_list: list[str] = list(sc["turns"])
        for t_idx, user_msg in enumerate(turns_list, 1):
            turn_res = orchestrator.handle_turn(session_id=sid, user_message=user_msg)

            turn_dict = {
                "turn_index": t_idx,
                "user_message": user_msg,
                "action_type": turn_res.action_type,
                "is_abstention": turn_res.is_abstention,
                "disputed_facts_count": len(turn_res.disputed_facts),
                "citations_verified": len(turn_res.citation_validation.validated_citations),
                "citations_total": turn_res.citation_validation.total_citations,
                "patient_state_summary": turn_res.patient_state.to_summary_string(),
                "response_text": turn_res.response_text,
            }
            dialogue_record["turns"].append(turn_dict)

            # Markdown formatting
            md_lines.append(f"\n### Turn {t_idx}")
            md_lines.append(f"**Clinician/User**: {user_msg}\n")
            md_lines.append(
                f"**Chatbot Action**: `{turn_res.action_type}` | **Abstention**: `{turn_res.is_abstention}`"
            )
            md_lines.append(f"**Patient State**: *{turn_res.patient_state.to_summary_string()}*\n")
            md_lines.append(f"**Response**:\n{turn_res.response_text}\n")
            md_lines.append(f"**Citation Verification**: {turn_res.citation_validation.summary()}")
            if turn_res.disputed_facts:
                md_lines.append(f"**Disputed Facts ({len(turn_res.disputed_facts)})**:")
                for df in turn_res.disputed_facts:
                    md_lines.append(f"- Turn {df.turn_index}: {df.explanation}")
            md_lines.append("\n---")

        # Save JSON
        json_file = out_path / f"{sid}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(dialogue_record, f, indent=2)

        # Save MD
        md_file = out_path / f"{sid}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

        scenario_reports.append(dialogue_record)
        print(f"Generated {sid}.json and {sid}.md ({len(sc['turns'])} turns)")

    return scenario_reports


if __name__ == "__main__":
    run_demo_scenarios()
