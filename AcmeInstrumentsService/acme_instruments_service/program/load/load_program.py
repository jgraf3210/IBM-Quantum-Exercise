"""Use case for loading a program."""

from typing import List, Union

import inject

from AcmeInstrumentsService.acme_instruments_service.program.errors import (
    MalformedProgramError,
    ValueNotAnIntegerError,
)
from AcmeInstrumentsService.acme_instruments_service.program.program_id import ProgramId
from AcmeInstrumentsService.acme_instruments_service.program.program_operations import ProgramOperations
from AcmeInstrumentsService.acme_instruments_service.program.pulse_to_operations import (
    from_pulse_sequence_to_operation,
)
from AcmeInstrumentsService.acme_instruments_service.pulse.pulse import Pulse


@inject.params(operations=ProgramOperations)
def load_program(
    program_code: List[Union[Pulse, int]], operations: ProgramOperations
) -> ProgramId:
    """Load the ACME pulse representation and translate it into a sequence of operations."""
    if len(program_code) == 0:
        raise MalformedProgramError("There are no pulse sequences in the program!")

    id_ = operations.new()
    # We only run one program at a time, so we remove previous operations everytime a new
    # program arrives.
    pulse_block = []
    # A block of pulses is defined by a sequence of pulses plus a value that ends the block.
    for pulse_or_value in program_code:
        if isinstance(pulse_or_value, Pulse):
            pulse_block.append(pulse_or_value)
        elif isinstance(pulse_or_value, int):
            operations.add_operation(
                from_pulse_sequence_to_operation(pulse_block, pulse_or_value)
            )
            pulse_block.clear()
        else:
            raise ValueNotAnIntegerError(
                f"The value ({pulse_or_value}) after the pulse sequence needs to be an integer!"
            )

    if len(pulse_block) > 0:
        raise MalformedProgramError(
            "There are malformed pulse sequences in the program!: "
            f"Malformed sequence: {pulse_block}"
        )

    return id_
