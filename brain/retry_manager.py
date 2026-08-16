import time


class RetryManager:
    """
    Industry-Level Retry Manager

    Features:
    - Automatic retries
    - Exponential backoff
    - Failure handling
    """

    def __init__(
        self,
        max_retries=3,
        base_delay=1
    ):

        self.max_retries = max_retries
        self.base_delay = base_delay

    # ---------------------------------
    # Execute With Retry
    # ---------------------------------

    def execute(self, func, *args, **kwargs):

        last_exception = None

        for attempt in range(1, self.max_retries + 1):

            try:

                return func(*args, **kwargs)

            except Exception as e:

                last_exception = e

                print(
                    f"⚠ Retry {attempt}/{self.max_retries}"
                    f" failed: {e}"
                )

                if attempt < self.max_retries:

                    delay = self.base_delay * (2 ** (attempt - 1))

                    print(
                        f"⏳ Waiting {delay} second(s)..."
                    )

                    time.sleep(delay)

        raise last_exception