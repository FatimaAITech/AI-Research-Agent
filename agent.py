from memory.history import ResearchHistory
from utils.planner import ResearchPlanner
from utils.formatter import SearchFormatter
from dotenv import load_dotenv
import os
from utils.source_handler import SourceHandler
from langchain_groq import ChatGroq
from tools import SearchTool
from prompts.research_prompt import ResearchPrompt
from tools.metrics import Metrics

# Load environment variables
load_dotenv()

# Get Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")


class ResearchAgent:

    def __init__(self):
        # Initialize LLM
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile"
        )

        # Initialize Search Tool
        self.search_tool = SearchTool()

    def research(self, topic):

        # Search from Internet
        search_results = self.search_tool.search(topic)
        sources = SourceHandler.get_sources(search_results)
        formatted_results = SearchFormatter.format_results(search_results)
        plan_prompt = ResearchPlanner.create_plan(topic)

        plan = self.llm.invoke(plan_prompt).content

        print("\n========== RESEARCH PLAN ==========\n")
        print(plan)

        # Create Prompt
        prompt = ResearchPrompt.create(topic, formatted_results)
        # Generate AI Response
        response = self.llm.invoke(prompt)

        report = response.content

        report += "\n\n====================\n"
        report += "Sources\n\n"

        for index, source in enumerate(sources, start=1):
            report += f"{index}. {source}\n"

         # Save report into memory
            ResearchHistory.save(
            topic=topic,
            report=report,
            sources=sources
)
        return report