from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ResearchRequest(BaseModel):
    """
    Input contract for the research service/API.
    """

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Research topic to investigate."
    )


class ResearchResponse(BaseModel):
    """
    Output contract returned by the research service/API.
    """

    model_config = ConfigDict(extra="forbid")

    success: bool = Field(
        ...,
        description="Whether the research request completed successfully."
    )

    topic: str = Field(
        ...,
        description="Research topic."
    )

    report: str | None = Field(
        default=None,
        description="Generated research report."
    )

    error: str | None = Field(
        default=None,
        description="Error message when the request fails."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional service metadata."
    )