
import streamlit as st

from theme import inject, masthead, nav

st.set_page_config(page_title="Research Report", page_icon="◆", layout="wide")

inject()

# Guard
if "result" not in st.session_state:
    st.warning("No research found. Please run the pipeline from the Home page first.")
    st.page_link("Home.py", label="← Go to Home")
    st.stop()

result = st.session_state["result"]
topic  = st.session_state.get("topic", "Research Topic")

# Header
masthead(
    eyebrow="Section 01 · Draft",
    title="Research Report",
    subtitle=f"Topic: {topic}",
)

# Nav
nav("report")

st.markdown("---")

# Content — render as real markdown (not raw HTML) so headers/tables parse correctly
report = result.get("report", "No report available.")

st.markdown('<p class="panel-label">Full report</p>', unsafe_allow_html=True)
st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
st.markdown(report)
st.markdown('</div>', unsafe_allow_html=True)

# Download
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="Download report (.txt)",
    data=report,
    file_name=f"report_{topic[:30].replace(' ','_')}.txt",
    mime="text/plain",
    use_container_width=True,
)