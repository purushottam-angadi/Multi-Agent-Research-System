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


# ── Structured parsing ────────────────────────────────────────────────────────
# The fact_check_report tool always builds an exact "| Claim | Status |" markdown
# table with Status in {"Verified", "Unsupported", "Contradicted"}. Parse that
# table directly instead of regex-scanning the whole blob for keywords — scanning
# free text double-counts words like "accurate"/"confirmed" that show up naturally
# inside claim wording, not just in the Status column.
def parse_fact_check_table(fact_check: str):
    """Extract (claim, status) pairs from the markdown table the tool builds."""
    rows = []
    for line in fact_check.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        claim, status = cells
        if status in ("Verified", "Unsupported", "Contradicted"):
            rows.append((claim, status))
    return rows


parsed_rows = parse_fact_check_table(fact_check)
verified_count = sum(1 for _, s in parsed_rows if s == "Verified")
flagged_count  = sum(1 for _, s in parsed_rows if s in ("Unsupported", "Contradicted"))
total_claims   = len(parsed_rows)

# Fallback if parsing failed to find any valid rows (unexpected format upstream)
parse_failed = total_claims == 0

# ── Status stamp ───────────────────────────────────────────────────────────────
if parse_failed:
    stamp_html = stamp("Could not parse structured results — see full assessment below", "neutral")
elif flagged_count == 0 and verified_count > 0:
    stamp_html = stamp(f"{verified_count} claim(s) verified against sources", "ok")
elif flagged_count > 0:
    stamp_html = stamp(f"{flagged_count} claim(s) flagged for review", "warn")
else:
    stamp_html = stamp("Review the full assessment below", "neutral")

c1, c2 = st.columns([1, 4])
with c1:
    st.markdown(stamp_html, unsafe_allow_html=True)
with c2:
    if not parse_failed and total_claims:
        st.markdown(
            f'<span style="color: var(--text-secondary); font-size: 0.85rem;">'
            f'{verified_count} of {total_claims} claims verified · {flagged_count} flagged</span>',
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