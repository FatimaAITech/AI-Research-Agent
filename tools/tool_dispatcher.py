from time import time

from tools.metrics import Metrics
from tools.tool_result import ToolResult
from tools.tool_validator import ToolValidator
from tools.retry import Retry
from tools.logger import Logger
from tools.tool_exceptions import (
    ValidationError,
    APIError,
    NetworkError,
    ToolError
)

class ToolDispatcher:

    def __init__(self, registry):

        self.registry = registry
        self.validator = ToolValidator()
        self.retry = Retry()

    def execute(self, action, state):

        start = time()

        tool = self.registry.get(action)

        if tool is None:

            elapsed = time() - start

            Logger.log(
                f"UNKNOWN TOOL -> {action}"
            )

            return ToolResult.failure_result(
                tool=action,
                error=f"Unknown Tool: {action}",
                execution_time=elapsed
            )

        self.validator.validate(tool, state)

        print(f"\n🚀 Dispatching Tool: {action}")

        Logger.log(
            f"START -> {action}"
        )

        try:

            new_state = self.retry.execute(
                 tool.run,
                  state
            )

            elapsed = time() - start

            Logger.log(
                  f"SUCCESS -> {action} ({elapsed:.2f}s)"
        )
            
            Metrics.record(
                 tool_name=action,
                 success=True,
                 execution_time=elapsed
            )

            return ToolResult.success_result(
               tool=action,
               data=new_state,
               execution_time=elapsed
        )


        except ValidationError as e:

            elapsed = time() - start

            Metrics.record(
                tool_name=action,
                success=False,
                execution_time=elapsed
            )

            Logger.log(
               f"VALIDATION ERROR -> {action}: {e}"
        )

            return ToolResult.failure_result(
                tool=action,
                error=str(e),
                execution_time=elapsed
        )


        except (APIError, NetworkError) as e:

            elapsed = time() - start

            Metrics.record(
                tool_name=action,
                success=False,
                execution_time=elapsed
        )

            Logger.log(
                f"RETRYABLE ERROR -> {action}: {e}"
        )

            return ToolResult.failure_result(
                tool=action,
                error=str(e),
                execution_time=elapsed
        )


        except ToolError as e:

             elapsed = time() - start

             Metrics.record(
                tool_name=action,
                success=False,
                execution_time=elapsed
            )

             Logger.log(
                  f"TOOL ERROR -> {action}: {e}"
        )

             return ToolResult.failure_result(
                 tool=action,
                 error=str(e),
                 execution_time=elapsed
        )


        except Exception as e:

             elapsed = time() - start

             Metrics.record(
                 tool_name=action,
                 success=False,
                 execution_time=elapsed
            )

             Logger.log(
                  f"UNKNOWN ERROR -> {action}: {e}"
        )

             return ToolResult.failure_result(
                tool=action,
                error=str(e),
                execution_time=elapsed
        )