from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent

topic = input("Enter Topic: ")

research = ResearcherAgent.research(topic)

report = WriterAgent.write(topic, research)

print("\n========== REPORT ==========\n")

print(report)