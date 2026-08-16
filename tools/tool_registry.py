class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool):
        """
        Register a tool.
        """
        self.tools[tool.name] = tool

    def get(self, name):
        """
        Get tool by name.
        """
        return self.tools.get(name)

    def exists(self, name):
        """
        Check if tool exists.
        """
        return name in self.tools

    def list_tools(self):
        """
        Return all registered tool names.
        """
        return list(self.tools.keys())

    def tool_info(self):
        """
        Return metadata for all registered tools.
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "version": tool.version,
                "category": tool.category,
            }
            for tool in self.tools.values()
        ]