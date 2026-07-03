from services.agent import SHLAgent

# Create the agent
agent = SHLAgent()

print("=" * 60)
print("TEST 1 - Vague Query")
print("=" * 60)

response = agent.reply("I need an assessment")

print(response)

print("\n")

print("=" * 60)
print("TEST 2 - Specific Query")
print("=" * 60)

response = agent.reply("I am hiring a Java Developer")

print(response)