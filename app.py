import streamlit as st
import subprocess
from jira_client import fetch_jira_ticket
from agents.requirement_extractor import extract_requirements
from agents.edge_case_identifier import identify_edge_cases
from agents.gherkin_formatter import generate_gherkin
from agents.step_definition_generator import generate_step_definitions

st.set_page_config(page_title="Agentic QA Orchestration", layout="wide")

st.title("🤖 Agentic QA Orchestration")
st.caption("Jira ticket → requirements → edge cases → Gherkin → automation code → real execution")

ticket_key = st.text_input("Jira Ticket Key", placeholder="e.g. KAN-2")

if "gherkin_output" not in st.session_state:
    st.session_state.gherkin_output = None
if "step_code" not in st.session_state:
    st.session_state.step_code = None

if st.button("Run Analysis (Agents 1–3)", type="primary"):
    if not ticket_key:
        st.warning("Please enter a ticket key.")
    else:
        with st.spinner("Fetching ticket from Jira..."):
            ticket = fetch_jira_ticket(ticket_key)

        st.subheader("📋 Fetched from Jira")
        st.markdown("**Key:** " + ticket["key"] + " — **Summary:** " + ticket["summary"])
        st.write(ticket["description"])

        combined_story = ticket["summary"] + "\n\n" + ticket["description"]

        with st.spinner("Agent 1: Extracting requirements..."):
            requirements_output = extract_requirements(combined_story)
        st.subheader("🧠 Agent 1 — Requirements")
        st.markdown(str(requirements_output))

        with st.spinner("Agent 2: Identifying edge cases..."):
            edge_cases_output = identify_edge_cases(requirements_output)
        st.subheader("🔍 Agent 2 — Edge Cases")
        st.markdown(str(edge_cases_output))

        with st.spinner("Agent 3: Generating Gherkin..."):
            gherkin_output = generate_gherkin(requirements_output, edge_cases_output)
        st.subheader("✅ Agent 3 — Gherkin Scenarios")
        st.code(gherkin_output, language="gherkin")

        st.session_state.gherkin_output = gherkin_output

if st.session_state.gherkin_output:
    st.divider()
    st.subheader("🛠️ Agent 4 — Generate Automation Code")
    st.caption("Paste ONE scenario from above to generate step definitions for it")

    scenario_input = st.text_area(
        "Scenario to automate",
        height=150,
        placeholder="Paste a single Scenario block here"
    )

    if st.button("Generate Step Definitions"):
        with st.spinner("Agent 4: Writing Selenium step definitions..."):
            step_code = generate_step_definitions(scenario_input)
        st.session_state.step_code = step_code

if st.session_state.step_code:
    st.subheader("👀 Review Generated Code Before Running")
    st.warning(
        "Review this code carefully — AI-generated automation "
        "code can contain bugs (e.g. invented methods, syntax "
        "errors). Edit below if needed before running."
    )
    edited_code = st.text_area(
        "Generated step definitions (editable)",
        value=st.session_state.step_code,
        height=300
    )

    st.info(
        "To run: copy the reviewed/corrected code above into "
        "features/steps/login_steps.py manually, then click "
        "'Run Tests' below."
    )

    if st.button("▶️ Run Tests (behave)", type="primary"):
        with st.spinner("Running behave against the real page..."):
            result = subprocess.run(
                ["behave", "features/login.feature"],
                capture_output=True,
                text=True
            )

        st.subheader("📊 Test Execution Results")
        if result.returncode == 0:
            st.success("All scenarios passed!")
        else:
            st.error("Some scenarios failed — see output below")

        st.code(result.stdout, language="text")
        if result.stderr:
            with st.expander("stderr (usually safe to ignore Selenium cleanup noise)"):
                st.code(result.stderr, language="text")