from brain.task_queue import TaskQueue

class AutonomousScheduler:
    """
    Industry-Level Autonomous Scheduler

    Responsible for:
    - Managing task execution order
    - Supporting future priorities
    - Supporting future parallel execution
    """

    def __init__(self):

        from agents.parallel_executor import ParallelExecutor

        self.queue = TaskQueue()

        self.parallel = ParallelExecutor()
    # ---------------------------------
    # Load Tasks
    # ---------------------------------
    def load_tasks(self, tasks):

        self.queue.clear()

        self.queue.extend(tasks)
    # ---------------------------------
    # Get Next Task
    # ---------------------------------
    def next_task(self):

        return self.queue.next_task()


    def pop(self):

        task = self.queue.next_task()

        if task:

           print(f"\n📌 Scheduled -> {task.name}")

        return task
    # ---------------------------------
    # Remaining Tasks
    # ---------------------------------
    def remaining_tasks(self):

        return self.queue.size()
    # ---------------------------------
    # Has Work?
    # ---------------------------------
    def has_tasks(self):

        return not self.queue.empty()

    # ---------------------------------
    # Preview Queue
    # ---------------------------------

    def preview(self):

        return self.queue.tasks()

    def statistics(self):

        return {

            "remaining": self.remaining_tasks(),

            "queued": len(self.preview())

        }

    # ---------------------------------
    # Reset Scheduler
    # ---------------------------------

    def reset(self):

        self.queue.clear()

    # ---------------------------------
# Parallel Execution
# ---------------------------------

    def run_parallel(self, functions):

        print("\n========== PARALLEL EXECUTION ==========\n")

        return self.parallel.run(functions)    