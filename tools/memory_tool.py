from tools.base_tool import BaseTool

from memory.history import ResearchHistory
from memory.semantic_memory import SemanticMemory
from memory.long_term_memory import LongTermMemory
from memory.consolidation import MemoryConsolidator


class MemoryTool(BaseTool):

    @property
    def name(self):
        return "MEMORY"

    @property
    def description(self):
        return "Complete Memory Pipeline"

    @property
    def version(self):
        return "2.0"

    @property
    def category(self):
        return "Memory"

    def run(self, state):

        print("\n🧠 MEMORY PIPELINE STARTED\n")

        report = state.final_report or state.report

        # ---------------------------------
        # 1. Save Research History
        # ---------------------------------

        ResearchHistory.save(
            topic=state.topic,
            report=report,
            sources=[]
        )

        print("✅ Research History Updated")

        # ---------------------------------
        # 2. Save Semantic Memory
        # ---------------------------------

        SemanticMemory.add_memory(
            topic=state.topic,
            report=report
        )

        print("✅ Semantic Memory Updated")

        # ---------------------------------
        # 3. Update Long-Term Memory
        # ---------------------------------

        LongTermMemory.touch(
            state.topic
        )

        print("✅ Long-Term Memory Updated")

        # ---------------------------------
        # 4. Memory Consolidation
        # ---------------------------------

        MemoryConsolidator.consolidate()

        print("✅ Memory Consolidated")

        print("\n🧠 MEMORY PIPELINE COMPLETED\n")

        return state