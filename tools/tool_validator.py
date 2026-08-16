from tools.tool_exceptions import ValidationError


class ToolValidator:

    def validate(self, tool, state):

        if tool is None:
            raise ValidationError("Tool does not exist.")

        if state is None:
            raise ValidationError("State cannot be None.")

        if not hasattr(tool, "run"):
            raise ValidationError(
                f"{tool.__class__.__name__} has no run() method."
            )

        return True