"""Dependency injection for MadridInstruments."""

import inject

from madrid_instruments_service.program.program_operations import ProgramOperations

program_operations = ProgramOperations()


def setup_dependencies():
    inject.configure(lambda binder: binder.bind(ProgramOperations, program_operations))
