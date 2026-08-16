class ResearchPrompt:

    @staticmethod
    def create(topic, search_results):

        return f"""
You are an expert AI Research Assistant.

Your task is to create a professional research report.

Research Topic:
{topic}

Search Results:
{search_results}

Instructions:

1. Write in simple English.
2. Give a proper Introduction.
3. Explain important concepts.
4. Add Key Findings.
5. Mention Important Facts.
6. End with a Conclusion.
7. Make the report easy to understand.
8. Use headings.
"""