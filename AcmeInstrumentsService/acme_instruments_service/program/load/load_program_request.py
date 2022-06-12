"""HTTP request for loading a program."""

from typing import List, Union

from pydantic import BaseModel, Field

from AcmeInstrumentsService.acme_instruments_service.pulse.pulse import Pulse


class LoadProgramRequest(BaseModel):
    """HTTP response for loading a program."""

    program_code: List[Union[Pulse, int]] = Field(
        ...,
        description="An ACME-specific pulse sequence representation of a quantum program",
        exmaple="['AcmePulse1','AcmePulse2','120']",
    )
