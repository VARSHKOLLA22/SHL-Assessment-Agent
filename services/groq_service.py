import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def ask_groq(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise assistant. "
                        "Follow the user's instructions exactly. "
                        "If asked to return JSON, return ONLY valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
            top_p=1,
            max_tokens=1024,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM_ERROR: {e}"