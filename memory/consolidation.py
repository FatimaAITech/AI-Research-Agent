from memory.history import ResearchHistory
from memory.semantic_memory import SemanticMemory


class MemoryConsolidator:

    @staticmethod
    def consolidate(threshold=0.90):

        history = ResearchHistory.load()

        if not history:
            return

        consolidated = []

        for item in history:

            merged = False

            for existing in consolidated:

                score = SemanticMemory.similarity(
                    item["topic"],
                    existing["topic"]
                )

                if score >= threshold:

                    # Keep longer report
                    if len(item["report"]) > len(existing["report"]):
                        existing["report"] = item["report"]

                    # Merge access count
                    existing["access_count"] = (
                        existing.get("access_count", 1)
                        + item.get("access_count", 1)
                    )

                    # Keep latest access
                    if item.get("last_access", "") > existing.get("last_access", ""):
                        existing["last_access"] = item["last_access"]

                    merged = True
                    break

            if not merged:
                consolidated.append(item)

        ResearchHistory.write(consolidated)