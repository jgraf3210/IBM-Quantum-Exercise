"""Converter from pulses to operations."""

from typing import List

from AcmeInstrumentsService.acme_instruments_service.operation.operations import (
    Division,
    Multiplication,
    SetInitialState,
    Summation,
)
from AcmeInstrumentsService.acme_instruments_service.program.errors import InvalidPulseSequenceError
from AcmeInstrumentsService.acme_instruments_service.pulse.pulse import Pulse

_PULSES_TO_OPERATION = {
    (Pulse.AcmePulse1, Pulse.AcmePulse2): Summation,
    (Pulse.AcmePulse2, Pulse.AcmePulse1, Pulse.AcmePulse1): Multiplication,
    (Pulse.AcmePulse2, Pulse.AcmePulse2): Division,
    (Pulse.AcmeInitialStatePulse,): SetInitialState,
}


def from_pulse_sequence_to_operation(pulses: List[Pulse], value: int):
    """Convert a pulse sequence into operators."""
    pulse_sequence_types = tuple(pulses)
    try:
        operation_class = _PULSES_TO_OPERATION[pulse_sequence_types]
    except KeyError:
        raise InvalidPulseSequenceError(
            f"There's no existing operation for this pulse sequence: {pulse_sequence_types}"
        )

    # Create an instance of the operation with its corresponding value.
    return operation_class(value=value)
