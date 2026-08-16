from time import sleep


class Retry:

    def __init__(self, retries=3, delay=2):

        self.retries = retries
        self.delay = delay

    def execute(self, func, *args, **kwargs):

        last_error = None

        for attempt in range(1, self.retries + 1):

            try:

                return func(*args, **kwargs)

            except Exception as e:

                last_error = e

                print(
                    f"⚠ Retry {attempt}/{self.retries} failed:"
                )

                print(e)

                if attempt < self.retries:

                    sleep(self.delay)

        raise last_error