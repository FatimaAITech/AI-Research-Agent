from brain.react_loop import ReActLoop

loop = ReActLoop()

goal = input("Enter Goal: ")

result = loop.next_action(goal)

print("\n========== RESULT ==========\n")

print("Action:")
print(result["action"])

print("\nObservation:\n")
print(result["observation"])