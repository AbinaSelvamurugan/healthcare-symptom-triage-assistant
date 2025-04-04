"""Local fictional-scenario demonstration; no default persistence or analytics."""
import streamlit as st

from app.pages.privacy import render_privacy
from app.pages.triage import render_triage

st.set_page_config(page_title="CareGuide AI — DEMO ONLY", page_icon="🛡️", layout="centered")
st.sidebar.title("CareGuide AI")
st.sidebar.caption("Unvalidated software demonstration; not a clinical service")
selection = st.sidebar.radio("Page", ["Fictional scenario demo", "Privacy and data use"])
if selection == "Fictional scenario demo":
    render_triage()
else:
    render_privacy()
