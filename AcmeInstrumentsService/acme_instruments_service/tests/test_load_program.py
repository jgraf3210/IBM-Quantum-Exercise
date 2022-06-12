"""Tests for loading a program."""

import json
import unittest

from fastapi.testclient import TestClient

from AcmeInstrumentsService.acme_instruments_service.main import app


class TestLoadProgram(unittest.TestCase):
    """Tests for loading a program."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_load_program_returns_ok(self):
        pulse_sequence = (
            '{ "program_code": ["Acme_initial_state_pulse", 10,"Acme_pulse_1", "Acme_pulse_2",'
            '120, "Acme_pulse_2", "Acme_pulse_1", "Acme_pulse_1", 3, "Acme_pulse_2",'
            '"Acme_pulse_2", 2] }'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/load_program", json=json_pulses)
        assert response.status_code == 200
        assert "AcmeProgramId" in response.json()["program_id"]

    def test_load_pulse_sequence_doesnt_exist(self):
        pulse_sequence = (
            '{ "program_code": ["Acme_initial_state_pulse", 10, "Acme_pulse_1", "Acme_pulse_1",'
            '"Acme_pulse_2", 2] }'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/load_program", json=json_pulses)

        assert response.status_code == 452

    def test_load_malformed_sequence_in_program(self):
        pulse_sequence = '{ "program_code": ["Acme_initial_state_pulse"] }'
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/load_program", json=json_pulses)

        assert response.status_code == 454

    def test_load_empty_program(self):
        # We first load the program
        pulse_sequence = '{ "program_code": [] }'
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/load_program", json=json_pulses)

        assert response.status_code == 454
