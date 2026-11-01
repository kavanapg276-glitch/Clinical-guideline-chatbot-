# ClinCoherence Guideline Chatbot

**Clinical Guideline-Based Decision Support RAG Chatbot** — Part of the capstone project:  
*"Longitudinal Clinical Coherence: A Real-Time, State-Aware Verification Layer for Multi-Turn Clinical LLM Conversations."*

> ⚠️ **Research prototype for evaluation only.** Not for clinical use. Never rely on this system for medical decisions.

## Status

- [x] **Phase 0** — Environment Setup & Dataset Acquisition
- [x] **Phase 1** — Extraction, Cleaning, Recommendation-Aware Chunking (1009 chunks, 850 indexed)
- [x] **Phase 2** — Embeddings, ChromaDB, Hybrid BM25/Dense Retrieval
- [x] **Phase 3** — Patient State, Generator, Multi-Turn Backend, 10 Demo Dialogues
- [x] **Phase 4** — ClinCoherence Verification & Decision Gating (3-Arm Pipeline)
- [ ] **Phase 5** — Full Cohort Evaluation

## Quick-Start: Streamlit Clinical UI

To launch the interactive clinical reference frontend:

```powershell
# 1. Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\activate

# 2. Launch the Streamlit application
streamlit run frontend/app.py
```

Or run directly using the virtual environment python:
```powershell
.\.venv\Scripts\streamlit.exe run frontend/app.py
```

The application opens at `http://localhost:8501` featuring:
- **Chat Consultation**: Multi-turn clinical reasoning with live patient state, gate badges, and collapsed guideline evidence, citation grounding, and conflict expanders.
- **Compare Arms**: Side-by-side evaluation of Arm 1 (Baseline), Arm 2 (Self-Check), and Arm 3 (ClinCoherence) on any clinical query or dilemma preset.
- **Replay & Scenarios**: Turn-by-turn inspector for the 5 scripted clinical demo dialogues and 14 controlled injected test cases.

## Scope

- **Conditions:** Hypertension, Type 2 Diabetes
- **Sources:** MoHFW STG (India), ICMR STW (India), WHO, NICE (UK)

## Prerequisites

- Python ≥ 3.10
- Git

## Setup

```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and configure as needed. See `guideline_chatbot/config/settings.yaml` for full configuration options.

## Project Structure

```
capstone/
  guideline_chatbot/
    config/          # YAML configuration
    data/            # Raw, processed, inventory, reports
    ingestion/       # Download, inventory, extraction, cleaning
    chunking/        # Recommendation-aware chunking
    retrieval/       # Embeddings, vector store, hybrid search
    chatbot/         # Patient state, generation, orchestration
    coherence/       # ClinCoherence verification layer
    integration/     # CLI, Streamlit hooks, adapters
    evaluation/      # Scenarios, metrics, reports
    tests/           # pytest test suite
    docs/            # Documentation
```

## License

See `docs/LICENSING.md` for source document licensing information.

## Disclaimer

This is a research prototype built for academic evaluation. It is **not** validated for clinical use. All recommendations are grounded in retrieved guideline text and carry no clinical authority beyond the source documents themselves.

