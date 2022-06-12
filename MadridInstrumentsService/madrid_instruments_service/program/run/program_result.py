"""Model for a program result."""

from pydantic import BaseModel, Field


class ProgramResult(BaseModel):
    result: int = Field(0, description="The result of the computation", example="69")
