"""Use case for running a program."""

import inject

from AcmeInstrumentsService.acme_instruments_service.program.program_id import ProgramId
from AcmeInstrumentsService.acme_instruments_service.program.program_operations import ProgramOperations
from AcmeInstrumentsService.acme_instruments_service.program.run.program_result import ProgramResult


@inject.params(operations=ProgramOperations)
def run_program(program_id: ProgramId, operations: ProgramOperations) -> ProgramResult:
    """Run program use case."""
    return operations.run(program_id)
