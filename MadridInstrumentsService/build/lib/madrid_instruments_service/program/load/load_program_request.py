"""HTTP request for loading a program."""

from typing import List, Union

from pydantic import BaseModel, Field

from madrid_instruments_service.pulse.pulse import Pulse


class LoadProgramRequest(BaseModel):
    """HTTP response for loading a program."""

    program_code: List[Union[Pulse, int]] = Field(
        ...,
        description="An Madrid-specific pulse sequence representation of a quantum program",
        exmaple="['MadridPulse1','MadridPulse2','120']",
    )
