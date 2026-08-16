from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):

    def __init__(self, planner):

        super().__init__("Planner")

        self.planner = planner

    # -------------------------------------------------
    # Planner Execution
    # -------------------------------------------------

    def run(self, state):

        self.log("Generating research plan...")

        # Existing PlannerAgent already works with AgentState
        state = self.planner.run(state)

        self.log("Research plan generated successfully.")

        return state