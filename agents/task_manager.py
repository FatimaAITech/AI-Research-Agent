from agents.task import Task


class TaskManager:
    """
    Industry-Level Task Manager

    Responsible for:
    - Creating tasks
    - Tracking task status
    - Returning pending/completed tasks
    """

    def __init__(self):

        self.tasks = []

        self.next_id = 1

    # ---------------------------------
    # Create Task
    # ---------------------------------

    def create_task(
        self,
        name,
        assigned_agent,
        description
    ):

        task = Task(
            id=self.next_id,
            name=name,
            assigned_agent=assigned_agent,
            description=description
        )

        self.tasks.append(task)

        self.next_id += 1

        return task

    # ---------------------------------
    # Get Pending Tasks
    # ---------------------------------

    def pending_tasks(self):

        return [
            task
            for task in self.tasks
            if task.status == "PENDING"
        ]

    # ---------------------------------
    # Get Completed Tasks
    # ---------------------------------

    def completed_tasks(self):

        return [
            task
            for task in self.tasks
            if task.status == "COMPLETED"
        ]

    # ---------------------------------
    # Find Task By ID
    # ---------------------------------

    def get_task(self, task_id):

        for task in self.tasks:

            if task.id == task_id:
                return task

        return None

    # ---------------------------------
    # Reset Manager
    # ---------------------------------

    def clear(self):

        self.tasks.clear()

        self.next_id = 1

    # ---------------------------------
    # Summary
    # ---------------------------------

    def summary(self):

        return {

            "total": len(self.tasks),

            "pending": len(self.pending_tasks()),

            "completed": len(self.completed_tasks())

        }