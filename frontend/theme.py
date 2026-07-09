"""
Shared visual design system for the research pipeline UI.

Every page calls `inject()` once, then uses the small helper functions
below to render the masthead, navigation row, document panels and
status stamps consistently. Keeping this in one place means a palette
or type change only has to happen here.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% 0%, #0c1220 0%, var(--ink-950) 45%) fixed;
}
section[data-testid="stSidebar"] {
    background: var(--ink-900);
    border-right: 1px solid var(--hairline);
}

:root {
    --ink-950: #070a10;
    --ink-900: #0e131c;
    --ink-800: #141b26;
    --hairline: #232c3a;
    --text-primary: #e8ecf4;
    --text-secondary: #7c8ba0;
    --accent: #4a86c4;
    --accent-soft: #16253a;
    --ok: #5a9e93;
    --warn: #c99a52;
    --err: #b6635a;
}

/* ---------- Masthead ---------- */
.masthead {
    background: var(--ink-900);
    border: 1px solid var(--hairline);
    border-left: 3px solid var(--accent);
    border-radius: 4px;
    padding: 30px 34px;
    margin-bottom: 22px;
}
.masthead .eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 8px 0;
}
.masthead h2 {
    font-family: 'Source Serif 4', serif;
    color: var(--text-primary);
    font-size: 1.85rem;
    font-weight: 700;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.masthead p {
    color: var(--text-secondary);
    margin: 0;
    font-size: 0.92rem;
}

/* ---------- Document panel (report / critique / citations / fact-check body) ---------- */
.doc-panel {
    background: var(--ink-900);
    border: 1px solid var(--hairline);
    border-radius: 6px;
    padding: 28px 34px;
    color: var(--text-primary);
}
.panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin: 0 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--hairline);
}

.doc-panel div[data-testid="stMarkdownContainer"] { line-height: 1.5; }
.doc-panel div[data-testid="stMarkdownContainer"] > * { margin-top: 0 !important; margin-bottom: 0.55rem !important; }
.doc-panel div[data-testid="stMarkdownContainer"] > *:last-child { margin-bottom: 0 !important; }
.doc-panel h1, .doc-panel h2, .doc-panel h3, .doc-panel h4 {
    font-family: 'Source Serif 4', serif;
    color: var(--text-primary);
    margin-top: 1.1rem !important;
    margin-bottom: 0.4rem !important;
    line-height: 1.3 !important;
    font-weight: 700;
}
.doc-panel h1:first-child, .doc-panel h2:first-child, .doc-panel h3:first-child { margin-top: 0 !important; }
.doc-panel ul, .doc-panel ol { margin-top: 0.2rem !important; margin-bottom: 0.6rem !important; padding-left: 1.35rem !important; }
.doc-panel li { margin-bottom: 0.22rem !important; }
.doc-panel table { border-collapse: collapse; width: 100%; margin: 0.4rem 0 0.8rem 0 !important; font-size: 0.9rem; }
.doc-panel th, .doc-panel td { border: 1px solid var(--hairline); padding: 7px 13px !important; text-align: left; }
.doc-panel th { background: var(--ink-800); color: var(--text-primary); font-weight: 600; }
.doc-panel tr:nth-child(even) td { background: var(--ink-800); }

/* ---------- Status stamp ---------- */
.stamp {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: 1px solid currentColor;
    border-radius: 3px;
    padding: 6px 16px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.stamp-ok { color: var(--ok); }
.stamp-warn { color: var(--warn); }
.stamp-err { color: var(--err); }
.stamp-neutral { color: var(--accent); }

/* ---------- Score block ---------- */
.score-block { display: flex; align-items: center; gap: 22px; margin-bottom: 22px; }
.score-figure {
    font-family: 'Source Serif 4', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--text-primary);
    border: 1px solid var(--hairline);
    border-radius: 6px;
    padding: 10px 22px;
    line-height: 1;
}
.score-figure span { font-size: 1.1rem; color: var(--text-secondary); font-weight: 500; }
.score-caption { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 6px; }

/* ---------- Verdict / summary callout ---------- */
.callout {
    background: var(--ink-800);
    border: 1px solid var(--hairline);
    border-left: 3px solid var(--accent);
    border-radius: 4px;
    padding: 16px 22px;
    color: var(--text-primary);
    font-size: 0.95rem;
}

/* ---------- Streamlit widget restraint ---------- */
div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button {
    border-radius: 4px;
    border: 1px solid var(--hairline);
    background: var(--ink-800);
    color: var(--text-primary);
    font-weight: 500;
    font-size: 0.88rem;
    padding: 10px 18px;
    transition: border-color 0.15s ease;
}
div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {
    border-color: var(--accent);
    color: var(--accent);
}
div[data-testid="stProgress"] div[role="progressbar"] > div { background: var(--accent) !important; }
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def masthead(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="masthead">
            <p class="eyebrow">{eyebrow}</p>
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nav(current: str) -> None:
    """Render the cross-page navigation row. `current` is excluded/dimmed implicitly
    by simply not being clickable elsewhere — Streamlit page_link handles state."""
    items = [
        ("Home.py", "Home"),
        ("pages/1_Report.py", "Report"),
        ("pages/4_FactCheck.py", "Fact Check"),
        ("pages/2_Critique.py", "Critique"),
        ("pages/3_Citations.py", "Citations"),
    ]
    cols = st.columns(len(items))
    for col, (path, label) in zip(cols, items):
        with col:
            st.page_link(path, label=label)


def stamp(text: str, kind: str = "neutral") -> str:
    return f'<span class="stamp stamp-{kind}">{text}</span>'