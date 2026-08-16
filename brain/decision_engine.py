from brain.goal_analyzer import GoalAnalyzer


class DecisionEngine:
    """
    Industry-Level Decision Engine

    Responsible for:
    - Deciding execution strategy
    - Selecting workflow
    - Future autonomous reasoning
    """

    @staticmethod
    def decide(goal):

        analysis = GoalAnalyzer.analyze(goal)

        strategy = {

            "analysis": analysis,

            "use_memory": analysis.requires_memory,

            "do_research": analysis.requires_research,

            "review_output": analysis.requires_review,

            "parallel_execution": (
                analysis.complexity == "HIGH"
            ),

            "retry_enabled": True,

            "max_iterations": {

                "LOW": 2,

                "MEDIUM": 4,

                "HIGH": 6

            }[analysis.complexity]

        }

        return strategy