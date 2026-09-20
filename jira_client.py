import os
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_SITE_URL = os.getenv("JIRA_SITE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


def fetch_jira_ticket(ticket_key):
    if not all([JIRA_SITE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
        raise ValueError("Missing Jira config in .env")

    url = JIRA_SITE_URL + "/rest/api/3/issue/" + ticket_key

    response = requests.get(
        url,
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Accept": "application/json"}
    )

    if response.status_code != 200:
        raise RuntimeError(
            "Jira API error " + str(response.status_code)
            + ": " + response.text
        )

    data = response.json()
    fields = data["fields"]

    summary = fields.get("summary", "")
    description_raw = fields.get("description")

    description_text = extract_text_from_adf(description_raw)

    result = {}
    result["key"] = ticket_key
    result["summary"] = summary
    result["description"] = description_text
    return result


def extract_text_from_adf(adf_content):
    if not adf_content:
        return ""

    text_parts = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "text":
                text_parts.append(node.get("text", ""))
            for child in node.get("content", []):
                walk(child)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(adf_content)
    return " ".join(text_parts)


if __name__ == "__main__":
    ticket_key = input("Enter Jira ticket key (e.g. PROJ-1): ")
    ticket = fetch_jira_ticket(ticket_key)

    print("")
    print("Key: " + ticket["key"])
    print("Summary: " + ticket["summary"])
    print("Description: " + ticket["description"])