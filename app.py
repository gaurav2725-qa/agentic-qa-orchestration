import streamlit as st
from jira_client import fetch_jira_ticket
from agents.requirement_extractor import extract_requirements
from agents.edge_case_identifier import identify_edge_cases

st.set_page_config(page_title="Agentic QA Orchestration", layout="wide")

st.title("🤖 Agentic QA Orchestration")
st.caption("Fetch a Jira ticket, extract requirements, and identify edge cases using AI agents")

ticket_key = st.text_input("Jira Ticket Key", placeholder="e.g. KAN-1")

if st.button("Run Full Analysis", type="primary"):
    if not ticket_key:
        st.warning("Please enter a ticket key.")
    else:
        with st.spinner("Fetching ticket from Jira..."):
            try:
                ticket = fetch_jira_ticket(ticket_key)
            except Exception as e:
                st.error("Failed to fetch ticket: " + str(e))
                st.stop()

        st.subheader("📋 Fetched from Jira")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Key:** " + ticket["key"])
            st.markdown("**Summary:** " + ticket["summary"])
        with col2:
            st.markdown("**Description:**")
            st.write(ticket["description"])

        combined_story = ticket["summary"] + "\n\n" + ticket["description"]

        with st.spinner("Agent 1: Extracting requirements... (10-20s)"):
            try:
                requirements_output = extract_requirements(combined_story)
            except Exception as e:
                st.error("Agent 1 failed: " + str(e))
                st.stop()

        st.subheader("🧠 Agent 1 — Requirements Analysis")
        st.markdown(str(requirements_output))

        with st.spinner("Agent 2: Identifying edge cases... (10-20s)"):
            try:
                edge_cases_output = identify_edge_cases(requirements_output)
            except Exception as e:
                st.error("Agent 2 failed: " + str(e))
                st.stop()

        st.subheader("🔍 Agent 2 — Edge Cases & Negative Scenarios")
        st.markdown(str(edge_cases_output))