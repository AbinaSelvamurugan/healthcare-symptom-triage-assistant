"""Presentation never bypasses the independent safety and validation layers."""
import streamlit as st

from careguide.config import load_config
from careguide.conversation.session import Session
from careguide.conversation.state import State
from careguide.llm.anthropic_client import AnthropicProvider, ProviderUnavailable
from careguide.services.presentation import banner_for
from careguide.services.triage import TriageService


def render_triage() -> None:
    st.title("CareGuide AI")
    st.subheader("Safety-First Symptom Triage Architecture — Educational Demo")
    st.error("NOT A MEDICAL SERVICE. UNVALIDATED DEMONSTRATION RULES. Do not enter real patient data or rely on outputs for medical decisions. For a real emergency, contact your local emergency service.")
    try:
        app, policy, protocol = load_config()
    except Exception:
        st.error("Clinical/demo configuration unavailable or invalid. The application cannot process scenarios.")
        st.stop()
    st.caption(f"Mode: {app.mode} · Jurisdiction: {app.jurisdiction} · Protocol: {protocol.protocol_id} ({protocol.status})")
    with st.expander("Processing and privacy disclosure (read before starting)", expanded=True):
        st.write("Use fictional scenarios only. Messages are held only in your current Streamlit session, not stored in a database. Reset and session expiry clear them. Offline demo sends nothing externally. In Claude demo mode, your latest fictional input is sent to the external Anthropic API. This is NOT clinical triage.")
        st.write("The demo phrase rules are simplified test fixtures and may miss emergencies. A missing match is never proof of safety.")
    if "careguide_session" not in st.session_state:
        st.session_state.careguide_session = Session()
        st.session_state.careguide_history = []
    session = st.session_state.careguide_session
    if session.expired(app.session_ttl_minutes):
        st.session_state.careguide_session = Session()
        st.session_state.careguide_history = []
        st.warning("Session expired. Fictional conversation memory was discarded; please accept the disclosure again.")
        session = st.session_state.careguide_session
    if st.button("Reset session and delete in-memory conversation"):
        st.session_state.careguide_session = session.reset()
        st.session_state.careguide_history = []
        st.rerun()
    if session.state.value == "DISCLOSURE":
        accepted = st.checkbox("I understand this is for FICTIONAL scenarios only and is not medical advice or a real emergency service.")
        if st.button("Start fictional scenario", disabled=not accepted):
            session.consent()
            st.rerun()
        return
    if session.state == State.COMPLETE:
        st.info("This fictional scenario is complete. Use Reset to clear the session and start again.")
        return
    if session.state not in (State.EMERGENCY, State.URGENT):
        if st.button("Complete fictional scenario"):
            session.complete()
            st.rerun()
    provider = None
    if app.mode == "claude_demo":
        try:
            provider = AnthropicProvider(timeout=app.provider_timeout_seconds,
                                         max_retries=app.provider_max_retries)
        except ProviderUnavailable:
            st.warning("Claude credentials or model configuration unavailable. Rules still run; optional language generation will fail safely.")
    service = TriageService(app=app, policy=policy, protocol=protocol, provider=provider)
    for item in st.session_state.careguide_history:
        with st.chat_message(item["role"]):
            if item["role"] == "user":
                st.text(item["text"])
            else:
                decision = item["decision"]
                banner = banner_for(decision)
                st.markdown(f"**{banner.heading}**")
                if banner.kind == "EMERGENCY":
                    st.error(banner.instruction, icon="🚨")
                elif banner.kind in ("URGENT", "PROVIDER_FAILURE", "CLINICIAN_REFERRAL"):
                    st.warning(banner.instruction, icon="⚠️")
                else:
                    st.info(banner.instruction)
                if decision.next_question:
                    st.write("**Protocol-defined question:** " + decision.next_question)
    if session.state in (State.EMERGENCY, State.URGENT):
        st.warning("The configured demonstration escalation is active. Routine follow-up is stopped; do not wait for this chat to pursue real emergency assistance.")
    message = st.chat_input("Enter a FICTIONAL symptom scenario (no real patient information)",
                            disabled=session.state in (State.EMERGENCY, State.URGENT))
    if message:
        try:
            decision = service.submit(session, message)
            st.session_state.careguide_history.extend([
                {"role": "user", "text": message}, {"role": "assistant", "decision": decision}
            ])
        except ValueError:
            st.error("Unable to process input: verify the disclosure, text length, and session state. No medical assessment was made.")
        st.rerun()
