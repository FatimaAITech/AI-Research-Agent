from agents.base_agent import BaseAgent


class WriterAgent(BaseAgent):

    def __init__(self, writer):

        super().__init__("Writer")

        self.writer = writer

    # -------------------------------------------------
    # Report Generation
    # -------------------------------------------------

    def run(self, state):

        self.log("Generating professional report...")

        # Existing WriterAgent already works with AgentState
        state = self.writer.run(state)

        self.log("Professional report generated successfully.")

        return state