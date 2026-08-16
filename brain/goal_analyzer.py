from dataclasses import dataclass


@dataclass
class GoalAnalysis:

    goal: str

    category: str

    complexity: str

    estimated_tasks: int

    requires_research: bool

    requires_memory: bool

    requires_review: bool


class GoalAnalyzer:

    """
    Industry-Level Goal Analyzer

    Responsible for:
    - Understanding user goals
    - Estimating complexity
    - Planning execution strategy
    """

    @staticmethod
    def analyze(goal: str):

        text = goal.lower()

        research_keywords = [
            "research",
            "compare",
            "analysis",
            "latest",
            "study",
            "future",
            "report"
        ]

        coding_keywords = [
            "python",
            "code",
            "program",
            "api",
            "agent"
        ]

        if any(word in text for word in coding_keywords):
            category = "CODING"

        elif any(word in text for word in research_keywords):
            category = "RESEARCH"

        else:
            category = "GENERAL"

        word_count = len(goal.split())

        if word_count <= 4:
            complexity = "LOW"

        elif word_count <= 10:
            complexity = "MEDIUM"

        else:
            complexity = "HIGH"

        estimated_tasks = {
            "LOW": 3,
            "MEDIUM": 5,
            "HIGH": 7
        }[complexity]

        return GoalAnalysis(
            goal=goal,
            category=category,
            complexity=complexity,
            estimated_tasks=estimated_tasks,
            requires_research=True,
            requires_memory=True,
            requires_review=True
        )