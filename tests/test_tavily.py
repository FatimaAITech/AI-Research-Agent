from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

print("API Loaded:", api_key is not None)

client = TavilyClient(api_key=api_key)

result = client.search("Artificial Intelligence")

print(result)