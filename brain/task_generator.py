from agents.task import Task
from brain.goal_analyzer import GoalAnalysis


class DynamicTaskGenerator:
    """
    Industry-Level Dynamic Task Generator

    Creates task pipeline based on
    GoalAnalysis.
    """

    @staticmethod
    def generate(analysis: GoalAnalysis):

        tasks = []

        task_id = 1

        # -----------------------------
        # Research Task
        # -----------------------------
        if analysis.requires_research:

            tasks.append(
                Task(
                    id=task_id,
                    name="Research",
                    assigned_agent="ResearchAgent",
                    description=f"Research about: {analysis.goal}"
                )
            )

            task_id += 1

        # -----------------------------
        # Planning Task
        # -----------------------------
        tasks.append(
            Task(
                id=task_id,
                name="Planning",
                assigned_agent="PlannerAgent",
                description="Prepare execution plan"
            )
        )

        task_id += 1

        # -----------------------------
        # Writing Task
        # -----------------------------
        tasks.append(
            Task(
                id=task_id,
                name="Writing",
                assigned_agent="WriterAgent",
                description="Generate professional report"
            )
        )

        task_id += 1

        # -----------------------------
        # Review Task
        # -----------------------------
        if analysis.requires_review:

            tasks.append(
                Task(
                    id=task_id,
                    name="Review",
                    assigned_agent="CriticAgent",
                    description="Review report quality"
                )
            )

            task_id += 1

        # -----------------------------
        # Memory Task
        # -----------------------------
        if analysis.requires_memory:

            tasks.append(
                Task(
                    id=task_id,
                    name="Memory",
                    assigned_agent="MemoryAgent",
                    description="Store knowledge into memory"
                )
            )

        return tasks