from tools.llm import llm
from agents.reviewer import ReviewerAgent

report = """

# AI

Artificial Intelligence is...

"""

reviewer = ReviewerAgent(llm)

result = reviewer.review(report)

print(result)