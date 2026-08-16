import time
import traceback
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base class for all agents.

    Features:
    - Logging
    - Execution timing
    - Error handling
    - Retry support
    - Shared state validation
    """

    def __init__(self, name: str):

        self.name = name

    # -------------------------------------------------
    # Main Entry
    # -------------------------------------------------

    def execute(self, state):

        print(f"\n{'=' * 12} {self.name.upper()} AGENT {'=' * 12}")

        start = time.time()

        try:

            self.validate_state(state)

            state = self.run(state)

            elapsed = round(time.time() - start, 2)

            print(f"\n✅ {self.name} completed in {elapsed}s")

            return state

        except Exception as e:

            elapsed = round(time.time() - start, 2)

            print(f"\n❌ {self.name} failed after {elapsed}s")

            print(f"Reason: {e}")

            traceback.print_exc()

            raise

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate_state(self, state):

        if state is None:

            raise ValueError("AgentState cannot be None.")

        if not hasattr(state, "topic"):

            raise ValueError("AgentState has no topic.")

    # -------------------------------------------------
    # Logging Helper
    # -------------------------------------------------

    def log(self, message):

        print(f"[{self.name}] {message}")

    # -------------------------------------------------
    # Retry Helper
    # -------------------------------------------------

    def retry(self, function, retries=3):

        last_error = None

        for attempt in range(1, retries + 1):

            try:

                return function()

            except Exception as e:

                last_error = e

                self.log(
                    f"Retry {attempt}/{retries} failed: {e}"
                )

        raise last_error

    # -------------------------------------------------
    # Every Agent Must Implement
    # -------------------------------------------------

    @abstractmethod
    def run(self, state):
        """
        Child agents implement their logic here.
        """
        pass
    