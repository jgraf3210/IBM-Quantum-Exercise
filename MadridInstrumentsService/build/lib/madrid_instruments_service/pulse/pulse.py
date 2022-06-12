"""Model for a pulse."""

from enum import Enum


class Pulse(str, Enum):
    """Model for a pulse."""

    MadridPulse1 = "Madrid_pulse_1"
    MadridPulse2 = "Madrid_pulse_2"
    MadridPulse3 = "Madrid_pulse_3"
    MadridInitialStatePulse = "Madrid_initial_state_pulse"
