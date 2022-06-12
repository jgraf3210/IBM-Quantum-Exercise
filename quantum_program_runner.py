#!/usr/bin/python3

import json
import time
from argparse import ArgumentParser
from instructions import *
import requests
import subprocess


# Dictionary of instruction set classes so that the translate_json method knows which instrument it is translating for.
# More useful so that I can get away from adding endless conditional statements and use just one line to index it
instructions_dict = {
    'ACME': AcmeInstructions,
    'MADRID': MadridInstructions,
}

# List of programs to run for each instrument. This makes it possible to run all the instrumensts in a single file
# and only have to open and close the service once in a run
instructions_list_dict = {
    'ACME': [],
    'MADRID': []
}

# Commands for starting the uvicorn services
instructions_uvicorn = {
    'ACME': ['uvicorn', 'AcmeInstrumentsService.acme_instruments_service.main:app'],
    'MADRID': ['uvicorn', 'MadridInstrumentsService.madrid_instruments_service.main:app']
}

# Generates the ArgumentParser for the program
def generate_parser():
    parser = ArgumentParser()
    parser.add_argument('-f', dest='file_path', help='Takes in a file for the input')
    parser.add_argument('-s', dest='json_string', help='Takes a string of a json')
    return parser


# Translates the json input into the required program code
def translate_json(quantum_json):
    """
    Processes the json and translates the high level commands into the low level pulses for the selected instrument.
    The processed code is returned.
    """
    control_instrument = quantum_json['control_instrument']
    initial_value = quantum_json['initial_value']
    operations = quantum_json['operations']
    instructions = instructions_dict[control_instrument.upper()]
    program_json = json.loads('{"program_code":[]}')
    program_code = program_json['program_code']
    for step in instructions.initial:
        if step == 'Value':
            step = initial_value
        program_code.append(step)
    for operation in operations:
        steps = None
        match operation['type']:
            case 'Sum':
                steps = instructions.sum
            case 'Mul':
                steps = instructions.mul
            case 'Div':
                steps = instructions.div
            case 'Initial':
                steps = instructions.initial
        for step in steps:
            if step == 'Value':
                step = operation['value']
            program_code.append(step)
    return program_json


def process_quantum_code(code, instrument):
    """
    Processes the single program
    """
    instruction = instructions_dict[instrument]
    post_endpoint = 'http://127.0.0.1:8000' + instruction.post_endpoint
    r = requests.post(post_endpoint, json=code)
    content = r.content.decode('utf-8')
    content_json = json.loads(content)
    program_id = content_json['program_id']
    run_endpoint = 'http://127.0.0.1:8000' + instruction.run_endpoint + program_id
    response = requests.get(run_endpoint)
    content = response.content.decode('utf-8')
    content_json = json.loads(content)
    result = content_json['result']
    return result


def parse_json(quantum_json):
    """
    Calls the needed functions to translate the code if the json is a single program or if it is a list of programs. The
    translated code is then stored into their respective lists in instructions_list_dict dictionary at the top.
    """
    # If the json is a list of json objects, iterate through each one and translate the programs
    if isinstance(quantum_json, list):
        for i in quantum_json:
            dict_str = json.dumps(i, indent=4)
            json_tmp = json.loads(dict_str)
            program_code = translate_json(json_tmp)
            program_list = instructions_list_dict[i['control_instrument'].upper()]
            program_list.append(program_code)
    # Else translate and store the single program
    else:
        program_code = translate_json(quantum_json)
        program_list = instructions_list_dict[quantum_json['control_instrument'].upper()]
        program_list.append(program_code)


def run_instruments_code():
    """
    Iterates through the dictionary of instrument programs and runs them one by one if the instrument has programs to
    run. The instance of the instrument service is started and closed only if the instrument has programs in the array.
    """
    results = {}
    for instrument in instructions_list_dict:
        if instructions_list_dict[instrument]:
            if len(instructions_list_dict[instrument]) > 1:
                results[instrument] = []  # Create a blank list for the results
                command = instructions_uvicorn[instrument]
                print('Starting service for ' + instrument)
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                time.sleep(1)   # Give the service a second to finish starting before sending code to it.
                for program in instructions_list_dict[instrument]:
                    result = process_quantum_code(program, instrument)
                    results[instrument].append(result)
                print('Stopping service for ' + instrument)
                process.kill()
                process.wait()
            else:
                results = {}
                command = instructions_uvicorn[instrument]
                print('Starting service for ' + instrument)
                # subprocess.PIPE prevents all the response text from returning to stdout
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                time.sleep(1)   # Give the service a second to finish starting before sending code to it.
                for program in instructions_list_dict[instrument]:
                    result = process_quantum_code(program, instrument)
                    results[instrument] = result
                print('Stopping service for ' + instrument)
                process.kill()
                process.wait()
    return results  # Return value is for testing and debugging

def main():
    parser = generate_parser()
    args = parser.parse_args()
    # This program prioritizes files
    if args.file_path:
        file_path = args.file_path
        file = open(file_path)
        quantum_json = json.load(file)
        file.close()
    else:
        json_string = args.json_string
        quantum_json = json.loads(json_string)
    parse_json(quantum_json)
    result = run_instruments_code()
    print(result)

if __name__ == "__main__":
    main()
