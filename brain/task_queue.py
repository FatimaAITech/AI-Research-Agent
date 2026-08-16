from collections import deque

class TaskQueue:
    """
    Industry-Level Task Queue

    Responsible for:
    - FIFO task execution
    - Task scheduling
    - Queue management
    """

    def __init__(self):

        self.queue = deque()
    # ---------------------------------
    # Add Task
    # ---------------------------------
    def add(self, task):

        self.queue.append(task)
    # ---------------------------------
    # Add Multiple Tasks
    # ---------------------------------
    def extend(self, tasks):

        self.queue.extend(tasks)
    # ---------------------------------
    # Next Task
    # ---------------------------------
    def next_task(self):

        if self.queue:

            return self.queue.popleft()

        return None
    # ---------------------------------
    # Queue Size
    # ---------------------------------
    def size(self):

        return len(self.queue)
    # --------------------------------
    # Is Empty
    # ---------------------------------
    def empty(self):

        return len(self.queue) == 0
    # ---------------------------------
    # Clear Queue
    # ---------------------------------
    def clear(self):

        self.queue.clear()
    # ---------------------------------
    # Preview Queue
    # --------------------------------

    def tasks(self):

        return list(self.queue)