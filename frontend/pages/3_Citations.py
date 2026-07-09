# import streamlit as st
# import re

# st.set_page_config(page_title="Citations", page_icon="📚", layout="wide")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#     .page-header {
#         background: linear-gradient(135deg, #1a0a2e, #3d2060);
#         border-radius: 14px;
#         padding: 32px 28px;
#         margin-bottom: 28px;
#     }
#     .page-header h2 { color: #fff; margin: 0 0 4px 0; font-size: 1.8rem; }
#     .page-header p  { color: #bba; margin: 0; font-size: 0.95rem; }

#     .cite-block {
#         background: #13131f;
#         border: 1px solid #2a2a45;
#         border-radius: 12px;
#         padding: 18px 24px;
#         margin-bottom: 14px;
#         color: #d0d0f0;
#         font-family: 'Courier New', monospace;
#         font-size: 0.88rem;
#     }

#     .cite-style-label {
#         font-size: 0.75rem;
#         font-weight: 700;
#         letter-spacing: 1.5px;
#         text-transform: uppercase;
#         margin-bottom: 6px;
#         color: #8888cc;
#     }

#     /* Tighten markdown rendered inside cite-block */
#     .cite-block div[data-testid="stMarkdownContainer"] {
#         line-height: 1.55;
#     }
#     .cite-block div[data-testid="stMarkdownContainer"] > * {
#         margin-top: 0 !important;
#         margin-bottom: 0.4rem !important;
#     }
#     .cite-block div[data-testid="stMarkdownContainer"] > *:last-child {
#         margin-bottom: 0 !important;
#     }
#     .cite-block ul, .cite-block ol {
#         margin-top: 0.1rem !important;
#         margin-bottom: 0.4rem !important;
#         padding-left: 1.2rem !important;
#     }
#     .cite-block li { margin-bottom: 0.3rem !important; }

#     /* Tables: compact, no huge gaps */
#     .cite-block table {
#         border-collapse: collapse;
#         width: 100%;
#         margin: 0.3rem 0 0.5rem 0 !important;
#         font-size: 0.85rem;
#         font-family: 'Inter', sans-serif;
#     }
#     .cite-block th, .cite-block td {
#         border: 1px solid #2a2a45;
#         padding: 6px 12px !important;
#         text-align: left;
#     }
#     .cite-block th {
#         background: #1c1c2e;
#         color: #fff;
#         font-weight: 600;
#     }
#     .cite-block tr:nth-child(even) td { background: #16161f; }
# </style>
# """, unsafe_allow_html=True)

# # Guard
# if "result" not in st.session_state:
#     st.warning("No research found. Please run the pipeline from the Home page first.")
#     st.page_link("Home.py", label="← Go to Home")
#     st.stop()

# result    = st.session_state["result"]
# topic     = st.session_state.get("topic", "Research Topic")
# citations = result.get("citations", "")

# # Header
# st.markdown(f"""
# <div class="page-header">
#     <h2>Citations</h2>
#     <p>Topic: <strong>{topic}</strong></p>
# </div>
# """, unsafe_allow_html=True)

# # Nav
# col1, col2, col3, col4 = st.columns(4)
# col1.page_link("Home.py",                  label="Home")
# col2.page_link("pages/1_Report.py",        label="← Report")
# col3.page_link("pages/2_Critique.py",      label="← Critique")

# st.markdown("---")

# # ── Parse APA / IEEE ──────────────────────────────────────────────────────────
# apa_match  = re.search(r"APA\s*:\s*([\s\S]*?)(?=IEEE\s*:|$)",  citations, re.IGNORECASE)
# ieee_match = re.search(r"IEEE\s*:\s*([\s\S]*?)(?=APA\s*:|$)",  citations, re.IGNORECASE)

# apa  = apa_match.group(1).strip()  if apa_match  else ""
# ieee = ieee_match.group(1).strip() if ieee_match else ""

# if apa:
#     st.markdown('<div class="cite-style-label">📖 APA Style</div>', unsafe_allow_html=True)
#     st.markdown('<div class="cite-block">', unsafe_allow_html=True)
#     st.markdown(apa)
#     st.markdown('</div>', unsafe_allow_html=True)

# if ieee:
#     st.markdown('<div class="cite-style-label">🔢 IEEE Style</div>', unsafe_allow_html=True)
#     st.markdown('<div class="cite-block">', unsafe_allow_html=True)
#     st.markdown(ieee)
#     st.markdown('</div>', unsafe_allow_html=True)

# if not apa and not ieee:
#     st.markdown('<div class="cite-block">', unsafe_allow_html=True)
#     st.markdown(citations)
#     st.markdown('</div>', unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)
# st.download_button(
#     label="Download Citations (.txt)",
#     data=citations,
#     file_name=f"citations_{topic[:30].replace(' ','_')}.txt",
#     mime="text/plain",
#     use_container_width=True,
# )

import streamlit as st
import re

from theme import inject, masthead, nav

st.set_page_config(page_title="Citations", page_icon="◆", layout="wide")

inject()

# Guard
if "result" not in st.session_state:
    st.warning("No research found. Please run the pipeline from the Home page first.")
    st.page_link("Home.py", label="← Go to Home")
    st.stop()

result    = st.session_state["result"]
topic     = st.session_state.get("topic", "Research Topic")
citations = result.get("citations", "")

# Header
masthead(
    eyebrow="Section 04 · Sourcing",
    title="Citations",
    subtitle=f"Topic: {topic}",
)

# Nav
nav("citations")

st.markdown("---")

# ── Parse APA / IEEE ──────────────────────────────────────────────────────────
apa_match  = re.search(r"APA\s*:\s*([\s\S]*?)(?=IEEE\s*:|$)",  citations, re.IGNORECASE)
ieee_match = re.search(r"IEEE\s*:\s*([\s\S]*?)(?=APA\s*:|$)",  citations, re.IGNORECASE)

apa  = apa_match.group(1).strip()  if apa_match  else ""
ieee = ieee_match.group(1).strip() if ieee_match else ""

if apa:
    st.markdown('<p class="panel-label">APA style</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(apa)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

if ieee:
    st.markdown('<p class="panel-label">IEEE style</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(ieee)
    st.markdown('</div>', unsafe_allow_html=True)

if not apa and not ieee:
    st.markdown('<p class="panel-label">Citations</p>', unsafe_allow_html=True)
    st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
    st.markdown(citations)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="Download citations (.txt)",
    data=citations,
    file_name=f"citations_{topic[:30].replace(' ','_')}.txt",
    mime="text/plain",
    use_container_width=True,
)