class ToolError(Exception):
    """Base Tool Error"""
    pass


class ValidationError(ToolError):
    """Validation failed"""
    pass


class APIError(ToolError):
    """LLM/API Error"""
    pass


class MemoryError(ToolError):
    """Memory Error"""
    pass


class NetworkError(ToolError):
    """Internet Error"""
    pass


class PlannerError(ToolError):
    """Planner Error"""
    pass


class ResearchError(ToolError):
    """Research Error"""
    pass


class WriterError(ToolError):
    """Writer Error"""
    pass


class ReviewError(ToolError):
    """Review Error"""
    pass