import json
import os
import unittest
import quantum_program_runner

test_instructions_list_dict = {
    'ACME': [],
    'MADRID': []
}

# Parses the json into a string to run a eval command for the result and returns the value
# Using this to confirm and assert that the result from the quantum program is accurate
def process_file(json_file):
    math_str = '(' * len(json_file['operations'])
    math_str = math_str + str(json_file['initial_value'])
    for i in json_file['operations']:
        operation = i['type']
        match operation:
            case 'Sum':
                math_str = math_str + '+'
            case 'Div':
                math_str = math_str + '/'
            case 'Mul':
                math_str = math_str + '*'
        math_str = math_str + str(i['value'])
        math_str = math_str + ')'
    result = int(eval(math_str))
    return result


class TestAcme(unittest.TestCase):

    def test_single_acme(self):
        """
        Tests running a single program for AcmeInstrumentsService
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        file_path = os.getcwd() + '/test_files/acme_single_test.json'
        file = open(file_path)
        acme_json = json.load(file)
        file.close()
        expected_result = process_file(acme_json)
        quantum_program_runner.parse_json(acme_json)
        result = quantum_program_runner.run_instruments_code()

        self.assertEqual(result['ACME'], expected_result)

    def test_long_acme(self):
        """
        Tests running a long list of programs for AcmeInstrumentsService
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        file_path = os.getcwd() + '/test_files/acme_list_test.json'
        file = open(file_path)
        acme_json = json.load(file)
        file.close()
        expected_result = []
        for i in acme_json:
            expected_result.append(process_file(i))
        quantum_program_runner.parse_json(acme_json)
        results = quantum_program_runner.run_instruments_code()
        self.assertEqual(results['ACME'], expected_result)


class TestMadrid(unittest.TestCase):

    def test_single_madrid(self):
        """
        Tests running a single program for MadridInstrumentsService
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        file_path = os.getcwd() + '/test_files/madrid_single_test.json'
        file = open(file_path)
        madrid_json = json.load(file)
        file.close()
        expected_result = process_file(madrid_json)
        quantum_program_runner.parse_json(madrid_json)
        result = quantum_program_runner.run_instruments_code()
        self.assertEqual(result['MADRID'], expected_result)

    def test_long_madrid(self):
        """
        Tests running a long list of programs for MadridInstrumentsService
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        file_path = os.getcwd() + '/test_files/madrid_list_test.json'
        file = open(file_path)
        madrid_json = json.load(file)
        file.close()
        expected_result = []
        for i in madrid_json:
            expected_result.append(process_file(i))
        quantum_program_runner.parse_json(madrid_json)
        results = quantum_program_runner.run_instruments_code()
        self.assertEqual(results['MADRID'], expected_result)


class TestSimultaneousFile(unittest.TestCase):

    def test_simultaneous_instruments(self):
        """
        Tests running a long list of programs for both AcmeInstrumentsService and
        MadridInstrumentsService in a random order
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        inside_instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        file_path = os.getcwd() + '/test_files/large_quantum_program_input.json'
        file = open(file_path)
        large_json = json.load(file)
        file.close()
        for i in large_json:
            result = process_file(i)
            if i['control_instrument'].upper() == 'MADRID':
                inside_instructions_list_dict['MADRID'].append(result)
            else:
                inside_instructions_list_dict['ACME'].append(result)
        quantum_program_runner.parse_json(large_json)
        results = quantum_program_runner.run_instruments_code()
        self.assertEqual(results['MADRID'], inside_instructions_list_dict['MADRID'])
        self.assertEqual(results['ACME'], inside_instructions_list_dict['ACME'])



class TestString(unittest.TestCase):

    def test_string_input(self):
        """
        Tests running a single program using string input
        """
        quantum_program_runner.instructions_list_dict = {
            'ACME': [],
            'MADRID': []
        }
        program_string = '{"id": "35d2b439-93af-c851-a62e-bc222021064e", "control_instrument": ' \
                         '"Madrid", "initial_value": 7, "operations": [{"type": "Sum", "value": 9},' \
                         ' {"type": "Div", "value": 7}, {"type": "Mul", "value": 8}]}'
        string_json = json.loads(program_string)
        expected_result = process_file(string_json)
        quantum_program_runner.parse_json(string_json)
        result = quantum_program_runner.run_instruments_code()
        self.assertEqual(result['MADRID'], expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
