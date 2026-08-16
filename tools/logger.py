from datetime import datetime


class Logger:

    LOG_FILE = "logs/agent.log"

    @classmethod
    def log(cls, message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        line = f"[{timestamp}] {message}\n"

        with open(
            cls.LOG_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(line)