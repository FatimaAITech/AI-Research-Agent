import re


class MemoryReuseDecision:
    """
    Production-oriented Memory Reuse Decision Engine.

    Responsibilities:
    - Decide whether existing memory is safe to reuse
    - Prevent false semantic reuse
    - Remove duplicate memory candidates
    - Prefer exact topic matches
    - Require additional lexical evidence for semantic reuse
    """

    # Very high semantic similarity required
    REUSE_THRESHOLD = 0.95

    # Minimum lexical similarity required when
    # topic is not an exact match.
    LEXICAL_THRESHOLD = 0.50

    # -------------------------------------------------
    # Normalize Topic
    # -------------------------------------------------

    @staticmethod
    def normalize_topic(topic):

        if not topic:
            return ""

        topic = topic.lower().strip()

        # Remove punctuation
        topic = re.sub(r"[^a-z0-9\s]", " ", topic)

        # Remove extra spaces
        topic = re.sub(r"\s+", " ", topic)

        return topic.strip()

    # -------------------------------------------------
    # Tokenize Topic
    # -------------------------------------------------

    @staticmethod
    def tokenize(topic):

        normalized = MemoryReuseDecision.normalize_topic(topic)

        if not normalized:
            return set()

        return set(normalized.split())

    # -------------------------------------------------
    # Lexical Similarity
    # -------------------------------------------------

    @staticmethod
    def lexical_similarity(topic1, topic2):

        tokens1 = MemoryReuseDecision.tokenize(topic1)
        tokens2 = MemoryReuseDecision.tokenize(topic2)

        if not tokens1 or not tokens2:
            return 0.0

        intersection = tokens1.intersection(tokens2)

        union = tokens1.union(tokens2)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    # -------------------------------------------------
    # Exact Topic Match
    # -------------------------------------------------

    @staticmethod
    def exact_match(topic1, topic2):

        return (
            MemoryReuseDecision.normalize_topic(topic1)
            ==
            MemoryReuseDecision.normalize_topic(topic2)
        )

    # -------------------------------------------------
    # Remove Duplicate Candidates
    # -------------------------------------------------

    @classmethod
    def deduplicate_matches(cls, matches):

        unique = {}

        for item in matches:

            topic = item.get("topic", "")

            normalized = cls.normalize_topic(topic)

            if not normalized:
                continue

            score = float(
                item.get("score", 0)
            )

            # Keep highest-scoring version
            if (
                normalized not in unique
                or score > unique[normalized].get("score", 0)
            ):

                unique[normalized] = item

        return list(unique.values())

    # -------------------------------------------------
    # Decide
    # -------------------------------------------------

    @classmethod
    def decide(cls, matches, requested_topic=None):

        # ---------------------------------------------
        # No memories
        # ---------------------------------------------

        if not matches:

            return {
                "decision": "RESEARCH",
                "reason": "No relevant memory found.",
                "confidence": 0.0,
                "memory": None,
                "exact_match": False,
                "lexical_similarity": 0.0
            }

        # ---------------------------------------------
        # Remove duplicate candidates
        # ---------------------------------------------

        matches = cls.deduplicate_matches(matches)

        # ---------------------------------------------
        # If requested topic is missing,
        # use best semantic match.
        # ---------------------------------------------

        if requested_topic is None:

            best_match = max(
                matches,
                key=lambda item: item.get("score", 0)
            )

            score = float(
                best_match.get("score", 0)
            )

            if score >= cls.REUSE_THRESHOLD:

                return {
                    "decision": "REUSE",
                    "reason": "Very high similarity memory found.",
                    "confidence": score,
                    "memory": best_match,
                    "exact_match": False,
                    "lexical_similarity": 0.0
                }

            return {
                "decision": "RESEARCH",
                "reason": "Memory exists but similarity is below reuse threshold.",
                "confidence": score,
                "memory": best_match,
                "exact_match": False,
                "lexical_similarity": 0.0
            }

        # ---------------------------------------------
        # Find best candidate
        # ---------------------------------------------

        best_match = None
        best_score = -1

        for item in matches:

            topic = item.get("topic", "")

            score = float(
                item.get("score", 0)
            )

            # Exact topic match gets highest priority
            if cls.exact_match(
                requested_topic,
                topic
            ):

                best_match = item
                best_score = score

                break

            if score > best_score:

                best_score = score
                best_match = item

        # ---------------------------------------------
        # Exact Match = SAFE REUSE
        # ---------------------------------------------

        if best_match:

            memory_topic = best_match.get(
                "topic",
                ""
            )

            if cls.exact_match(
                requested_topic,
                memory_topic
            ):

                return {
                    "decision": "REUSE",
                    "reason": "Exact topic match found in memory.",
                    "confidence": max(
                        best_score,
                        1.0
                    ),
                    "memory": best_match,
                    "exact_match": True,
                    "lexical_similarity": 1.0
                }

        # ---------------------------------------------
        # Semantic + Lexical Validation
        # ---------------------------------------------

        if best_match:

            memory_topic = best_match.get(
                "topic",
                ""
            )

            semantic_score = float(
                best_match.get("score", 0)
            )

            lexical_score = cls.lexical_similarity(
                requested_topic,
                memory_topic
            )

            # -----------------------------------------
            # SAFE SEMANTIC REUSE
            # -----------------------------------------

            if (
                semantic_score >= cls.REUSE_THRESHOLD
                and
                lexical_score >= cls.LEXICAL_THRESHOLD
            ):

                return {
                    "decision": "REUSE",
                    "reason": (
                        "High semantic similarity confirmed "
                        "by lexical topic overlap."
                    ),
                    "confidence": semantic_score,
                    "memory": best_match,
                    "exact_match": False,
                    "lexical_similarity": lexical_score
                }

            # -----------------------------------------
            # FALSE REUSE PROTECTION
            # -----------------------------------------

            return {
                "decision": "RESEARCH",
                "reason": (
                    "Semantic similarity is insufficiently "
                    "supported by topic overlap."
                ),
                "confidence": semantic_score,
                "memory": best_match,
                "exact_match": False,
                "lexical_similarity": lexical_score
            }

        # ---------------------------------------------
        # Final fallback
        # ---------------------------------------------

        return {
            "decision": "RESEARCH",
            "reason": "No safe memory match found.",
            "confidence": 0.0,
            "memory": None,
            "exact_match": False,
            "lexical_similarity": 0.0
        }