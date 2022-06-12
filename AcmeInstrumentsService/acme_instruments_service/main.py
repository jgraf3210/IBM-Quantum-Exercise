"""HTTP service for AcmeInstruments."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from AcmeInstrumentsService.acme_instruments_service.program.errors import (
    DivisionByZeroError,
    InvalidPulseSequenceError,
    MalformedProgramError,
    ProgramNotFoundError,
    ValueNotAnIntegerError,
)
from AcmeInstrumentsService.acme_instruments_service.program.load.load_program import load_program
from AcmeInstrumentsService.acme_instruments_service.program.load.load_program_request import (
    LoadProgramRequest,
)
from AcmeInstrumentsService.acme_instruments_service.program.load.load_program_response import (
    LoadProgramResponse,
)
from AcmeInstrumentsService.acme_instruments_service.program.program_id import ProgramId
from AcmeInstrumentsService.acme_instruments_service.program.run.run_program import run_program
from AcmeInstrumentsService.acme_instruments_service.program.run.run_program_response import RunProgramResponse

from AcmeInstrumentsService.acme_instruments_service.dependencies import setup_dependencies

app = FastAPI()

setup_dependencies()


@app.post("/load_program", response_model=LoadProgramResponse, status_code=200)
def load_program_endpoint(program_req: LoadProgramRequest):
    """Endpoint for loading a program."""
    program_id = load_program(program_req.program_code)
    return LoadProgramResponse(program_id=program_id)


@app.get("/run_program/{program_id}", response_model=RunProgramResponse, status_code=200)
def run_program_endpoint(program_id: ProgramId):
    """Endpoint for running a program."""
    result = run_program(program_id)
    return RunProgramResponse(program_id=program_id, result=result.result)


@app.exception_handler(InvalidPulseSequenceError)
async def invalid_pulse_sequence_exception_handler(
    _: Request, ex: InvalidPulseSequenceError
):
    """Handler for `InvalidPulseSequenceError`."""
    return JSONResponse(
        status_code=452,
        content={"message": f"{ex.name}"},
    )


@app.exception_handler(ValueNotAnIntegerError)
async def value_not_an_integer_exception_handler(_: Request, ex: ValueNotAnIntegerError):
    """Handler for `ValueNotAnIntegerError`."""
    return JSONResponse(
        status_code=453,
        content={"message": f"{ex.name}"},
    )


@app.exception_handler(MalformedProgramError)
async def malformed_program_exception_handler(_: Request, ex: MalformedProgramError):
    """Handler for `MalformedProgramError`."""
    return JSONResponse(
        status_code=454,
        content={"message": f"{ex.name}"},
    )


@app.exception_handler(ProgramNotFoundError)
async def program_not_found_exception_handler(_: Request, ex: ProgramNotFoundError):
    """Handler for `ProgramNotFoundError`."""
    return JSONResponse(
        status_code=455,
        content={"message": f"{ex.name}"},
    )


@app.exception_handler(DivisionByZeroError)
async def division_by_zero_exception_handler(_: Request, ex: DivisionByZeroError):
    """Handler for `DivisionByZeroError`."""
    return JSONResponse(
        status_code=456,
        content={"message": f"{ex.name}"},
    )
