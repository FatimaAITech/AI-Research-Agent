from brain.reflection import ReflectionAgent

reflection = ReflectionAgent()

goal = "Physics"

observation = """
Physics is the study of matter,
energy, force and motion.
"""

result = reflection.reflect(
    goal,
    observation
)

print("\nDecision:\n")
print(result)