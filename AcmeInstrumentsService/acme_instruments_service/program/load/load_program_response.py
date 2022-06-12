"""HTTP response for loading a program."""

from pydantic import BaseModel, Field

from AcmeInstrumentsService.acme_instruments_service.program.program_id import ProgramId


class LoadProgramResponse(BaseModel):
    """HTTP response for loading a program."""

    program_id: ProgramId = Field(
        ...,
        description="ID of the program loaded in the instruments ready to be run",
        example="1234-5678-9012-3456",
    )
