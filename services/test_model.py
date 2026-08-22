from pydantic import ValidationError

from services.models import ResearchRequest


try:
    ResearchRequest(topic="")
except ValidationError:
    print("Validation working successfully.")
else:
    print("❌ Validation failed.")