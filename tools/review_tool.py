from tools.base_tool import BaseTool


class ReviewTool(BaseTool):

    def __init__(self, reviewer):
        self.reviewer = reviewer

    @property
    def name(self):
        return "REVIEW"
    
    @property
    def description(self):
        return "Reviews the generated report."

    @property
    def version(self):
        return "1.0"

    @property
    def category(self):
        return "Review"

    def run(self, state):
        return self.reviewer.run(state)