

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