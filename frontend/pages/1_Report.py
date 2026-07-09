# import streamlit as st

# st.set_page_config(page_title="Research Report", page_icon="📄", layout="wide")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#     .page-header {
#         background: linear-gradient(135deg, #0f0c29, #302b63);
#         border-radius: 14px;
#         padding: 32px 28px;
#         margin-bottom: 28px;
#     }
#     .page-header h2 { color: #fff; margin: 0 0 4px 0; font-size: 1.8rem; }
#     .page-header p  { color: #aaa; margin: 0; font-size: 0.95rem; }

#     .nav-bar {
#         display: flex;
#         gap: 10px;
#         margin-bottom: 20px;
#         flex-wrap: wrap;
#     }

#     /* ── Report body container ───────────────────────────────────────── */
#     .report-box {
#         background: #13131f;
#         border: 1px solid #2a2a45;
#         border-radius: 12px;
#         padding: 28px 36px;
#         color: #d8d8f0;
#         font-size: 0.97rem;
#     }

#     /* Tighten up all markdown elements rendered inside the report box */
#     .report-box div[data-testid="stMarkdownContainer"] {
#         line-height: 1.45;
#     }
#     .report-box div[data-testid="stMarkdownContainer"] > * {
#         margin-top: 0 !important;
#         margin-bottom: 0.5rem !important;
#     }
#     .report-box h1, .report-box h2, .report-box h3,
#     .report-box h4, .report-box h5, .report-box h6 {
#         color: #fff;
#         margin-top: 1rem !important;
#         margin-bottom: 0.4rem !important;
#         padding: 0 !important;
#         line-height: 1.3 !important;
#     }
#     .report-box h1:first-child, .report-box h2:first-child,
#     .report-box h3:first-child {
#         margin-top: 0 !important;
#     }
#     .report-box p {
#         margin-bottom: 0.6rem !important;
#     }
#     .report-box ul, .report-box ol {
#         margin-top: 0.2rem !important;
#         margin-bottom: 0.6rem !important;
#         padding-left: 1.4rem !important;
#     }
#     .report-box li {
#         margin-bottom: 0.2rem !important;
#     }

#     /* Tables: kill the huge gap above/below and make them compact */
#     .report-box div[data-testid="stMarkdownContainer"] table {
#         border-collapse: collapse;
#         width: 100%;
#         margin: 0.4rem 0 0.8rem 0 !important;
#         font-size: 0.92rem;
#     }
#     .report-box th, .report-box td {
#         border: 1px solid #2a2a45;
#         padding: 6px 12px !important;
#         text-align: left;
#     }
#     .report-box th {
#         background: #1c1c2e;
#         color: #fff;
#         font-weight: 600;
#     }
#     .report-box tr:nth-child(even) td {
#         background: #16161f;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Guard
# if "result" not in st.session_state:
#     st.warning("No research found. Please run the pipeline from the Home page first.")
#     st.page_link("Home.py", label="← Go to Home")
#     st.stop()

# result = st.session_state["result"]
# topic  = st.session_state.get("topic", "Research Topic")

# # Header
# st.markdown(f"""
# <div class="page-header">
#     <h2>📄 Research Report</h2>
#     <p>Topic: <strong>{topic}</strong></p>
# </div>
# """, unsafe_allow_html=True)

# # Nav
# col1, col2, col3 = st.columns(3)
# col1.page_link("Home.py",             label="Home")
# col2.page_link("pages/2_Critique.py", label="Critique →")
# col3.page_link("pages/3_Citations.py",label="Citations →")

# st.markdown("---")

# # Content — render as real markdown (not raw HTML) so headers/tables parse correctly
# report = result.get("report", "No report available.")

# st.markdown('<div class="report-box">', unsafe_allow_html=True)
# st.markdown(report)
# st.markdown('</div>', unsafe_allow_html=True)

# # Download
# st.markdown("<br>", unsafe_allow_html=True)
# st.download_button(
#     label="Download Report (.txt)",
#     data=report,
#     file_name=f"report_{topic[:30].replace(' ','_')}.txt",
#     mime="text/plain",
#     use_container_width=True,
# )

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