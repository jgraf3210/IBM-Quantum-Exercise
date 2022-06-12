"""Converter from pulses to operations."""

from typing import List

from madrid_instruments_service.operation.operations import (
    Division,
    Multiplication,
    SetInitialState,
    Summation,
)
from madrid_instruments_service.program.errors import InvalidPulseSequenceError
from madrid_instruments_service.pulse.pulse import Pulse

_PULSES_TO_OPERATION = {
    (Pulse.MadridPulse1,): Summation,
    (Pulse.MadridPulse2, Pulse.MadridPulse2): Multiplication,
    (Pulse.MadridPulse2, Pulse.MadridPulse1): Division,
    (Pulse.MadridInitialStatePulse,): SetInitialState,
}


def from_pulse_sequence_to_operation(pulses: List[Pulse]):
    """Convert a pulse sequence into operators."""
    value = pulses[0]
    pulses = pulses[1:]
    pulse_sequence_types = tuple(pulses)
    try:
        operation_class = _PULSES_TO_OPERATION[pulse_sequence_types]
    except KeyError:
        raise InvalidPulseSequenceError(
            f"There's no existing operation for this pulse sequence: {pulse_sequence_types}"
        )

    # Create an instance of the operation with its corresponding value.
    return operation_class(value=value)
