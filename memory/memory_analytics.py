from datetime import datetime

from memory.history import ResearchHistory


class MemoryAnalytics:

    @staticmethod
    def summary():

        history = ResearchHistory.load()

        total_memories = len(history)

        total_reuses = sum(
            item.get("access_count", 0)
            for item in history
        )

        average_access = (
            total_reuses / total_memories
            if total_memories
            else 0
        )

        return {
            "total_memories": total_memories,
            "total_reuses": total_reuses,
            "average_access": round(average_access, 2)
        }

    @staticmethod
    def most_used(limit=5):

        history = ResearchHistory.load()

        return sorted(
            history,
            key=lambda x: x.get("access_count", 0),
            reverse=True
        )[:limit]

    @staticmethod
    def recently_accessed(limit=5):

        history = ResearchHistory.load()

        history = sorted(
            history,
            key=lambda x: x.get("last_access", ""),
            reverse=True
        )

        return history[:limit]

    @staticmethod
    def oldest(limit=5):

        history = ResearchHistory.load()

        def get_time(item):

            value = item.get("time")

            if not value:
                return datetime.max

            return datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

        history = sorted(
            history,
            key=get_time
        )

        return history[:limit]

    @staticmethod
    def report():

        print("\n========== MEMORY ANALYTICS ==========\n")

        summary = MemoryAnalytics.summary()

        print(f"📚 Total Memories : {summary['total_memories']}")
        print(f"🔁 Total Reuses   : {summary['total_reuses']}")
        print(f"📊 Average Access : {summary['average_access']}")

        print("\n🏆 MOST USED TOPICS\n")

        for item in MemoryAnalytics.most_used():

            print(
                f"- {item['topic']} "
                f"(Used {item.get('access_count', 0)} times)"
            )

        print("\n🕒 RECENTLY ACCESSED\n")

        for item in MemoryAnalytics.recently_accessed():

            print(
                f"- {item['topic']} "
                f"({item.get('last_access', 'Never')})"
            )

        print("\n📜 OLDEST MEMORIES\n")

        for item in MemoryAnalytics.oldest():

            print(
                f"- {item['topic']} "
                f"({item.get('time', '-')})"
            )

        print("\n========== END OF MEMORY ANALYTICS ==========\n")