"""Theme and clinical styling definitions for the ClinCoherence Streamlit UI.

Provides:
- Design tokens: restrained clinical palette (off-white, near-black, deep teal accent)
- Gate badge styles: muted functional status pills (PASS, WARN, CLARIFY, REFUSE)
- Clinical note typography: 16px base font, tabular numerals for vitals, small-caps section labels
- Dark mode compatibility rules
"""

from __future__ import annotations

import streamlit as st

# Muted, accessible gate colors
GATE_COLORS = {
    "pass": {
        "text": "#1b5e20",
        "bg": "#edf7ed",
        "border": "#c8e6c9",
        "dark_text": "#81c784",
        "dark_bg": "#1e3820",
        "dark_border": "#2e5b32",
    },
    "warn": {
        "text": "#b25e00",
        "bg": "#fff8e1",
        "border": "#ffe082",
        "dark_text": "#ffb74d",
        "dark_bg": "#3e2710",
        "dark_border": "#664319",
    },
    "clarify": {
        "text": "#026aa7",
        "bg": "#e1f5fe",
        "border": "#b3e5fc",
        "dark_text": "#4fc3f7",
        "dark_bg": "#0c2836",
        "dark_border": "#134b66",
    },
    "refuse": {
        "text": "#c62828",
        "bg": "#ffebee",
        "border": "#ffcdd2",
        "dark_text": "#e57373",
        "dark_bg": "#3c181a",
        "dark_border": "#5c2427",
    },
}

CLINICAL_CSS = """
<style>
/* Global typography and sizing */
html, body, [class*="css"] {
    font-size: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1a1f2c;
    -webkit-font-smoothing: antialiased;
}

/* Tabular numbers for clinical measurements */
.tabular-nums, .stMetric, table, code {
    font-variant-numeric: tabular-nums;
}

/* Subtle flat borders, clean clinical styling */
div[data-testid="stExpander"],
div[data-testid="stExpander"] * {
    box-sizing: border-box;
}

div[data-testid="stExpander"] {
    border: 1px solid #cbd5e1 !important;
    border-radius: 6px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
    background-color: #ffffff !important;
    background: #ffffff !important;
    margin-bottom: 0.75rem !important;
    overflow: hidden !important;
}

/* Ensure all details containers and nested Streamlit wrapper blocks are crisp white */
div[data-testid="stExpander"] details,
div[data-testid="stExpander"] details > div,
div[data-testid="stExpander"] [data-testid="stExpanderDetails"],
div[data-testid="stExpanderDetails"],
div[data-testid="stExpander"] [data-testid="stVerticalBlock"],
div[data-testid="stExpander"] [data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stExpander"] div[role="region"],
div[data-testid="stExpander"] .stMarkdown,
div[data-testid="stExpander"] .stMarkdown > div {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #0f172a !important;
}

div[data-testid="stExpander"] details summary {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #0f172a !important;
    background-color: #f8fafc !important;
    background: #f8fafc !important;
    border-bottom: 1px solid #e2e8f0 !important;
    padding: 0.6rem 0.85rem !important;
}

div[data-testid="stExpander"] details summary:hover {
    color: #006666 !important;
    background-color: #f1f5f9 !important;
}

div[data-testid="stExpander"] details summary p,
div[data-testid="stExpander"] details summary span {
    color: #0f172a !important;
    font-weight: 600 !important;
}

div[data-testid="stExpander"] details:not([open]) summary {
    border-bottom: none !important;
}

/* Force all text elements inside expander to be crystal clear dark readable text */
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] li,
div[data-testid="stExpander"] div,
div[data-testid="stExpander"] label,
div[data-testid="stExpanderDetails"] p,
div[data-testid="stExpanderDetails"] span,
div[data-testid="stExpanderDetails"] li,
div[data-testid="stExpanderDetails"] div,
div[data-testid="stExpanderDetails"] label {
    color: #0f172a !important;
}

div[data-testid="stExpander"] strong,
div[data-testid="stExpanderDetails"] strong {
    color: #0f172a !important;
    font-weight: 600 !important;
}

div[data-testid="stExpander"] code,
div[data-testid="stExpanderDetails"] code {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    padding: 2px 6px !important;
    border-radius: 4px !important;
    font-size: 0.85em !important;
    font-weight: 600 !important;
}

/* Clinical chat bubble styling */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border-bottom: 1px solid #edf2f7;
    padding: 1rem 0;
}

/* Small flat gate badge pill */
.gate-pill {
    display: inline-block;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-radius: 4px;
    border-width: 1px;
    border-style: solid;
    line-height: 1.3;
    margin-bottom: 4px;
}

.gate-pill-pass {
    color: #1b5e20 !important;
    background-color: #edf7ed !important;
    border-color: #c8e6c9 !important;
}

.gate-pill-warn {
    color: #b25e00 !important;
    background-color: #fff8e1 !important;
    border-color: #ffe082 !important;
}

.gate-pill-clarify {
    color: #026aa7 !important;
    background-color: #e1f5fe !important;
    border-color: #b3e5fc !important;
}

.gate-pill-refuse {
    color: #c62828 !important;
    background-color: #ffebee !important;
    border-color: #ffcdd2 !important;
}

/* Gate explanation notice */
.gate-notice {
    font-size: 0.85rem;
    color: #334155;
    margin-top: 2px;
    margin-bottom: 8px;
    line-height: 1.4;
}

.gate-notice-warn {
    color: #9a5300;
    font-weight: 500;
}

.gate-notice-refuse {
    color: #b71c1c;
    font-weight: 600;
}

/* Patient state sidebar card */
.patient-card {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px;
    background-color: #ffffff;
    margin-bottom: 12px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.patient-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #475569;
    margin-bottom: 2px;
}

.patient-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 8px;
    font-variant-numeric: tabular-nums;
}

/* Disputed fact highlight */
.disputed-fact-pill {
    background-color: #fff8e1;
    border: 1px solid #ffe082;
    color: #9a5300;
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 0.82rem;
    margin-top: 4px;
    margin-bottom: 4px;
}

/* Small clinical section header */
.clinical-section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #006666;
    margin-top: 10px;
    margin-bottom: 2px;
}

/* Footnote evidence item */
.evidence-item {
    font-size: 0.82rem;
    color: #334155;
    padding: 4px 0;
    border-bottom: 1px dashed #e2e8f0;
}

/* LLM mode banner in sidebar */
.llm-mode-banner {
    font-size: 0.78rem;
    padding: 4px 8px;
    border-radius: 3px;
    border: 1px solid #cbd5e1;
    background-color: #f8fafc;
    color: #475569;
    margin-bottom: 12px;
}

/* Legal notice */
.legal-notice {
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.3;
    margin-top: 16px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
}
</style>
"""


def apply_theme() -> None:
    """Inject clinical stylesheet into Streamlit page."""
    st.markdown(CLINICAL_CSS, unsafe_allow_html=True)


def render_gate_badge(decision: str, reason: str = "") -> str:
    """Generate HTML snippet for a small flat gate pill with optional reason."""
    dec_lower = decision.lower()
    if dec_lower not in ("pass", "warn", "clarify", "refuse"):
        dec_lower = "pass"

    pill_html = f'<span class="gate-pill gate-pill-{dec_lower}">{dec_lower.upper()}</span>'

    if reason and dec_lower in ("warn", "refuse"):
        notice_class = f"gate-notice gate-notice-{dec_lower}"
        return f'{pill_html}<div class="{notice_class}">{reason}</div>'
    return pill_html
