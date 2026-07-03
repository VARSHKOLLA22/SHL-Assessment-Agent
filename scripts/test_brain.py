from services.agent_brain import AgentBrain

brain = AgentBrain()

messages = [
    {
        "role": "user",
        "content": "I am hiring a Java developer."
    }
]

result = brain.decide(messages)

print("RESULT repr:", repr(result))
print("RESULT:", result)