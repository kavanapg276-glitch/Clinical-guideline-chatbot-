# Licensing & Reuse Terms

All source documents are downloaded and utilized strictly for **academic research purposes only** as part of the capstone project evaluation ("Longitudinal Clinical Coherence: A Real-Time, State-Aware Verification Layer for Multi-Turn Clinical LLM Conversations").

In accordance with Standing Rule 4, original files are preserved untouched with SHA-256 hashes, and raw data (`guideline_chatbot/data/raw/`) is excluded from Git tracking via `.gitignore`.

| Source | Issuing Organisation | Licence / Reuse Terms | Source Landing URL | Date Accessed | Notes |
|---|---|---|---|---|---|
| **WHO Guidelines** | World Health Organization | Creative Commons Attribution-NonCommercial-ShareAlike 3.0 IGO (**CC BY-NC-SA 3.0 IGO**) | https://www.who.int/publications | 2026-10-31 | Freely accessible for non-commercial educational/research use with appropriate citation. |
| **ICMR STWs** | Indian Council of Medical Research (ICMR) / Department of Health Research (DHR), Ministry of Health and Family Welfare, Government of India | Official Government Publication / Clinical Workflows for Public Healthcare | https://www.icmr.gov.in/standard-treatment-workflows-stws | 2026-10-31 | Published for clinical education and standardisation across healthcare tiers in India. Not restricted for non-commercial academic research. |
| **NICE Guidance** | National Institute for Health and Care Excellence (NICE), United Kingdom | **Open Government Licence v3.0 (OGL)** / Crown Copyright | https://www.nice.org.uk/guidance | 2026-10-31 | Content is available under the terms of the UK Open Government Licence v3.0, permitting non-commercial research, reproduction, and adaptation with attribution. |
| **MoHFW STGs** | Ministry of Health and Family Welfare, Government of India | Official Government Publication under the Clinical Establishments Act | https://clinicalestablishments.mohfw.gov.in/en/standard-treatment-guidelines | 2026-10-31 | Public standard treatment guidelines formulated by national expert committees for clinical establishments in India. |

## Redundancy & Preservation Policy

1. **Original Files:** Stored untouched under `guideline_chatbot/data/raw/{mohfw_stg,icmr_stw,who,nice}/`.
2. **Integrity:** SHA-256 cryptographic checksums are recorded in `data/inventory/source_inventory.csv` and `data/inventory/source_inventory.json`.
3. **No Redistribution of Raw Binaries:** Raw PDFs are ignored in `.gitignore`. The acquisition scripts (`acquire.py` and `inventory.py`) permit fully automated, reproducible re-downloading from verified official URLs.
