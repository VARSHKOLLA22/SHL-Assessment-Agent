from services.gemini_service import ask_gemini

response = ask_gemini(
    "Reply with exactly one word: WORKING"
)

print(response)