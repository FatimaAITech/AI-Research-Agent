from tools.base_tool import BaseTool


class SearchTool(BaseTool):

    def __init__(self, researcher):
        self.researcher = researcher

    @property
    def name(self):
        return "SEARCH"
    
    @property
    def description(self):
        return "Searches the web and gathers research."

    @property
    def version(self):
        return "1.0"

    @property
    def category(self):
        return "Research"

    def run(self, state):
        return self.researcher.run(state)