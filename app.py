import streamlit as st
from jira_client import fetch_jira_ticket
from agents.requirement_extractor import extract_requirements

st.set_page_config(page_title="Agentic QA Orchestration", layout="wide")

st.title("🤖 Agentic QA Orchestration")
st.caption("Fetch a Jira ticket, extract structured requirements using an AI agent")

ticket_key = st.text_input("Jira Ticket Key", placeholder="e.g. KAN-1")

if st.button("Fetch and Analyze", type="primary"):
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

        st.subheader("🧠 Agent Analysis")
        with st.spinner("Agent analyzing requirements... (this can take 10-20s)"):
            try:
                result = extract_requirements(combined_story)
            except Exception as e:
                st.error("Agent execution failed: " + str(e))
                st.stop()

        st.markdown(str(result))