import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

edge_case_identifier = Agent(
    role="QA Edge Case Specialist",
    goal="Identify edge cases, negative scenarios, and boundary "
         "conditions that requirements analysis alone tends to miss",
    backstory=(
        "You are a senior QA engineer with a reputation for "
        "finding the bugs no one else thinks of. You specialize "
        "in asking 'what happens if...' for every requirement: "
        "what if the input is empty, what if the user has no "
        "permission, what if the network fails mid-action, what "
        "if two users do this simultaneously. You never accept a "
        "requirement as fully understood until you've stress-"
        "tested it against failure scenarios."
    ),
    llm=gemini_llm,
    verbose=True
)


def identify_edge_cases(requirement_analysis):
    edge_case_task = Task(
        description=(
            "Below is a structured requirements analysis "
            "(user roles, explicit requirements, implicit "
            "preconditions) for a feature. Your job is to "
            "identify edge cases and negative scenarios this "
            "analysis has NOT already covered.\n\n"
            "Focus specifically on:\n"
            "- Boundary conditions (empty states, maximum "
            "limits, zero/negative values)\n"
            "- Error and failure scenarios (network failure, "
            "timeout, invalid input, permission denial)\n"
            "- Concurrency issues (simultaneous actions by "
            "multiple users or sessions)\n"
            "- Security-adjacent concerns (unauthorized access "
            "attempts, data exposure risks)\n\n"
            "Do not repeat anything already listed in the "
            "analysis below. Only add genuinely new scenarios.\n\n"
            "Requirements Analysis:\n" + str(requirement_analysis)
        ),
        expected_output=(
            "A bulleted list of edge cases and negative "
            "scenarios, grouped under clear headings "
            "(Boundary Conditions, Error/Failure Scenarios, "
            "Concurrency Issues, Security Concerns). Each item "
            "should be a single, specific, testable scenario."
        ),
        agent=edge_case_identifier
    )

    crew = Crew(
        agents=[edge_case_identifier],
        tasks=[edge_case_task],
        verbose=True
    )

    result = crew.kickoff()
    return result


if __name__ == "__main__":
    sample_analysis = """
    User Roles: Registered Customer

    Explicit Requirements:
    - Export functionality accessible from account dashboard
    - Output must be a downloadable PDF
    - Must include complete order history
    - Must contain order dates, item names, quantities, totals

    Implicit Preconditions:
    - User must be authenticated
    - Order data must exist in the database
    - PDF generation service must be available
    """

    output = identify_edge_cases(sample_analysis)
    print("\n\n===== EDGE CASES OUTPUT =====")
    print(output)