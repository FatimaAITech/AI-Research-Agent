from dataclasses import dataclass
from typing import Any
from time import time


@dataclass
class ToolResult:
    tool: str
    success: bool
    data: Any = None
    error: str = ""
    execution_time: float = 0.0

    @classmethod
    def success_result(cls, tool, data, execution_time):
        return cls(
            tool=tool,
            success=True,
            data=data,
            execution_time=execution_time
        )

    @classmethod
    def failure_result(cls, tool, error, execution_time):
        return cls(
            tool=tool,
            success=False,
            error=error,
            execution_time=execution_time
        )