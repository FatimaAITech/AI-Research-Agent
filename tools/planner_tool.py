from tools.base_tool import BaseTool


class PlannerTool(BaseTool):

    def __init__(self, planner):
        self.planner = planner

    @property
    def name(self):
        return "PLAN"

    @property
    def description(self):
        return "Creates a research plan."

    @property
    def version(self):
        return "1.0"

    @property
    def category(self):
        return "Planning"

    def run(self, state):
        return self.planner.run(state)