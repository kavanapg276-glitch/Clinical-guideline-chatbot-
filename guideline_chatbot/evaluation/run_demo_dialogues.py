"""Generates and records 10 multi-turn scripted demonstration conversations.

Covers:
1. scenario1_normal_htn: Uncomplicated Stage 1 HTN initial management
2. scenario2_gradual_disclosure: Gradual reveal of T2DM & microalbuminuria (no silent CKD)
3. scenario3_conflicting_statement: Normotensive claim vs elevated reading conflict & resolution
4. scenario4_patient_pushback: Pushback against pharmacotherapy & guideline fidelity
5. scenario5_out_of_scope: Pediatric asthma dosing abstention
6. scenario6_dual_htn_t2dm: Dual HTN + T2DM dual therapy initiation
7. scenario7_elderly_systolic_htn: Elderly patient (age 84) target BP
8. scenario8_pregnancy_new_htn: Pregnant woman (28 weeks) drug choices & contraindications
9. scenario9_htn_microalbuminuria: HTN with newly reported microalbuminuria (ACR 4.2 mg/mmol)
10. scenario10_amlodipine_followup: Amlodipine started last week, BP today 145/92, next step
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from guideline_chatbot.chatbot.orchestrator import ChatbotOrchestrator


def run_demo_scenarios(
    output_dirs: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Execute 10 demo dialogues and save JSON and Markdown transcripts."""
    if output_dirs is None:
        output_dirs = [
            "guideline_chatbot/evaluation/demo_conversations",
            "evaluation/demo_conversations",
        ]

    for d in output_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

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
            "description": "Patient reveals hypertension, then type 2 diabetes, then microalbuminuria (ACR 4.2 mg/mmol).",
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
            "description": "Patient claims normotension in Turn 1, then presents with Grade 2 HTN (168/104 mmHg) in Turn 2, resolved in Turn 3.",
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
        {
            "scenario_id": "scenario6_dual_htn_t2dm",
            "title": "Scenario 6: Comorbid Hypertension and Type 2 Diabetes Dual Therapy Initiation",
            "category": "Normal Guideline Questions",
            "description": "Clinician evaluates whether to initiate dual combination therapy vs monotherapy in concurrent HTN and T2DM.",
            "turns": [
                "Patient is a 54-year-old male with confirmed type 2 diabetes and clinic BP 154/92 mmHg.",
                "Should we start dual combination therapy immediately or begin with monotherapy according to WHO and ICMR guidelines?",
                "What are the specific blood pressure targets for adults with concurrent diabetes?",
            ],
        },
        {
            "scenario_id": "scenario7_elderly_systolic_htn",
            "title": "Scenario 7: Elderly Patient with Isolated Systolic Hypertension",
            "category": "Normal Guideline Questions",
            "description": "84-year-old patient with clinic BP 162/78 mmHg; clinician asks about blood pressure targets and relaxed thresholds.",
            "turns": [
                "I am evaluating an 84-year-old patient with clinic blood pressure 162/78 mmHg and no prior cardiovascular events.",
                "What clinic blood pressure target applies to adults aged 80 and over according to NICE NG136 and ICMR STW?",
                "What first-line drug class is recommended for isolated systolic hypertension in elderly patients?",
            ],
        },
        {
            "scenario_id": "scenario8_pregnancy_new_htn",
            "title": "Scenario 8: Pregnancy with New-Onset Hypertension",
            "category": "Contraindications & Vulnerable Populations",
            "description": "32-year-old pregnant woman at 28 weeks gestation presenting with clinic BP 155/95 mmHg.",
            "turns": [
                "A 32-year-old female patient who is currently pregnant at 28 weeks gestation has a new clinic BP of 155/95 mmHg.",
                "Which antihypertensive medications are strictly contraindicated in pregnancy, and what first-line agents are recommended?",
                "What is the recommended blood pressure target during pregnancy management?",
            ],
        },
        {
            "scenario_id": "scenario9_htn_microalbuminuria",
            "title": "Scenario 9: Hypertension with Newly Reported Microalbuminuria",
            "category": "Target Organ Damage & Renal Protection",
            "description": "Patient with hypertension and newly reported urine ACR 4.2 mg/mmol; clinician asks about ACEi/ARB and CKD classification.",
            "turns": [
                "A 56-year-old hypertensive patient has a newly reported urine ACR of 4.2 mg/mmol and eGFR of 82 mL/min.",
                "Does a single urine ACR of 4.2 mg/mmol constitute a diagnosis of chronic kidney disease?",
                "Should an ACE inhibitor or ARB be initiated for this patient based on the microalbuminuria finding?",
            ],
        },
        {
            "scenario_id": "scenario10_amlodipine_followup",
            "title": "Scenario 10: Multi-Turn Antihypertensive Follow-Up & Treatment Escalation",
            "category": "Follow-Up & Escalation",
            "description": "Patient was started on amlodipine last week; clinic BP today is 145/92 mmHg; clinician asks for next step.",
            "turns": [
                "Patient was started on amlodipine 5 mg last week for Stage 1 hypertension; clinic BP today is 145/92 mmHg.",
                "Since blood pressure remains above target at 145/92 mmHg on monotherapy, what is the recommended next step?",
                "If we add a second agent, which drug class should be combined with amlodipine according to ICMR and WHO protocols?",
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

            # Format retrieved chunks list
            retrieved_summary = []
            for h in turn_res.retrieved_chunks:
                meta = h.get("metadata", {})
                retrieved_summary.append(
                    {
                        "chunk_id": h.get("chunk_id"),
                        "score": round(float(h.get("score", 0.0)), 4),
                        "document_name": meta.get("document_name"),
                        "heading": meta.get("heading"),
                        "page": meta.get("page_start"),
                    }
                )

            turn_dict = {
                "turn_index": t_idx,
                "user_message": user_msg,
                "action_type": turn_res.action_type,
                "is_abstention": turn_res.is_abstention,
                "patient_state_delta": turn_res.state_delta,
                "patient_state_summary": turn_res.patient_state.to_summary_string(),
                "retrieved_chunks": retrieved_summary,
                "disputed_facts_count": len(turn_res.disputed_facts),
                "citations_verified": len(turn_res.citation_validation.validated_citations),
                "citations_total": turn_res.citation_validation.total_citations,
                "response_text": turn_res.response_text,
            }
            dialogue_record["turns"].append(turn_dict)

            # Markdown formatting
            md_lines.append(f"\n### Turn {t_idx}")
            md_lines.append(f"**Clinician/User**: {user_msg}\n")
            md_lines.append(
                f"**Chatbot Action**: `{turn_res.action_type}` | **Abstention**: `{turn_res.is_abstention}`"
            )
            md_lines.append(
                f"**Patient State Summary**: *{turn_res.patient_state.to_summary_string()}*"
            )
            if turn_res.state_delta:
                md_lines.append(f"**Patient State Delta**: `{json.dumps(turn_res.state_delta)}`")
            md_lines.append("\n**Retrieved Guideline Evidence (Top-5)**:")
            for rc in retrieved_summary:
                md_lines.append(
                    f"- `{rc['chunk_id']}` (Score: {rc['score']}): {rc['document_name']} (p. {rc['page']}, §{rc['heading']})"
                )
            md_lines.append(
                f"\n**Response (Sentence-by-Sentence Grounding)**:\n{turn_res.response_text}\n"
            )
            md_lines.append(f"**Citation Verification**: {turn_res.citation_validation.summary()}")
            if turn_res.disputed_facts:
                md_lines.append(f"**Disputed Facts ({len(turn_res.disputed_facts)})**:")
                for df in turn_res.disputed_facts:
                    resolved_str = " (RESOLVED)" if df.is_resolved else " (ACTIVE)"
                    md_lines.append(f"- Turn {df.turn_index}: {df.explanation}{resolved_str}")
            md_lines.append("\n---")

        for d_str in output_dirs:
            p = Path(d_str)
            json_file = p / f"{sid}.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(dialogue_record, f, indent=2)

            md_file = p / f"{sid}.md"
            with open(md_file, "w", encoding="utf-8") as f:
                f.write("\n".join(md_lines))

        scenario_reports.append(dialogue_record)
        print(f"Generated {sid}.json and {sid}.md ({len(sc['turns'])} turns) in {output_dirs}")

    return scenario_reports


if __name__ == "__main__":
    run_demo_scenarios()
