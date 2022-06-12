"""Model for program operations."""

from dataclasses import dataclass, field
from typing import Dict, List

from AcmeInstrumentsService.acme_instruments_service.operation.operations import Operation
from AcmeInstrumentsService.acme_instruments_service.program.errors import (
    DivisionByZeroError,
    ProgramNotFoundError,
)
from AcmeInstrumentsService.acme_instruments_service.program.program_id import ProgramId
from AcmeInstrumentsService.acme_instruments_service.program.run.program_result import ProgramResult


@dataclass
class ProgramOperations:
    """Model for program operations."""

    operations: Dict[ProgramId, List[Operation]] = field(default_factory=dict)
    id: ProgramId = ""
    counter: int = 0

    def run(self, program_id: ProgramId) -> ProgramResult:
        try:
            program_to_run = self.operations[program_id]
        except KeyError:
            raise ProgramNotFoundError(f"The program with ID {program_id} wasn't found")

        result = 0
        for operation in program_to_run:
            try:
                result = operation.operator(result, operation.value)
            except ZeroDivisionError:
                raise DivisionByZeroError("Division by zero!!")

        del self.operations[program_id]
        return ProgramResult(result=result)

    def new(self) -> ProgramId:
        self.counter += 1
        self.id = ProgramId(f"AcmeProgramId{self.counter}")
        self.operations[self.id] = []
        return self.id

    def add_operation(self, operation: Operation):
        if not isinstance(operation, Operation):
            raise TypeError(
                f"Operation type not recognized {operation.__class__.__name__}"
            )
        self.operations[self.id].append(operation)
