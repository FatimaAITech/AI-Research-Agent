from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()


class Config:
    """
    Central configuration for the AI Research Agent.
    """

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )

    # Application
    APP_NAME = os.getenv(
        "APP_NAME",
        "AI Research Agent"
    )

    @classmethod
    def validate(cls):
        """
        Validate required environment variables.
        """

        if not cls.GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is missing. "
                "Please add GROQ_API_KEY to your .env file."
            )

        return True


# Backward compatibility
# Existing project files can still use GROQ_API_KEY directly.
GROQ_API_KEY = Config.GROQ_API_KEY