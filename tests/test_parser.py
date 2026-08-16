from brain.parser import BrainParser

response = """
THOUGHT:
I need more information about HTML.

ACTION:
SEARCH
"""

result = BrainParser.parse(response)

print(result)
print()
print("Thought :", result["thought"])
print("Action  :", result["action"])