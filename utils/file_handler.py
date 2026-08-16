import os
import re
import hashlib


class FileHandler:

    @staticmethod
    def save_report(topic, report):
        """
        Save AI research report as a Markdown file
        using a safe, bounded filename.
        """

        # Create reports folder if it doesn't exist
        os.makedirs("reports", exist_ok=True)

        # Clean topic for safe filename
        safe_topic = re.sub(r'[<>:"/\\|?*]', '', topic)
        safe_topic = re.sub(r'\s+', '_', safe_topic.strip())

        # Remove leading/trailing dots and underscores
        safe_topic = safe_topic.strip("._")

        # Fallback if topic becomes empty
        if not safe_topic:
            safe_topic = "research_report"

        # Keep filename safely bounded
        safe_topic = safe_topic[:80]

        # Add short unique hash to avoid filename collisions
        topic_hash = hashlib.sha256(
            topic.strip().lower().encode("utf-8")
        ).hexdigest()[:8]

        filename = f"{safe_topic}_{topic_hash}.md"

        filepath = os.path.join("reports", filename)

        # Save report
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(report)

        return filepath