"""Use case for loading a program."""

from turtle import pu
from typing import List, Union

import inject

from madrid_instruments_service.program.errors import (
    MalformedProgramError,
    ValueNotAnIntegerError,
)
from madrid_instruments_service.program.program_id import ProgramId
from madrid_instruments_service.program.program_operations import ProgramOperations
from madrid_instruments_service.program.pulse_to_operations import (
    from_pulse_sequence_to_operation,
)
from madrid_instruments_service.pulse.pulse import Pulse


@inject.params(operations=ProgramOperations)
def load_program(program_code: List[Union[Pulse, int]], operations: ProgramOperations) -> ProgramId:
    """Load the Madrid pulse representation and translate it into a sequence of operations."""
    if len(program_code) == 0:
        raise MalformedProgramError("There are no pulse sequences in the program!")

    id_ = operations.new()
    # We only run one program at a time, so we remove previous operations everytime a new
    # program arrives.
    pulse_block = []
    # A block of pulses is defined by a sequence of pulses plus a value that ends the block.
    for pulse_or_value in program_code:
        if len(pulse_block) == 0:
            # First instruction must be the value of the operation
            if not isinstance(pulse_or_value, int):
                raise MalformedProgramError(
                    f"The first element in the pulse sequence must be the value of the operation!"
                )
            pulse_block.append(pulse_or_value)
            continue

        if isinstance(pulse_or_value, Pulse):
            pulse_block.append(pulse_or_value)
        elif isinstance(pulse_or_value, int):
            # An integer (or value) represents the initial element of a new pulse sequence
            # so we clean up and start a new sequence block
            operations.add_operation(from_pulse_sequence_to_operation(pulse_block))
            pulse_block.clear()
            pulse_block.append(pulse_or_value)

    operations.add_operation(from_pulse_sequence_to_operation(pulse_block))

    return id_
