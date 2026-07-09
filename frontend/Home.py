
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
    subtitle="A Multi-Agent Research System",
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
        sourced, self-checked research brief, not a single model's
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