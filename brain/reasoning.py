from tools.llm import ask


class AgentBrain:

    def think(self, goal, context=""):

        print("\n🧠 Agent Thinking...\n")

        prompt = f"""
You are the reasoning engine of an AI Research Agent.

Think step by step.

Goal:
{goal}

Current Context:
{context}

Return your answer EXACTLY in this format:

THOUGHT:
<your reasoning>

ACTION:
SEARCH

OR

ACTION:
WRITE

OR

ACTION:
REVIEW

OR

ACTION:
FINISH

Do not return anything else.
"""
    
        response = ask(prompt)

        return response 