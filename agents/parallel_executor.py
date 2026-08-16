from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelExecutor:
    """
    Industry-Level Parallel Executor

    Executes multiple independent agent tasks
    concurrently.
    """

    def __init__(self, max_workers=4):

        self.max_workers = max_workers

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, tasks):

        """
        tasks:

        [
            (callable, arg1, arg2),
            (callable, arg1),
            ...
        ]
        """

        results = []

        with ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:

            futures = []

            for task in tasks:

                fn = task[0]

                args = task[1:]

                futures.append(
                    executor.submit(
                        fn,
                        *args
                    )
                )

            for future in as_completed(futures):

                results.append(
                    future.result()
                )

        return results