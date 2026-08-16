import json
import os

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMemory:

    MODEL = SentenceTransformer("all-MiniLM-L6-v2")

    FILE_NAME = "memory/semantic_memory.json"

    # -----------------------------
    # Load Semantic Memory
    # -----------------------------
    @staticmethod
    def load():

        if not os.path.exists(SemanticMemory.FILE_NAME):
            return []

        with open(
            SemanticMemory.FILE_NAME,
            "r",
            encoding="utf-8"
        ) as f:

            try:
                return json.load(f)

            except Exception:
                return []

    # -----------------------------
    # Save Semantic Memory
    # -----------------------------
    @staticmethod
    def save(data):

        with open(
            SemanticMemory.FILE_NAME,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------
    # Cosine Similarity
    # -----------------------------
    @staticmethod
    def similarity(text1, text2):

        emb1 = SemanticMemory.MODEL.encode(text1)

        emb2 = SemanticMemory.MODEL.encode(text2)

        return float(
            cosine_similarity(
                [emb1],
                [emb2]
            )[0][0]
        )

    # -----------------------------
    # Search
    # -----------------------------
    @staticmethod
    def search(query, threshold=0.45):

        memories = SemanticMemory.load()

        results = []

        for item in memories:

            if not item.get("report"):
                  continue

            if len(item["report"].strip()) < 100:
                  continue
    
            score = SemanticMemory.similarity(
                query,
                item["topic"]
            )

            print(
                 f"{query}  <->  {item['topic']} = {round(score,3)}"
            )

            if score >= threshold:

                results.append({

                    "topic": item["topic"],

                    "report": item["report"],

                    "score": round(score, 4)
                })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results

    # -----------------------------
    # Add / Update Memory
    # -----------------------------
    @staticmethod
    def add_memory(topic, report):

        memories = SemanticMemory.load()

        for item in memories:

            if item["topic"].strip().lower() == topic.strip().lower():

                item["report"] = report

                SemanticMemory.save(memories)

                return

        memories.append({

            "topic": topic,

            "report": report

        })

        SemanticMemory.save(memories)

    # -----------------------------
    # Rebuild Memory
    # -----------------------------
    @staticmethod
    def rebuild():

        from memory.history import ResearchHistory

        history = ResearchHistory.load()

        memories = []

        for item in history:

            memories.append({

                "topic": item["topic"],

                "report": item["report"]

            })

        SemanticMemory.save(memories)

        print(
            f"✅ Semantic Memory rebuilt ({len(memories)} memories)"
        )