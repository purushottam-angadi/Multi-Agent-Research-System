import streamlit as st
import re

st.set_page_config(page_title="Critique", page_icon="🧐", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .page-header {
        background: linear-gradient(135deg, #1a0533, #3d1060);
        border-radius: 14px;
        padding: 32px 28px;
        margin-bottom: 28px;
    }
    .page-header h2 { color: #fff; margin: 0 0 4px 0; font-size: 1.8rem; }
    .page-header p  { color: #cca; margin: 0; font-size: 0.95rem; }

    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6c63ff, #48cfad);
        color: white;
        font-size: 2rem;
        font-weight: 700;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        line-height: 80px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(108,99,255,0.4);
    }

    .section-card {
        background: #13131f;
        border: 1px solid #2a2a45;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 14px;
        color: #d0d0f0;
    }
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #7878bb;
        margin-bottom: 6px;
    }

    .verdict-box {
        background: linear-gradient(135deg, #1a1a3e, #0d2b1a);
        border: 1px solid #3a6a5a;
        border-radius: 12px;
        padding: 16px 24px;
        color: #a0ffc0;
        font-style: italic;
        font-size: 1.02rem;
    }

    /* Tighten markdown rendered inside section-card */
    .section-card div[data-testid="stMarkdownContainer"] {
        line-height: 1.45;
    }
    .section-card div[data-testid="stMarkdownContainer"] > * {
        margin-top: 0 !important;
        margin-bottom: 0.45rem !important;
    }
    .section-card div[data-testid="stMarkdownContainer"] > *:last-child {
        margin-bottom: 0 !important;
    }
    .section-card h1, .section-card h2, .section-card h3,
    .section-card h4, .section-card h5, .section-card h6 {
        color: #fff;
        margin-top: 0.7rem !important;
        margin-bottom: 0.35rem !important;
        line-height: 1.3 !important;
    }
    .section-card h1:first-child, .section-card h2:first-child,
    .section-card h3:first-child {
        margin-top: 0 !important;
    }
    .section-card ul, .section-card ol {
        margin-top: 0.15rem !important;
        margin-bottom: 0.5rem !important;
        padding-left: 1.3rem !important;
    }
    .section-card li { margin-bottom: 0.15rem !important; }

    /* Tables: compact, no huge gaps */
    .section-card table {
        border-collapse: collapse;
        width: 100%;
        margin: 0.3rem 0 0.6rem 0 !important;
        font-size: 0.9rem;
    }
    .section-card th, .section-card td {
        border: 1px solid #2a2a45;
        padding: 6px 12px !important;
        text-align: left;
    }
    .section-card th {
        background: #1c1c2e;
        color: #fff;
        font-weight: 600;
    }
    .section-card tr:nth-child(even) td { background: #16161f; }
</style>
""", unsafe_allow_html=True)

# Guard
if "result" not in st.session_state:
    st.warning("No research found. Please run the pipeline from the Home page first.")
    st.page_link("Home.py", label="← Go to Home", icon="🏠")
    st.stop()

result = st.session_state["result"]
topic  = st.session_state.get("topic", "Research Topic")
feedback = result.get("feedback", "")

# Header
st.markdown(f"""
<div class="page-header">
    <h2>🧐 Report Critique</h2>
    <p>Topic: <strong>{topic}</strong></p>
</div>
""", unsafe_allow_html=True)

# Nav
col1, col2, col3, col4 = st.columns(4)
col1.page_link("Home.py",                  label="🏠 Home")
col2.page_link("pages/1_Report.py",        label="← 📄 Report")
col4.page_link("pages/3_Citations.py",     label="📚 Citations →")

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
c1, c2 = st.columns([1, 5])
with c1:
    st.markdown(f'<div class="score-badge">{score_val}</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f"### Score: **{score_val} / 10**")
    st.progress(int(float(score_val) * 10) if score_val != "?" else 0)

# ── Sections ──────────────────────────────────────────────────────────────────
parsed_any = False

if strengths:
    parsed_any = True
    st.markdown('<div class="section-title">💪 Strengths</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(strengths)
    st.markdown('</div>', unsafe_allow_html=True)

if improvements:
    parsed_any = True
    st.markdown('<div class="section-title">🔧 Areas to Improve</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(improvements)
    st.markdown('</div>', unsafe_allow_html=True)

if verdict:
    parsed_any = True
    st.markdown('<div class="verdict-box">💬 ' + verdict + '</div>', unsafe_allow_html=True)

# fallback if parsing failed
if not parsed_any:
    st.markdown("**Full Critique**")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(feedback)
    st.markdown('</div>', unsafe_allow_html=True)

# Download
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="Download Critique (.txt)",
    data=feedback,
    file_name=f"critique_{topic[:30].replace(' ','_')}.txt",
    mime="text/plain",
    use_container_width=True,
)