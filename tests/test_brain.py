from brain.reasoning import AgentBrain

brain = AgentBrain()

goal = input("Enter Goal: ")

decision = brain.think(goal)

print("\nDecision:\n")
print(decision)