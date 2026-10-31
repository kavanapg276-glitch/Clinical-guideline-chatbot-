# Architecture

*Full architecture diagram and description. To be written in Phase 3+.*

## Pipeline Overview

```
User turn → State extractor → Case state → Retrieval → LLM draft → Coherence checker → Decision gate
```

Decision gate outcomes: `Pass` / `Clarify` / `Warn` / `Refuse + explain`

## Detailed Design

*(To be documented as components are built)*
