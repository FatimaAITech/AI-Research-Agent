import json
import os
from datetime import datetime
# from memory.consolidation import MemoryConsolidator
# from memory.consolidation import MemoryConsolidator
class ResearchHistory:

    FILE_NAME = "memory/history.json"

    @staticmethod
    def save(topic, report, sources):

        data = []

        if os.path.exists(ResearchHistory.FILE_NAME):
         with open(ResearchHistory.FILE_NAME, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = []

        found = False

        for item in data:
           if item["topic"].strip().lower() == topic.strip().lower():
            item["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["report"] = report
            item["sources"] = sources
            found = True
            break

        if not found:
          data.append({
            "topic": topic,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "report": report,
            "sources": sources
        })

        with open(ResearchHistory.FILE_NAME, "w", encoding="utf-8") as f:
             json.dump(
                  data,
                  f,
                  indent=4,
                  ensure_ascii=False
            )
        # MemoryConsolidator.consolidate()
    @staticmethod
    def load():

        if not os.path.exists(ResearchHistory.FILE_NAME):
            return []

        with open(ResearchHistory.FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
        
    @staticmethod
    def exists(topic):

        data = ResearchHistory.load()

        for item in data:
            if item["topic"].strip().lower() == topic.strip().lower():            return item

    @staticmethod
    def write(data):

        with open(
               ResearchHistory.FILE_NAME,
               "w",
               encoding="utf-8"
        ) as f:

              json.dump(
                   data,
                   f,
                   indent=4,
                   ensure_ascii=False
              )

        return None    