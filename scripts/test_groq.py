from services.groq_service import ask_groq

response = ask_groq(
    "Reply with exactly one word: WORKING"
)

print(response)