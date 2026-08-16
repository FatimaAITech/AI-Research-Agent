class ResearchPlanner:

    @staticmethod
    def create_plan(topic):

        return f"""
You are an AI Research Planner.

Create a research outline for this topic.

Topic:
{topic}

Generate only the headings.

Example:

1. Introduction
2. Definition
3. History
4. Types
5. Advantages
6. Disadvantages
7. Applications
8. Future Scope
9. Conclusion

Do not explain anything.
Only return the outline.
"""