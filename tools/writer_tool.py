from tools.base_tool import BaseTool


class WriterTool(BaseTool):

    def __init__(self, writer):
        self.writer = writer

    @property
    def name(self):
        return "WRITE"
    
    @property
    def description(self):
        return "Writes a professional report."

    @property
    def version(self):
        return "1.0"

    @property
    def category(self):
        return "Writing"

    def run(self, state):
        return self.writer.run(state)