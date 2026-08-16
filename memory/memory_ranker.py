class MemoryRanker:
    """
    Responsible for ranking memory search results.

    Future Ranking Factors:
    - Semantic Similarity
    - Usage Frequency
    - Recency
    - Importance
    - User Preference
    """

    @staticmethod
    def rank(matches):
        """
        Rank memories by similarity score.
        """

        if not matches:
            return []

        ranked = sorted(
            matches,
            key=lambda item: item["score"],
            reverse=True
        )

        return ranked

    @staticmethod
    def best_match(matches):
        """
        Return highest ranked memory.
        """

        ranked = MemoryRanker.rank(matches)

        if not ranked:
            return None

        return ranked[0]