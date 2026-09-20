import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-3.6-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

gherkin_formatter = Agent(
    role="BDD Test Scenario Writer",
    goal="Convert requirements and edge cases into precise, "
         "executable Gherkin/BDD scenarios",
    backstory=(
        "You are a senior SDET who specializes in writing "
        "Gherkin scenarios that are both readable by business "
        "stakeholders and precise enough for automation engineers "
        "to implement directly as step definitions. You always "
        "write scenarios covering the happy path first, then "
        "systematically cover edge cases and negative scenarios "
        "as separate, clearly-titled scenarios within the same "
        "feature file."
    ),
    llm=gemini_llm,
    verbose=True
)


def generate_gherkin(requirements_analysis, edge_cases):
    gherkin_task = Task(
        description=(
            "Using the requirements analysis and edge cases "
            "below, write a complete Gherkin feature file.\n\n"
            "Rules:\n"
            "- Start with a Feature: line and a short "
            "description of the feature\n"
            "- Write one Scenario for the primary happy path, "
            "based on the explicit requirements\n"
            "- Write one additional Scenario for each distinct "
            "edge case category (Boundary Conditions, "
            "Error/Failure Scenarios, Concurrency Issues, "
            "Security Concerns) — pick the single most "
            "important scenario from each category, don't try "
            "to cover every edge case individually\n"
            "- Use proper Given/When/Then/And syntax\n"
            "- Keep each step concise and specific — avoid vague "
            "steps like 'the system works correctly'\n"
            "- Output ONLY the Gherkin syntax, no extra "
            "commentary before or after\n\n"
            "Requirements Analysis:\n" + str(requirements_analysis) +
            "\n\nEdge Cases:\n" + str(edge_cases)
        ),
        expected_output=(
            "A complete, valid Gherkin feature file with a "
            "Feature declaration and 4-5 Scenarios covering the "
            "happy path plus one representative scenario per "
            "edge case category."
        ),
        agent=gherkin_formatter
    )

    crew = Crew(
        agents=[gherkin_formatter],
        tasks=[gherkin_task],
        verbose=True
    )

    result = crew.kickoff()
    return result


if __name__ == "__main__":
    sample_requirements = """
    User Roles: Registered Customer
    Explicit Requirements:
    - Export functionality accessible from account dashboard
    - Output must be a downloadable PDF
    - Must include complete order history
    """

    sample_edge_cases = """
    Boundary Conditions:
    - Zero-order state: customer with no orders clicks export

    Error/Failure Scenarios:
    - PDF generation service times out

    Security Concerns:
    - IDOR: attacker modifies userID to access another customer's PDF
    """

    output = generate_gherkin(sample_requirements, sample_edge_cases)
    print("\n\n===== GHERKIN OUTPUT =====")
    print(output)