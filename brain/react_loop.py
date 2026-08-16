from brain.reasoning import AgentBrain

from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent

from tools.llm import llm
 

class ReActLoop:

    def __init__(self):

        self.brain = AgentBrain()

        self.researcher = ResearcherAgent()

        self.writer = WriterAgent()

        self.reviewer = ReviewerAgent(llm)

    def next_action(self, goal, context=""):

        response = self.brain.think(goal, context)

        print("\n========== AGENT THINKING ==========\n")
        print(response)

        decision = response.upper()

    # ---------------- SEARCH ---------------- #

        if "SEARCH" in decision:

            print("\n🚀 Executing Research Tool...\n")

            research = self.researcher.research(goal)

            return {
            "action": "SEARCH",
            "observation": research
        }

    # ---------------- WRITE ---------------- #

        elif "WRITE" in decision:

            print("\n📝 Executing Writer...\n")

            report = self.writer.write(
            topic=goal,
            plan="",
            research=context
        )

            return {
            "action": "WRITE",
            "observation": report
        }

    # ---------------- REVIEW ---------------- #

        elif "REVIEW" in decision:

            print("\n📋 Executing Reviewer...\n")

            reviewed = self.reviewer.review(context)

            return {
            "action": "REVIEW",
            "observation": reviewed
        }

    # ---------------- FINISH ---------------- #

        else:

             return {
             "action": "FINISH",
            "observation": context
        }