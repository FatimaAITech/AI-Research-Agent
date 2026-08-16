from agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):

    def __init__(self, reviewer, reflector):

        super().__init__("Critic")

        self.reviewer = reviewer
        self.reflector = reflector

    # -------------------------------------------------
    # Review + Reflection
    # -------------------------------------------------

    def run(self, state):

        self.log("Reviewing report...")

        # Existing ReviewerAgent already works with AgentState
        state = self.reviewer.run(state)

        self.log("Running reflection...")

        reflection = self.reflector.reflect(
            goal=state.topic,
            observation=state.report
        )

        state.reflection = reflection

        self.log("Critic completed successfully.")

        return state