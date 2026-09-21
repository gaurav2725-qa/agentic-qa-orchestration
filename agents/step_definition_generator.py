import os
from dotenv import load_dotenv
from agents.llm_config import get_llm
from crewai import Agent, Task, Crew

load_dotenv()

llm = get_llm()

# Known, real element locators for the target page —
# provided directly rather than letting the agent guess,
# since guessing against a real page it cannot see would
# be genuinely unreliable
PAGE_ELEMENTS = """
Known element locators for https://the-internet.herokuapp.com/login:
- Username field: By.ID, "username"
- Password field: By.ID, "password"
- Login button: By.CSS_SELECTOR, "button[type='submit']"
- Success message (after login): By.CSS_SELECTOR, ".flash.success"
- Error message (after failed login): By.CSS_SELECTOR, ".flash.error"
- Secure area URL contains: "/secure"
"""

step_definition_writer = Agent(
    role="SDET Automation Engineer",
    goal="Write precise, executable Python Selenium step "
         "definitions for a single Gherkin scenario",
    backstory=(
        "You are an experienced SDET who writes clean, "
        "reliable Selenium WebDriver code using the behave "
        "framework's step definition pattern. You always use "
        "context.driver for the WebDriver instance, use "
        "explicit waits where appropriate, and write code that "
        "matches the EXACT step text it implements, character "
        "for character, so behave's step matcher can find it."
    ),
    llm=llm,
    verbose=True
)


def generate_step_definitions(scenario_text):
    task = Task(
        description=(
            "Below is a single Gherkin scenario. Write Python "
            "step definitions (using the behave framework's "
            "@given/@when/@then decorators) that implement "
            "EVERY step in this scenario.\n\n"
            + PAGE_ELEMENTS +
            "\n\nSTRICT RULES:\n"
            "- Do NOT include any import statements — assume "
            "'from behave import given, when, then' and "
            "'from selenium.webdriver.common.by import By' "
            "already exist\n"
            "- Do NOT wrap output in markdown code fences "
            "(no ``` anywhere)\n"
            "- Do NOT add any commentary before or after the "
            "code\n"
            "- Use context.driver for all WebDriver actions\n"
            "- The @given/@when/@then decorator string must "
            "match the scenario's step text EXACTLY, including "
            "quoted values inside the step\n"
            "- Only use By.ID, By.NAME, By.CSS_SELECTOR, or "
            "By.XPATH as locator strategies\n"
            "- If a step's action doesn't map cleanly to any "
            "real element from the list above, write a "
            "'pass' statement as the function body instead "
            "of guessing at a nonexistent element\n\n"
            "Gherkin Scenario:\n" + scenario_text
        ),
        expected_output=(
            "Raw Python code containing only @given/@when/@then "
            "decorated functions, no imports, no markdown "
            "fences, no commentary."
        ),
        agent=step_definition_writer
    )

    crew = Crew(
        agents=[step_definition_writer],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    clean_result = str(result).replace("```python", "").replace("```", "").strip()

    return clean_result


if __name__ == "__main__":
    sample_scenario = """
Scenario: Successful Login with Valid Credentials
  Given user "tomsmith" logged in with password "SuperSecretPassword!"
  When login button is clicked
  Then redirect to secure area and success message is displayed
"""

    output = generate_step_definitions(sample_scenario)
    print("\n\n===== GENERATED STEP DEFINITIONS =====")
    print(output)