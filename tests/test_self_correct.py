from brain.self_correct import SelfCorrectAgent

agent = SelfCorrectAgent()

report = """
AI is computer intelligence.

It is used in many fields.

AI helps people.
"""

review = """
The report is too short.

Add applications.

Add advantages.

Improve formatting.

Improve conclusion.
"""

result = agent.correct(report, review)

print("\n========== IMPROVED REPORT ==========\n")
print(result)