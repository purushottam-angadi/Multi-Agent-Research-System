import streamlit as st
import re

from theme import inject, masthead, nav, stamp

st.set_page_config(page_title="Fact Check", page_icon="◆", layout="wide")

inject()

# Guard
if "result" not in st.session_state:
    st.warning("No research found. Please run the pipeline from the Home page first.")
    st.page_link("Home.py", label="← Go to Home")
    st.stop()

result     = st.session_state["result"]
topic      = st.session_state.get("topic", "Research Topic")
fact_check = result.get("fact_check", "")

# Header
masthead(
    eyebrow="Section 02 · Verification",
    title="Fact Check",
    subtitle=f"Topic: {topic}",
)

# Nav
nav("factcheck")

st.markdown("---")

if not fact_check:
    st.info("No fact-check data was returned for this run.")
    st.stop()

# ── Lightweight signal extraction ─────────────────────────────────────────────
# Doesn't assume a fixed output format from the fact-checker agent; just tallies
# how often verified vs. flagged language shows up, so the page can surface a
# clear at-a-glance status without editing the agent's own wording.
flagged_pattern  = re.compile(r"\bunverified\b|\bnot verified\b|\bunsupported\b|\bfalse\b|\bincorrect\b|\bcontradict(?:s|ed|ion)?\b|\bcannot be confirmed\b", re.IGNORECASE)
verified_pattern = re.compile(r"\bverified\b|\bsupported\b|\bconfirmed\b|\baccurate\b", re.IGNORECASE)

flagged_count  = len(flagged_pattern.findall(fact_check))
verified_count = len(verified_pattern.findall(fact_check))

if flagged_count == 0 and verified_count > 0:
    stamp_html = stamp(f"{verified_count} claim(s) verified against sources", "ok")
elif flagged_count > 0:
    stamp_html = stamp(f"{flagged_count} claim(s) flagged for review", "warn")
else:
    stamp_html = stamp("Review the full assessment below", "neutral")

c1, c2 = st.columns([1, 4])
with c1:
    st.markdown(stamp_html, unsafe_allow_html=True)
with c2:
    if verified_count or flagged_count:
        st.markdown(
            f'<span style="color: var(--text-secondary); font-size: 0.85rem;">'
            f'{verified_count} supported reference(s) · {flagged_count} flagged reference(s)</span>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Full assessment ────────────────────────────────────────────────────────────
st.markdown('<p class="panel-label">Full assessment</p>', unsafe_allow_html=True)
st.markdown('<div class="doc-panel">', unsafe_allow_html=True)
st.markdown(fact_check)
st.markdown('</div>', unsafe_allow_html=True)

# Download
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="Download fact check (.txt)",
    data=fact_check,
    file_name=f"factcheck_{topic[:30].replace(' ','_')}.txt",
    mime="text/plain",
    use_container_width=True,
)
