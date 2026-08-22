from agents.orchestrator import ResearchOrchestrator


class ResearchService:
    """
    Application service responsible for executing research workflows.

    This layer provides a clean boundary between external interfaces
    such as CLI/API clients and the internal research orchestration
    system.
    """

    def __init__(self, orchestrator=None):
        """
        Initialize the research service.

        Args:
            orchestrator: Optional ResearchOrchestrator instance.
                         If not provided, a new orchestrator is created.
        """

        self.orchestrator = orchestrator or ResearchOrchestrator()

    # -------------------------------------------------
    # Research Execution
    # -------------------------------------------------

    def run(self, topic):
        """
        Execute a complete research workflow.

        Args:
            topic: Research topic provided by the caller.

        Returns:
            AgentState returned by ResearchOrchestrator.

        Raises:
            ValueError: If the research topic is empty or invalid.
        """

        if not isinstance(topic, str):
            raise ValueError("Research topic must be a string.")

        topic = topic.strip()

        if not topic:
            raise ValueError("Research topic cannot be empty.")

        return self.orchestrator.run(topic)

    # -------------------------------------------------
    # Service Health
    # -------------------------------------------------

    def is_ready(self):
        """
        Check whether the research service is initialized.

        Returns:
            bool: True when the underlying orchestrator is available.
        """

        return self.orchestrator is not None