from difflib import SequenceMatcher
from memory.history import ResearchHistory


class MemorySearch:

    @staticmethod
    def similarity(a, b):
        return SequenceMatcher(
            None,
            a.lower(),
            b.lower()
        ).ratio()

    @classmethod
    def search(cls, query, threshold=0.60):

        history = ResearchHistory.load()

        matches = []

        for item in history:

            score = cls.similarity(
                query,
                item["topic"]
            )

            if score >= threshold:

                matches.append({
                    "topic": item["topic"],
                    "score": round(score, 2),
                    "report": item["report"],
                    "sources": item["sources"]
                })

        matches.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return matches