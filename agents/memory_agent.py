from agents.base_agent import BaseAgent

from memory.history import ResearchHistory
from memory.semantic_memory import SemanticMemory
from memory.consolidation import MemoryConsolidator


class MemoryAgent(BaseAgent):

    def __init__(self):

        super().__init__("Memory")

    # -------------------------------------------------
    # Complete Memory Lifecycle
    # -------------------------------------------------

    def run(self, state):

        self.log("Updating research history...")

        report = state.final_report or state.report

        # ---------------------------------------------
        # 1. Long-Term Research History
        # ---------------------------------------------

        ResearchHistory.save(
            topic=state.topic,
            report=report,
            sources=[]
        )

        self.log("Research history updated.")

        # ---------------------------------------------
        # 2. Semantic Memory
        # ---------------------------------------------

        self.log("Updating semantic memory...")

        SemanticMemory.add_memory(
            state.topic,
            report
        )

        self.log("Semantic memory updated.")

        # ---------------------------------------------
        # 3. Memory Consolidation
        # ---------------------------------------------

        self.log("Running memory consolidation...")

        MemoryConsolidator.consolidate()

        self.log("Memory consolidation completed.")

        # ---------------------------------------------
        # 4. Pipeline Complete
        # ---------------------------------------------

        self.log(
            "Memory lifecycle completed successfully."
        )

        return state