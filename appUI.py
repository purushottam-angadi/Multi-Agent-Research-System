import streamlit as st
import time
import io
from contextlib import redirect_stdout

st.set_page_config(
    page_title="NEXUS · Research Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg:      #080c12;
    --surface: #0d1117;
    --border:  #1e2a38;
    --accent:  #00e5ff;
    --accent2: #7c3aed;
    --text:    #e2e8f0;
    --muted:   #4a5568;
    --success: #10b981;
    --warn:    #f59e0b;
    --mono:    'Space Mono', monospace;
    --display: 'Syne', sans-serif;
    --body:    'Inter', sans-serif;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton           { display: none; }

/* ── Kill every ghost box Streamlit injects ── */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] > div,
[data-testid="stVerticalBlock"] > [data-testid="element-container"],
.element-container,
.stMarkdown,
div[class*="block-container"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* ── Specifically nuke the empty first markdown container ── */
[data-testid="stVerticalBlock"] > div:empty,
[data-testid="stVerticalBlock"] > div > [data-testid="stMarkdownContainer"]:empty {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ── Streamlit column gap / padding cleanup ── */
[data-testid="stHorizontalBlock"] {
    gap: 2rem !important;
    align-items: flex-start !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent2); border-radius: 2px; }

/* ══════════════════════════════════════
   MASTHEAD
══════════════════════════════════════ */
.nexus-masthead {
    display: flex; align-items: center; gap: 18px;
    padding: 36px 0 6px; margin-bottom: 0;
}
.nexus-hex {
    width: 54px; height: 54px; flex-shrink: 0;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    clip-path: polygon(50% 0%,95% 25%,95% 75%,50% 100%,5% 75%,5% 25%);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    animation: hexPulse 3s ease-in-out infinite;
}
@keyframes hexPulse {
    0%,100% { filter: drop-shadow(0 0 8px rgba(0,229,255,.4)); }
    50%      { filter: drop-shadow(0 0 22px rgba(0,229,255,.85)); }
}
.nexus-title-block h1 {
    font-family: var(--display) !important;
    font-size: 2.6rem !important; font-weight: 800 !important;
    letter-spacing: -0.04em !important;
    background: linear-gradient(90deg, var(--accent) 0%, #a78bfa 60%, var(--accent2) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    line-height: 1 !important; margin: 0 !important; padding: 0 !important;
}
.nexus-title-block p {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important; color: var(--muted) !important;
    letter-spacing: 0.22em !important; text-transform: uppercase !important;
    margin: 6px 0 0 !important;
}
.nexus-divider {
    height: 1px;
    background: linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);
    margin: 16px 0 28px; opacity: .5;
}

/* ══════════════════════════════════════
   INPUT CARD  — no Streamlit wrapping
══════════════════════════════════════ */
.input-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 24px 24px 20px;
    position: relative; overflow: hidden; margin-bottom: 0;
}
.input-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.input-label {
    font-family: var(--mono) !important; font-size: 0.68rem !important;
    letter-spacing: 0.2em !important; text-transform: uppercase !important;
    color: var(--accent) !important; margin: 0 0 10px !important; display: block;
}

/* ── Text input ── */
.stTextInput { margin-top: 0 !important; }
.stTextInput label { display: none !important; }
.stTextInput > div > div > input {
    background: #0a0f16 !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: var(--mono) !important; font-size: 0.95rem !important;
    padding: 13px 16px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,.12) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Launch button ── */
.stButton > button {
    background: linear-gradient(135deg, #00b4cc, var(--accent2)) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-family: var(--display) !important; font-size: 0.95rem !important;
    font-weight: 700 !important; letter-spacing: 0.04em !important;
    padding: 12px 32px !important; cursor: pointer !important;
    transition: opacity .2s, transform .15s !important; width: 100% !important;
    margin-top: 6px !important;
}
.stButton > button:hover  { opacity: .88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ══════════════════════════════════════
   STEP CARDS  (4-up grid via HTML)
══════════════════════════════════════ */
.steps-wrapper {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 10px; margin: 22px 0 0;
}
.step-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 14px 12px;
    position: relative; transition: border-color .3s, opacity .3s;
}
.step-card.active  { border-color: var(--accent); }
.step-card.done    { border-color: var(--success); }
.step-card.waiting { opacity: .4; }
.step-icon { font-size: 1.3rem; margin-bottom: 7px; display: block; }
.step-name {
    font-family: var(--display); font-weight: 700; font-size: .78rem;
    color: var(--text); margin-bottom: 2px;
}
.step-desc { font-size: .67rem; color: var(--muted); line-height: 1.4; }
.step-badge {
    position: absolute; top: 8px; right: 9px;
    font-family: var(--mono); font-size: .56rem;
    padding: 2px 7px; border-radius: 99px;
}
.step-badge.active  { background: rgba(0,229,255,.15); color: var(--accent); }
.step-badge.done    { background: rgba(16,185,129,.15); color: var(--success); }
.step-badge.waiting { background: rgba(74,85,104,.12); color: var(--muted); }

/* ══════════════════════════════════════
   METRICS ROW
══════════════════════════════════════ */
.metrics-row {
    display: grid; grid-template-columns: repeat(2,1fr);
    gap: 10px; margin-top: 20px;
}
.metric-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px; text-align: center;
}
.metric-value {
    font-family: var(--display); font-size: 1.7rem; font-weight: 800;
    background: linear-gradient(90deg, var(--accent), #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}
.metric-label {
    font-family: var(--mono); font-size: .62rem; color: var(--muted);
    text-transform: uppercase; letter-spacing: .15em; margin-top: 4px;
}

/* ══════════════════════════════════════
   STATUS BAR
══════════════════════════════════════ */
.status-bar {
    display: flex; align-items: center; gap: 10px; padding: 10px 16px;
    background: rgba(0,229,255,.05); border: 1px solid rgba(0,229,255,.15);
    border-radius: 8px; margin-bottom: 20px;
}
.status-dot {
    width: 8px; height: 8px; border-radius: 50%; background: var(--accent);
    animation: blink 1.2s ease-in-out infinite; flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.15} }
.status-text {
    font-family: var(--mono); font-size: .72rem;
    color: var(--accent); letter-spacing: .08em;
}

/* ══════════════════════════════════════
   RESULT PANELS
══════════════════════════════════════ */
.result-panel {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; margin-bottom: 20px; overflow: hidden;
}
.result-panel-header {
    display: flex; align-items: center; gap: 12px;
    padding: 13px 18px; border-bottom: 1px solid var(--border);
    background: rgba(255,255,255,.02);
}
.result-panel-header .rph-icon { font-size: 1.1rem; }
.result-panel-header .rph-title {
    font-family: var(--display); font-weight: 700;
    font-size: .88rem; color: var(--text); flex: 1;
}
.result-panel-header .rph-tag {
    font-family: var(--mono); font-size: .6rem;
    padding: 3px 10px; border-radius: 99px;
    background: rgba(0,229,255,.1); color: var(--accent);
}
.result-panel-body {
    padding: 20px; font-size: .87rem; line-height: 1.8;
    color: #cbd5e0; white-space: pre-wrap; word-break: break-word;
    max-height: 500px; overflow-y: auto;
}
.report-panel .result-panel-header  { border-bottom-color: rgba(124,58,237,.3); }
.report-panel .rph-tag              { background: rgba(124,58,237,.15) !important; color: #a78bfa !important; }
.critique-panel .result-panel-header{ border-bottom-color: rgba(245,158,11,.2); }
.critique-panel .rph-tag            { background: rgba(245,158,11,.1) !important; color: var(--warn) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]  { background: transparent !important; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--muted) !important;
    font-family: var(--display) !important; font-weight: 600 !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(0,229,255,.1) !important;
    border-color: var(--accent) !important; color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(0,229,255,.07) !important;
    border: 1px solid rgba(0,229,255,.22) !important;
    color: var(--accent) !important; border-radius: 8px !important;
    font-family: var(--mono) !important; font-size: .74rem !important;
    letter-spacing: .05em !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,229,255,.14) !important;
}

/* ── Alert ── */
[data-testid="stAlert"] {
    background: rgba(0,229,255,.05) !important;
    border: 1px solid rgba(0,229,255,.2) !important;
    border-radius: 8px !important; color: var(--text) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    border-color: var(--accent) transparent transparent transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "pipeline_ran": False,
    "state": {},
    "elapsed": 0.0,
    "step_status": {1:"waiting", 2:"waiting", 3:"waiting", 4:"waiting"},
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Pure-HTML step card grid (no Streamlit columns) ───────────────────────────
def render_step_cards(statuses):
    steps = [
        ("🔍", "Search",  "Live web crawl",    1),
        ("🕷️", "Scrape",  "Page extraction",   2),
        ("✍️", "Report",  "AI synthesis",      3),
        ("🧠", "Critique","Quality review",    4),
    ]
    cards = ""
    for icon, name, desc, num in steps:
        s = statuses[num]
        badge = {"active":"RUNNING","done":"DONE","waiting":"QUEUED"}[s]
        cards += f"""
        <div class="step-card {s}">
            <span class="step-badge {s}">{badge}</span>
            <span class="step-icon">{icon}</span>
            <div class="step-name">{name}</div>
            <div class="step-desc">{desc}</div>
        </div>"""
    st.markdown(f'<div class="steps-wrapper">{cards}</div>', unsafe_allow_html=True)


def render_result_panel(icon, title, tag, content, extra_class=""):
    st.markdown(f"""
    <div class="result-panel {extra_class}">
        <div class="result-panel-header">
            <span class="rph-icon">{icon}</span>
            <span class="rph-title">{title}</span>
            <span class="rph-tag">{tag}</span>
        </div>
        <div class="result-panel-body">{content}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MASTHEAD  — single st.markdown call, nothing above it
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nexus-masthead">
    <div class="nexus-hex">⬡</div>
    <div class="nexus-title-block">
        <h1>NEXUS</h1>
        <p>Multi-Agent Research Intelligence Platform</p>
    </div>
</div>
<div class="nexus-divider"></div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1, 2], gap="large")

# ════════════  LEFT  ══════════════════════════════════════════════════════════
with left:
    # ── The label sits INSIDE the same HTML block as the card border,
    #    so no Streamlit container can sneak in between them.
    st.markdown("""
    <div class="input-card">
        <span class="input-label">⬡ Research Query</span>
    </div>
    """, unsafe_allow_html=True)

    # Overlap the real input widgets right after — CSS keeps them visually inside
    topic = st.text_input(
        label="Research topic",
        placeholder="e.g.  Quantum computing breakthroughs 2025",
        label_visibility="collapsed",
        key="topic_input",
    )
    run_btn = st.button("⬡  Launch Pipeline", use_container_width=True)

    # Step cards (pure HTML grid — no st.columns, no spacing issues)
    render_step_cards(st.session_state.step_status)

    # Metrics after a run
    if st.session_state.pipeline_ran:
        elapsed = st.session_state.elapsed
        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card">
                <div class="metric-value">{elapsed:.0f}s</div>
                <div class="metric-label">Time</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">4</div>
                <div class="metric-label">Stages</div>
            </div>
        </div>""", unsafe_allow_html=True)


# ════════════  RIGHT  ═════════════════════════════════════════════════════════
with right:

    # Idle state
    if not st.session_state.pipeline_ran and not run_btn:
        st.markdown("""
        <div style="text-align:center;padding:90px 40px;">
            <div style="font-size:3.8rem;margin-bottom:18px;opacity:.35">⬡</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:700;
                        color:#4a5568;letter-spacing:-.02em;margin-bottom:10px;">
                Awaiting Research Query
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:.73rem;color:#2d3748;
                        max-width:320px;margin:0 auto;line-height:1.9;">
                Enter a topic on the left and launch<br>
                the four-stage multi-agent pipeline.<br><br>
                SEARCH → SCRAPE → WRITE → CRITIQUE
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Run ──
    if run_btn:
        if not topic.strip():
            st.warning("Please enter a research topic before launching.")
            st.stop()

        st.session_state.step_status  = {1:"waiting",2:"waiting",3:"waiting",4:"waiting"}
        st.session_state.pipeline_ran = False

        try:
            from pipeline import run_research_pipe
        except ImportError as e:
            st.error(f"Could not import pipeline.py — make sure it's in the same directory.\n\n`{e}`")
            st.stop()

        start = time.time()

        status_ph = st.empty()
        status_ph.markdown("""
        <div class="status-bar">
            <div class="status-dot"></div>
            <span class="status-text">Pipeline running — this may take a moment…</span>
        </div>""", unsafe_allow_html=True)

        buf = io.StringIO()
        try:
            with st.spinner("Running all four pipeline stages…"):
                with redirect_stdout(buf):
                    state = run_research_pipe(topic)
        except Exception as exc:
            st.error(f"Pipeline error: {exc}")
            st.stop()

        st.session_state.elapsed      = time.time() - start
        st.session_state.step_status  = {1:"done",2:"done",3:"done",4:"done"}
        st.session_state.state        = state
        st.session_state.pipeline_ran = True
        st.rerun()

    # ── Results ──
    if st.session_state.pipeline_ran:
        state = st.session_state.state
        st.markdown("""
        <div class="status-bar" style="background:rgba(16,185,129,.05);border-color:rgba(16,185,129,.2);">
            <div class="status-dot" style="background:#10b981;animation:none;"></div>
            <span class="status-text" style="color:#10b981;">Pipeline complete — results ready</span>
        </div>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["✍️  Research Report", "🧠  AI Critique"])

        with tab1:
            render_result_panel(
                "✍️", "Research Report", "SYNTHESISED OUTPUT",
                state.get("report","No report generated."),
                extra_class="report-panel"
            )
            st.download_button(
                label="⬇  Download Report (.txt)",
                data=state.get("report",""),
                file_name=f"nexus_report_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with tab2:
            render_result_panel(
                "🧠", "AI Critique & Feedback", "QUALITY ASSESSMENT",
                state.get("feedback","No critique generated."),
                extra_class="critique-panel"
            )


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 0 20px;border-top:1px solid #1e2a38;margin-top:40px;">
    <span style="font-family:'Space Mono',monospace;font-size:.63rem;color:#2d3748;letter-spacing:.2em;">
        NEXUS · MULTI-AGENT RESEARCH INTELLIGENCE · POWERED BY LANGCHAIN AGENTS
    </span>
</div>
""", unsafe_allow_html=True)