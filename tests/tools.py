import time
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")


class SearchTool:

    def __init__(self):
        self.client = TavilyClient(api_key=tavily_api_key)

    def search(self, query):

     for attempt in range(3):
        try:
            result = self.client.search(
                query=query,
                search_depth="basic",
                max_results=5
            )
            return result

        except Exception as e:
            print(f"Search failed (Attempt {attempt+1}/3): {e}")

            if attempt < 2:
                print("Retrying in 2 seconds...")
                time.sleep(2)
 
     raise Exception("Unable to connect to Tavily after 3 attempts.")
    
 