from tools.tavily_tool import search


class ResearcherAgent:

    def research(self, topic):

        print("\n🔍 Researching Topic...")
        print(f"Topic: {topic}")

        response = search(topic)

        results = response.get("results", [])

        formatted_research = ""

        for index, item in enumerate(results, start=1):

            title = item.get("title", "")
            content = item.get("content", "")
            url = item.get("url", "")

            content = content.replace("\n", " ")
            content = " ".join(content.split())
            content = content[:300]

            formatted_research += f"""
===============================
Source {index}

Title:
{title}

Content:
{content}

URL:
{url}
===============================

"""

        return formatted_research
    
    def run(self, state):

        print("\n🔍 Researching...\n")

        state.research = self.research(state.topic)

        return state