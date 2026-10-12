import os
import ollama
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")


def ask_llm(prompt: str, system: str = "You are a helpful food and nutrition assistant.") -> str:
    """Send a prompt to the local Ollama model and return the text reply."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    print(ask_llm("Name three common foods that contain peanuts."))
