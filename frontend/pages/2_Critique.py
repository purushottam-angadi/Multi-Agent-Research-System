
import streamlit as st
import re

from theme import inject, masthead, nav

st.set_page_config(page_title="Critique", page_icon="◆", layout="wide")

inject()

# Guard
if "result" not in st.session_state:
    st.warning("No research found. Please run the pipeline from the Home page first.")
    st.page_link("Home.py", label="← Go to Home")
    st.stop()

result = st.session_state["result"]
topic  = st.session_state.get("topic", "Research Topic")
feedback = result.get("feedback", "")

# Header
masthead(
    eyebrow="Section 03 · Editorial Review",
    title="Report Critique",
    subtitle=f"Topic: {topic}",
)

# Nav
nav("critique")

st.markdown("---")

# ── Parse the structured feedback ─────────────────────────────────────────────
def _strip_md(s: str) -> str:
    s = re.sub(r"\*\*|\*|__|_", "", s)
    return s

def extract_section(text: str, header: str, next_headers: list) -> str:
    clean_text = _strip_md(text)
    header_pat = re.escape(header).replace(r"\:", r"\s*:?")
    next_pat = "|".join(
        re.escape(_strip_md(h)).replace(r"\:", r"\s*:?") for h in next_headers
    )
    pattern = (
        rf"{header_pat}\s*[\n:]*([\s\S]*?)(?=(?:{next_pat})|\Z)"
        if next_pat
        else rf"{header_pat}\s*[\n:]*([\s\S]*)"
    )
    m = re.search(pattern, clean_text, re.IGNORECASE)
    if m:
        return m.group(1).strip(" \n-")
    return ""

clean_feedback = _strip_md(feedback)

score_match = re.search(r"Score\s*:?\s*(\d+(?:\.\d+)?)\s*/\s*10", clean_feedback, re.IGNORECASE)
score_val   = score_match.group(1) if score_match else "?"

strengths = extract_section(
    feedback, "Strengths:",
    ["Areas to Improve:", "Areas For Improvement:", "One line verdict:"]
)
improvements = (
    extract_section(feedback, "Areas to Improve:", ["One line verdict:"])
    or extract_section(feedback, "Areas For Improvement:", ["One line verdict:"])
)
verdict_match = re.search(r"One line verdict\s*:?\s*\n?\s*(.+)", clean_feedback, re.IGNORECASE)
verdict = verdict_match.group(1).strip() if verdict_match else ""

# ── Score ──────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([1, 4])
with c1:
    st.markdown(
        f'<p class="score-caption">Score</p>'
        f'<div class="score-figure">{score_val}<span>/10</span></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(int(float(score_val) * 10) if score_val != "?" else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sections ──────────────────────────────────────────────────────────────────
parsed_any = False

if strengths:
    parsed_any = True
    st.markdown('<p class="panel-label">Strengths</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(strengths)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

if improvements:
    parsed_any = True
    st.markdown('<p class="panel-label">Areas to improve</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(improvements)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

if verdict:
    parsed_any = True
    st.markdown('<div class="callout">' + verdict + '</div>', unsafe_allow_html=True)

# fallback if parsing failed
if not parsed_any:
    st.markdown('<p class="panel-label">Full critique</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(feedback)
    st.markdown('</div>', unsafe_allow_html=True)

# Download
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="Download critique (.txt)",
    data=feedback,
    file_name=f"critique_{topic[:30].replace(' ','_')}.txt",
    mime="text/plain",
    use_container_width=True,
)