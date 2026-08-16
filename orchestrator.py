from memory.history import ResearchHistory
from tools.llm import llm

from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent


class ResearchOrchestrator:

    def __init__(self):

        self.planner = PlannerAgent(llm)
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent(llm)
        self.reviewer = ReviewerAgent(llm)

    def run(self, topic):
        existing = ResearchHistory.exists(topic)

        if existing:

            print("\n⚠ Research already exists.\n")

            choice = input("Reuse old report? (y/n): ")

            if choice.lower() == "y":

                 print("\nReturning saved report...\n")


                 return {
                        "plan": "",
                        "research": "",
                        "report": existing["report"],
                        "review": "Loaded from Memory"
                           }

        print("\n========== PLANNER ==========\n")

        plan = self.planner.create_plan(topic)

        print(plan)


        print("\n========== RESEARCH ==========\n")

        research = self.researcher.research(topic)


        print("\n========== WRITER ==========\n")

        report = self.writer.write(
            topic=topic,
            plan=plan,
           research=research
        )


        print("\n========== REVIEWER ==========\n")

        review = self.reviewer.review(report)

 
        ResearchHistory.save(
         topic=topic,
         report=report,
         sources=[]
          )

        return {

            "plan": plan,
            "research": research,
            "report": report,
            "review": review

             }