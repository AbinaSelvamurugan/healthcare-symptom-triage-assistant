"""Separate developer-only local entry point. NOT imported by public app."""
import json
import os
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="CareGuide developer evaluation", layout="wide")
if os.getenv("CAREGUIDE_ENABLE_DEV_DASHBOARD") != "true":
    st.error("Developer evaluation is disabled. Use the CLI reports instead.")
    st.stop()
st.title("Developer evaluation — synthetic software test results only")
st.warning("Run ONLY on a private machine, bound to 127.0.0.1. No access-control middleware is provided.")
root = Path(__file__).resolve().parents[2]
path = root / "reports" / "safety_report.json"
if not path.exists():
    st.warning("No generated report found. Run python scripts/run_guardrail_tests.py")
    st.stop()
report = json.loads(path.read_text(encoding="utf-8"))
st.json({"generated_at_utc": report.get("generated_at_utc"),
         "clinical_validation": report.get("clinical_validation"),
         "summary": report.get("summary"), "metrics": report.get("metrics")})
st.dataframe(report.get("scenario_results", []), use_container_width=True)
st.caption("Per-session transition traces exist only in memory in the core Session object; they are not collected from public users.")


st.subheader("Synthetic transition trace")
if st.button("Generate a fictional escalation trace"):
    from careguide.config import load_config
    from careguide.conversation.session import Session
    from careguide.services.triage import TriageService
    app_config, policy, protocol = load_config()
    app_config = app_config.model_copy(update={"mode": "offline_demo"})
    workflow = TriageService(app=app_config, policy=policy, protocol=protocol)
    synthetic = Session()
    synthetic.consent()
    workflow.submit(synthetic, "I have a headache")
    workflow.submit(synthetic, "severe breathing difficulty")
    st.write("**Decision trace (metadata only, no narrative):**")
    st.dataframe(synthetic.decision_trace, use_container_width=True)
    st.write("**State transitions:**")
    st.dataframe([{"from": old, "to": new} for old, new in synthetic.transitions],
                 use_container_width=True)

coverage_path = root / "reports" / "coverage.xml"
if coverage_path.exists():
    import xml.etree.ElementTree as ET
    try:
        line_rate = float(ET.parse(coverage_path).getroot().attrib["line-rate"])
        st.metric("Core Python line coverage (measured offline)", f"{line_rate:.1%}")
    except (KeyError, ValueError, ET.ParseError):
        st.warning("Coverage XML is invalid or unavailable")
