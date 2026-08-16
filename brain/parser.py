import re


class BrainParser:

    @staticmethod
    def parse(response: str):
        """
        Parse the LLM response into structured data.
        """

        thought = ""
        action = "FINISH"

        thought_match = re.search(
            r"THOUGHT:\s*(.*?)\s*ACTION:",
            response,
            re.DOTALL | re.IGNORECASE
        )

        if thought_match:
            thought = thought_match.group(1).strip()

        action_match = re.search(
            r"ACTION:\s*(\w+)",
            response,
            re.IGNORECASE
        )

        if action_match:
            action = action_match.group(1).strip().upper()

        return {
            "thought": thought,
            "action": action
        }