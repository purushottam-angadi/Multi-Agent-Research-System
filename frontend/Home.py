import streamlit as st
import requests
import time


import os
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Research Pipeline",
    page_icon="🔬",
    layout="centered",
)

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .hero {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        border-radius: 16px;
        padding: 48px 32px;
        text-align: center;
        margin-bottom: 32px;
    }
    .hero h1 { color: #fff; font-size: 2.4rem; margin-bottom: 8px; }
    .hero p  { color: #bbb; font-size: 1.05rem; }

    .step-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 32px;
    }
    .step-pill {
        background: #1e1e2e;
        border: 1px solid #333;
        border-radius: 24px;
        padding: 6px 16px;
        color: #a0a0c0;
        font-size: 0.82rem;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
    }

    div[data-testid="stButton"] button {
        width: 100%;
        padding: 14px;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        background: linear-gradient(135deg, #6c63ff, #48cfad);
        color: white;
        border: none;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    div[data-testid="stButton"] button:hover { opacity: 0.9; }

    .status-box {
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 16px;
        font-size: 0.95rem;
    }
    .status-running { background: #1a2a1a; border: 1px solid #2d5a2d; color: #6fcf6f; }
    .status-done    { background: #1a1a2e; border: 1px solid #4a4a8a; color: #a0a0ff; }
    .status-error   { background: #2a1a1a; border: 1px solid #8a2d2d; color: #ff8080; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 AI Research Pipeline</h1>
    <p>Multi-agent research powered by LangGraph &amp; Mistral AI</p>
</div>
""", unsafe_allow_html=True)

# ── Pipeline steps ────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-row">
  <span class="step-pill">🔍 Web Search</span>
  <span class="step-pill">🌐 Scrape</span>
  <span class="step-pill">✍️ Write Report</span>
  <span class="step-pill">🧐 Critique</span>
  <span class="step-pill">📚 Citations</span>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
topic = st.text_input(
    "",
    placeholder="e.g.  Impact of AI on healthcare in 2025",
    label_visibility="collapsed",
)

if st.button("🚀  Run Research Pipeline"):
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
        "🔍 Searching the web…",
        "🌐 Scraping URLs…",
        "✍️ Writing report…",
        "🧐 Critiquing report…",
        "📚 Formatting citations…",
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
                f'<div class="status-box status-error">❌ Polling error: {e}</div>',
                unsafe_allow_html=True,
            )
            break

        if job["status"] == "completed":
            progress_bar.progress(100)
            st.session_state["result"] = job
            status_placeholder.markdown(
                '<div class="status-box status-done">✅ Research complete! Navigate to the pages on the left.</div>',
                unsafe_allow_html=True,
            )
            break

        if job["status"] == "failed":
            status_placeholder.markdown(
                f'<div class="status-box status-error">❌ Pipeline failed: {job.get("error")}</div>',
                unsafe_allow_html=True,
            )
            break

        # Cycle through step labels while running
        label = step_labels[step_index % len(step_labels)]
        progress_bar.progress(min(5 + step_index * 15, 90))
        status_placeholder.markdown(
            f'<div class="status-box status-running">{label}</div>',
            unsafe_allow_html=True,
        )

        poll_count += 1
        if poll_count % 3 == 0:
            step_index += 1

        time.sleep(4)

# ── Show nav hint once done ───────────────────────────────────────────────────
if "result" in st.session_state:
    st.markdown("---")
    st.markdown("### 📂 Your results are ready")
    col1, col2, col3 = st.columns(3)
    col1.page_link("pages/1_Report.py",   label="Report",   icon="📄")
    col2.page_link("pages/2_Critique.py", label="Critique", icon="🧐")
    col3.page_link("pages/3_Citations.py",label="Citations",icon="📚")
