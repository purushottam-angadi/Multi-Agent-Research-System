# # import streamlit as st
# # import requests
# # import time


# # import os
# # API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

# # st.set_page_config(
# #     page_title="AI Research Pipeline",
# #     page_icon="🔬",
# #     layout="centered",
# # )

# # # ── Styles ──────────────────────────────────────────────────────────────────
# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

# #     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

# #     .hero {
# #         background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
# #         border-radius: 16px;
# #         padding: 48px 32px;
# #         text-align: center;
# #         margin-bottom: 32px;
# #     }
# #     .hero h1 { color: #fff; font-size: 2.4rem; margin-bottom: 8px; }
# #     .hero p  { color: #bbb; font-size: 1.05rem; }

# #     .step-row {
# #         display: flex;
# #         justify-content: center;
# #         gap: 12px;
# #         flex-wrap: wrap;
# #         margin-bottom: 32px;
# #     }
# #     .step-pill {
# #         background: #1e1e2e;
# #         border: 1px solid #333;
# #         border-radius: 24px;
# #         padding: 6px 16px;
# #         color: #a0a0c0;
# #         font-size: 0.82rem;
# #     }

# #     div[data-testid="stTextInput"] input {
# #         border-radius: 10px !important;
# #         font-size: 1rem !important;
# #         padding: 12px 16px !important;
# #     }

# #     div[data-testid="stButton"] button {
# #         width: 100%;
# #         padding: 14px;
# #         border-radius: 10px;
# #         font-size: 1rem;
# #         font-weight: 600;
# #         background: linear-gradient(135deg, #6c63ff, #48cfad);
# #         color: white;
# #         border: none;
# #         cursor: pointer;
# #         transition: opacity 0.2s;
# #     }
# #     div[data-testid="stButton"] button:hover { opacity: 0.9; }

# #     .status-box {
# #         border-radius: 10px;
# #         padding: 16px 20px;
# #         margin-top: 16px;
# #         font-size: 0.95rem;
# #     }
# #     .status-running { background: #1a2a1a; border: 1px solid #2d5a2d; color: #6fcf6f; }
# #     .status-done    { background: #1a1a2e; border: 1px solid #4a4a8a; color: #a0a0ff; }
# #     .status-error   { background: #2a1a1a; border: 1px solid #8a2d2d; color: #ff8080; }
# # </style>
# # """, unsafe_allow_html=True)

# # # ── Hero ─────────────────────────────────────────────────────────────────────
# # st.markdown("""
# # <div class="hero">
# #     <h1>🔬 AI Research Pipeline</h1>
# #     <p>Multi-agent research powered by LangGraph &amp; Mistral AI</p>
# # </div>
# # """, unsafe_allow_html=True)

# # # ── Pipeline steps ────────────────────────────────────────────────────────────
# # st.markdown("""
# # <div class="step-row">
# #   <span class="step-pill">🔍 Web Search</span>
# #   <span class="step-pill">🌐 Scrape</span>
# #   <span class="step-pill">✍️ Write Report</span>
# #   <span class="step-pill">🧐 Critique</span>
# #   <span class="step-pill">📚 Citations</span>
# # </div>
# # """, unsafe_allow_html=True)

# # # ── Input ─────────────────────────────────────────────────────────────────────
# # topic = st.text_input(
# #     "",
# #     placeholder="e.g.  Impact of AI on healthcare in 2025",
# #     label_visibility="collapsed",
# # )

# # if st.button("🚀  Run Research Pipeline"):
# #     if not topic.strip():
# #         st.warning("Please enter a research topic first.")
# #     else:
# #         with st.spinner("Starting pipeline…"):
# #             try:
# #                 resp = requests.post(f"{API_BASE}/research", json={"topic": topic.strip()}, timeout=10)
# #                 resp.raise_for_status()
# #                 data = resp.json()
# #                 job_id = data["job_id"]
# #                 st.session_state["job_id"] = job_id
# #                 st.session_state["topic"] = topic.strip()
# #                 st.session_state.pop("result", None)   # clear old result
# #             except Exception as e:
# #                 st.error(f"Could not reach the API: {e}")
# #                 st.stop()

# # # ── Polling ───────────────────────────────────────────────────────────────────
# # if "job_id" in st.session_state and "result" not in st.session_state:
# #     job_id = st.session_state["job_id"]
# #     status_placeholder = st.empty()
# #     progress_bar = st.progress(0)

# #     step_labels = [
# #         "🔍 Searching the web…",
# #         "🌐 Scraping URLs…",
# #         "✍️ Writing report…",
# #         "🧐 Critiquing report…",
# #         "📚 Formatting citations…",
# #     ]
# #     step_index = 0
# #     poll_count = 0

# #     while True:
# #         try:
# #             r = requests.get(f"{API_BASE}/research/{job_id}", timeout=10)
# #             r.raise_for_status()
# #             job = r.json()
# #         except Exception as e:
# #             status_placeholder.markdown(
# #                 f'<div class="status-box status-error">❌ Polling error: {e}</div>',
# #                 unsafe_allow_html=True,
# #             )
# #             break

# #         if job["status"] == "completed":
# #             progress_bar.progress(100)
# #             st.session_state["result"] = job
# #             status_placeholder.markdown(
# #                 '<div class="status-box status-done">✅ Research complete! Navigate to the pages on the left.</div>',
# #                 unsafe_allow_html=True,
# #             )
# #             break

# #         if job["status"] == "failed":
# #             status_placeholder.markdown(
# #                 f'<div class="status-box status-error">❌ Pipeline failed: {job.get("error")}</div>',
# #                 unsafe_allow_html=True,
# #             )
# #             break

# #         # Cycle through step labels while running
# #         label = step_labels[step_index % len(step_labels)]
# #         progress_bar.progress(min(5 + step_index * 15, 90))
# #         status_placeholder.markdown(
# #             f'<div class="status-box status-running">{label}</div>',
# #             unsafe_allow_html=True,
# #         )

# #         poll_count += 1
# #         if poll_count % 3 == 0:
# #             step_index += 1

# #         time.sleep(4)

# # # ── Show nav hint once done ───────────────────────────────────────────────────
# # if "result" in st.session_state:
# #     st.markdown("---")
# #     st.markdown("### 📂 Your results are ready")
# #     col1, col2, col3 = st.columns(3)
# #     col1.page_link("pages/1_Report.py",   label="Report",   icon="📄")
# #     col2.page_link("pages/2_Critique.py", label="Critique", icon="🧐")
# #     col3.page_link("pages/3_Citations.py",label="Citations",icon="📚")

# import streamlit as st
# import requests
# import time

# import os
# API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

# st.set_page_config(
#     page_title="AI Research Pipeline",
#     page_icon="🔬",
#     layout="centered",
# )

# # ── Styles ──────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#     .hero {
#         background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
#         border-radius: 16px;
#         padding: 48px 32px;
#         text-align: center;
#         margin-bottom: 32px;
#     }
#     .hero h1 { color: #fff; font-size: 2.4rem; margin-bottom: 8px; }
#     .hero p  { color: #bbb; font-size: 1.05rem; }

#     .step-row {
#         display: flex;
#         justify-content: center;
#         gap: 12px;
#         flex-wrap: wrap;
#         margin-bottom: 32px;
#     }
#     .step-pill {
#         background: #1e1e2e;
#         border: 1px solid #333;
#         border-radius: 24px;
#         padding: 6px 16px;
#         color: #a0a0c0;
#         font-size: 0.82rem;
#     }

#     div[data-testid="stTextInput"] input {
#         border-radius: 10px !important;
#         font-size: 1rem !important;
#         padding: 12px 16px !important;
#     }

#     div[data-testid="stButton"] button {
#         width: 100%;
#         padding: 14px;
#         border-radius: 10px;
#         font-size: 1rem;
#         font-weight: 600;
#         background: linear-gradient(135deg, #6c63ff, #48cfad);
#         color: white;
#         border: none;
#         cursor: pointer;
#         transition: opacity 0.2s;
#     }
#     div[data-testid="stButton"] button:hover { opacity: 0.9; }

#     .status-box {
#         border-radius: 10px;
#         padding: 16px 20px;
#         margin-top: 16px;
#         font-size: 0.95rem;
#     }
#     .status-running  { background: #1a2a1a; border: 1px solid #2d5a2d; color: #6fcf6f; }
#     .status-done     { background: #1a1a2e; border: 1px solid #4a4a8a; color: #a0a0ff; }
#     .status-error    { background: #2a1a1a; border: 1px solid #8a2d2d; color: #ff8080; }
#     .status-review   { background: #2a2410; border: 1px solid #8a7a2d; color: #ffd580; }
# </style>
# """, unsafe_allow_html=True)

# # ── Hero ─────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <h1>🔬 AI Research Pipeline</h1>
#     <p>Multi-agent research powered by LangGraph &amp; Mistral AI</p>
# </div>
# """, unsafe_allow_html=True)

# # ── Pipeline steps ────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="step-row">
#   <span class="step-pill">🔍 Web Search</span>
#   <span class="step-pill">🌐 Scrape</span>
#   <span class="step-pill">✍️ Write Report</span>
#   <span class="step-pill">🧐 Critique</span>
#   <span class="step-pill">🧑 Human Review</span>
#   <span class="step-pill">📚 Citations</span>
# </div>
# """, unsafe_allow_html=True)

# # ── Input ─────────────────────────────────────────────────────────────────────
# topic = st.text_input(
#     "",
#     placeholder="e.g.  Impact of AI on healthcare in 2025",
#     label_visibility="collapsed",
# )

# if st.button("🚀  Run Research Pipeline"):
#     if not topic.strip():
#         st.warning("Please enter a research topic first.")
#     else:
#         with st.spinner("Starting pipeline…"):
#             try:
#                 resp = requests.post(f"{API_BASE}/research", json={"topic": topic.strip()}, timeout=10)
#                 resp.raise_for_status()
#                 data = resp.json()
#                 job_id = data["job_id"]
#                 st.session_state["job_id"] = job_id
#                 st.session_state["topic"] = topic.strip()
#                 st.session_state.pop("result", None)
#                 st.session_state.pop("review_data", None)
#                 st.session_state.pop("resumed", None)
#             except Exception as e:
#                 st.error(f"Could not reach the API: {e}")
#                 st.stop()

# # ── Polling (initial run, up to human review) ─────────────────────────────────
# if "job_id" in st.session_state and "result" not in st.session_state and "review_data" not in st.session_state and not st.session_state.get("resumed"):
#     job_id = st.session_state["job_id"]
#     status_placeholder = st.empty()
#     progress_bar = st.progress(0)

#     step_labels = [
#         "🔍 Searching the web…",
#         "🌐 Scraping URLs…",
#         "✍️ Writing report…",
#         "🧐 Critiquing report…",
#     ]
#     step_index = 0
#     poll_count = 0

#     while True:
#         try:
#             r = requests.get(f"{API_BASE}/research/{job_id}", timeout=10)
#             r.raise_for_status()
#             job = r.json()
#         except Exception as e:
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Polling error: {e}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "completed":
#             progress_bar.progress(100)
#             st.session_state["result"] = job
#             status_placeholder.markdown(
#                 '<div class="status-box status-done">✅ Research complete! Navigate to the pages on the left.</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "failed":
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Pipeline failed: {job.get("error")}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "awaiting_review":
#             progress_bar.progress(90)
#             status_placeholder.markdown(
#                 '<div class="status-box status-review">🧑 Draft ready — your review is needed before citations are generated.</div>',
#                 unsafe_allow_html=True,
#             )
#             st.session_state["review_data"] = job
#             st.rerun()

#         label = step_labels[step_index % len(step_labels)]
#         progress_bar.progress(min(5 + step_index * 15, 85))
#         status_placeholder.markdown(
#             f'<div class="status-box status-running">{label}</div>',
#             unsafe_allow_html=True,
#         )

#         poll_count += 1
#         if poll_count % 3 == 0:
#             step_index += 1

#         time.sleep(4)

# # ── Human review step ─────────────────────────────────────────────────────────
# if "review_data" in st.session_state:
#     job = st.session_state["review_data"]
#     job_id = job["job_id"]

#     st.markdown("---")
#     st.markdown("### 🧑 Human Review Required")
#     st.caption("The critic has reviewed the draft. Approve it as-is, edit it, or reject and stop here.")

#     st.markdown("**Critic feedback**")
#     st.info(job.get("feedback", "(no feedback available)"))

#     st.markdown("**Draft report**")
#     edited_report = st.text_area(
#         "Edit the report below if needed, then choose an action.",
#         value=job.get("report", ""),
#         height=350,
#         key="report_editor",
#     )

#     col1, col2, col3 = st.columns(3)

#     def resume_job(action: str, new_report: str | None = None):
#         payload = {"action": action}
#         if new_report is not None:
#             payload["new_report"] = new_report
#         try:
#             resp = requests.post(f"{API_BASE}/research/{job_id}/resume", json=payload, timeout=10)
#             resp.raise_for_status()
#             st.session_state.pop("review_data", None)
#             st.session_state["resumed"] = True
#             st.rerun()
#         except Exception as e:
#             st.error(f"Could not resume the pipeline: {e}")

#     if col1.button("✅ Approve", use_container_width=True):
#         resume_job("approve")

#     if col2.button("✏️ Approve edited version", use_container_width=True):
#         resume_job("edit", new_report=edited_report)

#     if col3.button("🛑 Reject", use_container_width=True):
#         resume_job("reject")

# # ── Resume polling after human decision ───────────────────────────────────────
# if st.session_state.get("resumed") and "result" not in st.session_state:
#     job_id = st.session_state["job_id"]
#     status_placeholder = st.empty()
#     progress_bar = st.progress(90)

#     while True:
#         try:
#             r = requests.get(f"{API_BASE}/research/{job_id}", timeout=10)
#             r.raise_for_status()
#             job = r.json()
#         except Exception as e:
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Polling error: {e}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "completed":
#             progress_bar.progress(100)
#             st.session_state["result"] = job
#             st.session_state.pop("resumed", None)
#             status_placeholder.markdown(
#                 '<div class="status-box status-done">✅ Research complete! Navigate to the pages on the left.</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] in ("failed", "rejected"):
#             st.session_state.pop("resumed", None)
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Pipeline ended: {job.get("status")}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         status_placeholder.markdown(
#             '<div class="status-box status-running">📚 Formatting citations…</div>',
#             unsafe_allow_html=True,
#         )
#         time.sleep(3)

# # ── Show nav hint once done ───────────────────────────────────────────────────
# if "result" in st.session_state:
#     st.markdown("---")
#     st.markdown("### 📂 Your results are ready")
#     col1, col2, col3 = st.columns(3)
#     col1.page_link("pages/1_Report.py",   label="Report",   icon="📄")
#     col2.page_link("pages/2_Critique.py", label="Critique", icon="🧐")
#     col3.page_link("pages/3_Citations.py",label="Citations",icon="📚")


# import streamlit as st
# import requests
# import time


# import os
# API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

# st.set_page_config(
#     page_title="AI Research Pipeline",
#     page_icon="🔬",
#     layout="centered",
# )

# # ── Styles ──────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

#     html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#     .hero {
#         background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
#         border-radius: 16px;
#         padding: 48px 32px;
#         text-align: center;
#         margin-bottom: 32px;
#     }
#     .hero h1 { color: #fff; font-size: 2.4rem; margin-bottom: 8px; }
#     .hero p  { color: #bbb; font-size: 1.05rem; }

#     .step-row {
#         display: flex;
#         justify-content: center;
#         gap: 12px;
#         flex-wrap: wrap;
#         margin-bottom: 32px;
#     }
#     .step-pill {
#         background: #1e1e2e;
#         border: 1px solid #333;
#         border-radius: 24px;
#         padding: 6px 16px;
#         color: #a0a0c0;
#         font-size: 0.82rem;
#     }

#     div[data-testid="stTextInput"] input {
#         border-radius: 10px !important;
#         font-size: 1rem !important;
#         padding: 12px 16px !important;
#     }

#     div[data-testid="stButton"] button {
#         width: 100%;
#         padding: 14px;
#         border-radius: 10px;
#         font-size: 1rem;
#         font-weight: 600;
#         background: linear-gradient(135deg, #6c63ff, #48cfad);
#         color: white;
#         border: none;
#         cursor: pointer;
#         transition: opacity 0.2s;
#     }
#     div[data-testid="stButton"] button:hover { opacity: 0.9; }

#     .status-box {
#         border-radius: 10px;
#         padding: 16px 20px;
#         margin-top: 16px;
#         font-size: 0.95rem;
#     }
#     .status-running { background: #1a2a1a; border: 1px solid #2d5a2d; color: #6fcf6f; }
#     .status-done    { background: #1a1a2e; border: 1px solid #4a4a8a; color: #a0a0ff; }
#     .status-error   { background: #2a1a1a; border: 1px solid #8a2d2d; color: #ff8080; }
# </style>
# """, unsafe_allow_html=True)

# # ── Hero ─────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <h1>🔬 AI Research Pipeline</h1>
#     <p>Multi-agent research powered by LangGraph &amp; Mistral AI</p>
# </div>
# """, unsafe_allow_html=True)

# # ── Pipeline steps ────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="step-row">
#   <span class="step-pill">🔍 Web Search</span>
#   <span class="step-pill">🌐 Scrape</span>
#   <span class="step-pill">✍️ Write Report</span>
#   <span class="step-pill">🧐 Critique</span>
#   <span class="step-pill">📚 Citations</span>
# </div>
# """, unsafe_allow_html=True)

# # ── Input ─────────────────────────────────────────────────────────────────────
# topic = st.text_input(
#     "",
#     placeholder="e.g.  Impact of AI on healthcare in 2025",
#     label_visibility="collapsed",
# )

# if st.button("🚀  Run Research Pipeline"):
#     if not topic.strip():
#         st.warning("Please enter a research topic first.")
#     else:
#         with st.spinner("Starting pipeline…"):
#             try:
#                 resp = requests.post(f"{API_BASE}/research", json={"topic": topic.strip()}, timeout=10)
#                 resp.raise_for_status()
#                 data = resp.json()
#                 job_id = data["job_id"]
#                 st.session_state["job_id"] = job_id
#                 st.session_state["topic"] = topic.strip()
#                 st.session_state.pop("result", None)   # clear old result
#             except Exception as e:
#                 st.error(f"Could not reach the API: {e}")
#                 st.stop()

# # ── Polling ───────────────────────────────────────────────────────────────────
# if "job_id" in st.session_state and "result" not in st.session_state:
#     job_id = st.session_state["job_id"]
#     status_placeholder = st.empty()
#     progress_bar = st.progress(0)

#     step_labels = [
#         "🔍 Searching the web…",
#         "🌐 Scraping URLs…",
#         "✍️ Writing report…",
#         "🧐 Critiquing report…",
#         "📚 Formatting citations…",
#     ]
#     step_index = 0
#     poll_count = 0

#     while True:
#         try:
#             r = requests.get(f"{API_BASE}/research/{job_id}", timeout=10)
#             r.raise_for_status()
#             job = r.json()
#         except Exception as e:
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Polling error: {e}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "completed":
#             progress_bar.progress(100)
#             st.session_state["result"] = job
#             status_placeholder.markdown(
#                 '<div class="status-box status-done">✅ Research complete! Navigate to the pages on the left.</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         if job["status"] == "failed":
#             status_placeholder.markdown(
#                 f'<div class="status-box status-error">❌ Pipeline failed: {job.get("error")}</div>',
#                 unsafe_allow_html=True,
#             )
#             break

#         # Cycle through step labels while running
#         label = step_labels[step_index % len(step_labels)]
#         progress_bar.progress(min(5 + step_index * 15, 90))
#         status_placeholder.markdown(
#             f'<div class="status-box status-running">{label}</div>',
#             unsafe_allow_html=True,
#         )

#         poll_count += 1
#         if poll_count % 3 == 0:
#             step_index += 1

#         time.sleep(4)

# # ── Show nav hint once done ───────────────────────────────────────────────────
# if "result" in st.session_state:
#     st.markdown("---")
#     st.markdown("### 📂 Your results are ready")
#     col1, col2, col3 = st.columns(3)
#     col1.page_link("pages/1_Report.py",   label="Report",   icon="📄")
#     col2.page_link("pages/2_Critique.py", label="Critique", icon="🧐")
#     col3.page_link("pages/3_Citations.py",label="Citations",icon="📚")

import streamlit as st
import requests
import time
import os

from theme import inject, masthead

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Research Pipeline",
    page_icon="◆",
    layout="centered",
)

inject()

# ── Masthead ───────────────────────────────────────────────────────────────
masthead(
    eyebrow="Autonomous Research Desk",
    title="AI Research Pipeline",
    subtitle="Multi-agent research, orchestrated with LangGraph",
)

# ── Description ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="callout" style="margin-bottom: 26px;">
        Give the desk a topic and five specialist agents take it from there:
        one gathers current sources, one retrieves and reads them in full,
        one drafts a structured report, one fact-checks every claim against
        the retrieved sources, one critiques the draft for rigor, and one
        formats the citations in APA and IEEE. What comes back is a
        sourced, self-checked research brief — not a single model's
        best guess.
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Pipeline stepper (reflects the actual graph order) ───────────────────────
steps = ["Search", "Scrape", "Draft", "Fact-Check", "Critique", "Citations"]
step_cols = st.columns(len(steps))
for i, (col, label) in enumerate(zip(step_cols, steps), start=1):
    col.markdown(
        f"""
        <div style="text-align:center; padding: 10px 4px; border-top: 2px solid var(--hairline);">
            <div style="font-family:'IBM Plex Mono',monospace; font-size:0.68rem; color:var(--text-secondary); margin-bottom:3px;">{i:02d}</div>
            <div style="font-size:0.82rem; color:var(--text-primary);">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
topic = st.text_input(
    "Research topic",
    placeholder="e.g.  Impact of AI on healthcare in 2025",
    label_visibility="collapsed",
)

if st.button("Run research pipeline", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        with st.spinner("Starting pipeline…"):
            try:
                resp = requests.post(f"{API_BASE}/research", json={"topic": topic.strip()}, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                job_id = data["job_id"]
                st.session_state["job_id"] = job_id
                st.session_state["topic"] = topic.strip()
                st.session_state.pop("result", None)   # clear old result
            except Exception as e:
                st.error(f"Could not reach the API: {e}")
                st.stop()

# ── Polling ───────────────────────────────────────────────────────────────────
if "job_id" in st.session_state and "result" not in st.session_state:
    job_id = st.session_state["job_id"]
    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    step_labels = [
        "Searching the web…",
        "Scraping sources…",
        "Drafting the report…",
        "Fact-checking claims…",
        "Critiquing the draft…",
        "Formatting citations…",
    ]
    step_index = 0
    poll_count = 0

    while True:
        try:
            r = requests.get(f"{API_BASE}/research/{job_id}", timeout=10)
            r.raise_for_status()
            job = r.json()
        except Exception as e:
            status_placeholder.markdown(
                f'<div class="callout" style="border-left-color: var(--err); color: var(--err);">Polling error: {e}</div>',
                unsafe_allow_html=True,
            )
            break

        if job["status"] == "completed":
            progress_bar.progress(100)
            st.session_state["result"] = job
            status_placeholder.markdown(
                '<div class="callout" style="border-left-color: var(--ok); color: var(--ok);">Research complete — see the pages above.</div>',
                unsafe_allow_html=True,
            )
            break

        if job["status"] == "failed":
            status_placeholder.markdown(
                f'<div class="callout" style="border-left-color: var(--err); color: var(--err);">Pipeline failed: {job.get("error")}</div>',
                unsafe_allow_html=True,
            )
            break

        # Cycle through step labels while running
        label = step_labels[step_index % len(step_labels)]
        progress_bar.progress(min(5 + step_index * 14, 90))
        status_placeholder.markdown(
            f'<div class="callout">{label}</div>',
            unsafe_allow_html=True,
        )

        poll_count += 1
        if poll_count % 3 == 0:
            step_index += 1

        time.sleep(4)

# ── Show nav hint once done ───────────────────────────────────────────────────
if "result" in st.session_state:
    st.markdown("---")
    st.markdown("**Your results are ready**")
    col1, col2, col3, col4 = st.columns(4)
    col1.page_link("pages/1_Report.py",    label="Report")
    col2.page_link("pages/4_FactCheck.py", label="Fact Check")
    col3.page_link("pages/2_Critique.py",  label="Critique")
    col4.page_link("pages/3_Citations.py", label="Citations")