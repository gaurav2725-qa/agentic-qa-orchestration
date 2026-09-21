import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jira_client import fetch_jira_ticket
from agents.requirement_extractor import extract_requirements
from agents.edge_case_identifier import identify_edge_cases
from agents.gherkin_formatter import generate_gherkin


def run_pipeline(ticket_key):
    print("\n===== STEP 1: FETCHING FROM JIRA =====")
    ticket = fetch_jira_ticket(ticket_key)
    print("Key: " + ticket["key"])
    print("Summary: " + ticket["summary"])

    combined_story = ticket["summary"] + "\n\n" + ticket["description"]

    print("\n===== STEP 2: AGENT 1 - REQUIREMENT EXTRACTION =====")
    requirements_output = extract_requirements(combined_story)
    print(requirements_output)

    print("\n===== STEP 3: AGENT 2 - EDGE CASE IDENTIFICATION =====")
    edge_cases_output = identify_edge_cases(requirements_output)
    print(edge_cases_output)

    print("\n===== STEP 4: AGENT 3 - GHERKIN GENERATION =====")
    gherkin_output = generate_gherkin(requirements_output, edge_cases_output)
    print(gherkin_output)

    return {
        "ticket": ticket,
        "requirements": requirements_output,
        "edge_cases": edge_cases_output,
        "gherkin": gherkin_output
    }


if __name__ == "__main__":
    ticket_key = input("Enter Jira ticket key: ")
    result = run_pipeline(ticket_key)

    with open("output_" + ticket_key + ".feature", "w", encoding="utf-8") as f:
        f.write(str(result["gherkin"]))

    print("\n\nGherkin saved to output_" + ticket_key + ".feature")