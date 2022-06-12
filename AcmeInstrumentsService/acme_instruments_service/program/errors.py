"""Errors related to programs."""


class InvalidPulseSequenceError(Exception):
    def __init__(self, description: str):
        self.name = description


class MalformedProgramError(Exception):
    def __init__(self, description: str):
        self.name = description


class ValueNotAnIntegerError(Exception):
    def __init__(self, description: str):
        self.name = description


class ProgramNotFoundError(Exception):
    def __init__(self, description: str):
        self.name = description


class DivisionByZeroError(Exception):
    def __init__(self, description: str):
        self.name = description
