from tools.llm import ask


class ReflectionAgent:

    def reflect(self, goal, observation):

        print("\n🤔 Reflecting...\n")

        prompt = f"""
You are an AI Reflection Agent.

Goal:
{goal}

Current Output:
{observation}

Decide the NEXT action.

Rules:

- If information is missing → SEARCH
- If research exists but report is missing → WRITE
- If report exists but has not been reviewed → REVIEW
- If review found mistakes → SELF_CORRECT
- If everything looks complete → FINISH

Return ONLY ONE WORD.

SEARCH
WRITE
REVIEW
SELF_CORRECT
FINISH
"""

        response = ask(prompt)

        return response.strip()