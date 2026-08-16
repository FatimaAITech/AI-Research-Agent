from agents.researcher import ResearcherAgent

topic = input("Enter Topic: ")

researcher = ResearcherAgent()

results = researcher.research(topic)

print("\n========== SEARCH RESULTS ==========\n")
print(results)