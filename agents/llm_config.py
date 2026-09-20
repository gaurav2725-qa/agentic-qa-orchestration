import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Switch this flag to change which provider all agents use
USE_LOCAL_OLLAMA = True


def get_llm():
    if USE_LOCAL_OLLAMA:
        return LLM(
            model="ollama/llama3.2",
            base_url="http://localhost:11434"
        )
    else:
        return LLM(
            model="gemini/gemini-3.6-flash",
            api_key=os.getenv("GEMINI_API_KEY")
        )