from tools.base_tool import BaseTool


class SelfCorrectTool(BaseTool):

    def __init__(self, self_corrector):
        self.self_corrector = self_corrector

    @property
    def name(self):
        return "SELF_CORRECT"
    
    @property
    def description(self):
       return "Improves the report using review feedback."

    @property
    def version(self):
       return "1.0"

    @property
    def category(self):
       return "Correction"

    def run(self, state):
        return self.self_corrector.run(state)