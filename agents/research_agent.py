from agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):

    def __init__(self, researcher):

        super().__init__("Research")

        self.researcher = researcher

    # -------------------------------------------------
    # Research Execution
    # -------------------------------------------------

    def run(self, state):

        self.log("Starting research...")

        # Existing ResearcherAgent already works with AgentState
        state = self.researcher.run(state)

        self.log("Research completed successfully.")

        return state