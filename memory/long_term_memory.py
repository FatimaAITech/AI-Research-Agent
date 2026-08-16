import json
from datetime import datetime

from memory.history import ResearchHistory


class LongTermMemory:

    @staticmethod
    def touch(topic):

        history = ResearchHistory.load()

        updated = False

        for item in history:

            if item["topic"].strip().lower() == topic.strip().lower():

                item["last_access"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                item["access_count"] = item.get(
                    "access_count",
                    0
                ) + 1

                updated = True
                break

        if updated:

            with open(
                ResearchHistory.FILE_NAME,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    history,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

        return updated

    @staticmethod
    def statistics():

        history = ResearchHistory.load()

        return {
            "total_memories": len(history),
            "total_reuses": sum(
                item.get("access_count", 0)
                for item in history
            )
        }

    @staticmethod
    def most_used(limit=5):

        history = ResearchHistory.load()

        return sorted(
            history,
            key=lambda x: x.get(
                "access_count",
                0
            ),
            reverse=True
        )[:limit]