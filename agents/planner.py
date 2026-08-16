# from langchain_groq import ChatGroq
from prompts.planner_prompt import planner_prompt


class PlannerAgent:

    def __init__(self, llm):
        self.llm = llm

    def run(self, state):

        print("\n📋 Planning...\n")

        prompt = planner_prompt(state.topic)

        response = self.llm.invoke(prompt)

        state.plan = response.content

        return state