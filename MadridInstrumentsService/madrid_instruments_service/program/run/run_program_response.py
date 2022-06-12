"""HTTP response for running a program."""

from pydantic import BaseModel, Field


class RunProgramResponse(BaseModel):
    """HTTP response for loading a program."""

    result: int = Field(
        ...,
        description="A number representing the result of the program run",
        example="10",
    )
