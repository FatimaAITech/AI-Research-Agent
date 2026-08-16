from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Task:
    """
    Industry-Level Task Object

    A single unit of work exchanged between agents.
    """

    id: int

    name: str

    assigned_agent: str

    description: str

    status: str = "PENDING"

    result: Any = None

    created_at: str = field(
        default_factory=lambda: datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    started_at: str | None = None

    completed_at: str | None = None

    # ---------------------------------
    # Task Lifecycle
    # ---------------------------------

    def start(self):

        self.status = "RUNNING"

        self.started_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def complete(self, result=None):

        self.status = "COMPLETED"

        self.result = result

        self.completed_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def fail(self, error):

        self.status = "FAILED"

        self.result = str(error)

        self.completed_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    # ---------------------------------
    # Serialization
    # ---------------------------------

    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "assigned_agent": self.assigned_agent,

            "description": self.description,

            "status": self.status,

            "result": self.result,

            "created_at": self.created_at,

            "started_at": self.started_at,

            "completed_at": self.completed_at

        }