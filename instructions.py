"""
    File is for storing the instruction sets for respective instruction sets. Should be expandable since you can just
    add another array of values to load the more instructions as more come along.
"""

class ArithmeticInstructions():
    """

    """
    sum = []
    mul = []
    div = []
    initial = []
    post_endpoint = ''
    run_endpoint = ''


# Arithmetic instructions for Acme
class AcmeInstructions(ArithmeticInstructions):

    sum = ['Acme_pulse_1', 'Acme_pulse_2', 'Value']
    mul = ['Acme_pulse_2', 'Acme_pulse_1', 'Acme_pulse_1', 'Value']
    div = ['Acme_pulse_2', 'Acme_pulse_2', 'Value']
    initial = ['Acme_initial_state_pulse', 'Value']
    post_endpoint = '/load_program'
    run_endpoint = '/run_program/'
    service_command = 'uvicorn AcmeInstrumentService.acme_instructions_service.main:app'


# Arithmetic instructions for Madrid
class MadridInstructions(ArithmeticInstructions):

    sum = ['Value', 'Madrid_pulse_1']
    mul = ['Value', 'Madrid_pulse_2', 'Madrid_pulse_2']
    div = ['Value', 'Madrid_pulse_2', 'Madrid_pulse_1']
    initial = ['Value', 'Madrid_initial_state_pulse']
    post_endpoint = '/program/load'
    run_endpoint = '/program/run/'
    service_command = 'uvicorn MadridInstrumentService.madrid_instructions_service.main:app'
