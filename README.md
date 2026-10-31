# ClinCoherence Guideline Chatbot

**Clinical Guideline-Based Decision Support RAG Chatbot** — Part of the capstone project:  
*"Longitudinal Clinical Coherence: A Real-Time, State-Aware Verification Layer for Multi-Turn Clinical LLM Conversations."*

> ⚠️ **Research prototype for evaluation only.** Not for clinical use. Never rely on this system for medical decisions.

## Status

- [x] **Phase 0** — Environment Setup & Dataset Acquisition *(in progress)*
- [ ] **Phase 1** — Extraction, Cleaning, Recommendation-Aware Chunking
- [ ] **Phase 2** — Embeddings, ChromaDB, Retrieval
- [ ] **Phase 3** — Patient State, Generation, Multi-Turn Backend
- [ ] **Phase 4** — ClinCoherence Layer
- [ ] **Phase 5** — Evaluation

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
