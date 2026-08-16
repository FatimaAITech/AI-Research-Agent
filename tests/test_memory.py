from memory.history import ResearchHistory

ResearchHistory.save(
    topic="Python",
    report="Python is a programming language.",
    sources=["https://python.org"]
)

print(ResearchHistory.load())