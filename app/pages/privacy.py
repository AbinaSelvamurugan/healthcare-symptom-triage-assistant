import streamlit as st


def render_privacy() -> None:
    st.title("Privacy and data use")
    st.warning("Fictional test scenarios only; never submit actual sensitive health information.")
    st.write("The default offline mode makes no external API calls, writes no conversation database, and does not retain symptoms across session resets. Streamlit keeps temporary history in the active browser/server session. Server logs are intended to contain only event codes and category metadata.")
    st.write("Claude demo mode transmits only the latest fictional scenario and protocol-provided instruction to Anthropic when permitted for a synthetic information scenario. Never enable this for real patient use without an appropriate privacy and legal review. No HIPAA, GDPR, or other regulatory compliance is claimed.")
    st.write("To discard active history, use Reset session. Session expiration is configurable. Operational deletion in a managed hosting environment requires a separate review of platform and provider retention policies.")
