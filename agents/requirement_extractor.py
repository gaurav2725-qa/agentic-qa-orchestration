import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jira_client import fetch_jira_ticket

load_dotenv()

from agents.llm_config import get_llm

gemini_llm = get_llm()

requirement_extractor = Agent(
    role="Requirements Analyst",
    goal="Extract explicit requirements, user roles, and "
         "implicit preconditions from raw user stories",
    backstory="You are a senior business analyst with 10 years "
              "of experience turning ambiguous stakeholder "
              "requests into precise, structured requirements "
              "that development teams can act on without "
              "ambiguity.",
    llm=gemini_llm,
    verbose=True
)


def extract_requirements(user_story):
    extraction_task = Task(
        description=(
            "Analyze this user story and extract:\n"
            "1. User role(s) involved\n"
            "2. Explicit stated requirements\n"
            "3. Implicit/unstated preconditions\n\n"
            "User Story:\n" + user_story
        ),
        expected_output=(
            "A structured breakdown with three clearly "
            "labeled sections: User Roles, Explicit "
            "Requirements, and Implicit Preconditions."
        ),
        agent=requirement_extractor
    )

    crew = Crew(
        agents=[requirement_extractor],
        tasks=[extraction_task],
        verbose=True
    )

    result = crew.kickoff()
    return result


if __name__ == "__main__":
    ticket_key = input("Enter Jira ticket key: ")
    ticket = fetch_jira_ticket(ticket_key)

    combined_story = ticket["summary"] + "\n\n" + ticket["description"]

    print("\n===== FETCHED FROM JIRA =====")
    print("Key: " + ticket["key"])
    print("Summary: " + ticket["summary"])
    print("Description: " + ticket["description"])

    output = extract_requirements(combined_story)

    print("\n\n===== AGENT OUTPUT =====")
    print(output)