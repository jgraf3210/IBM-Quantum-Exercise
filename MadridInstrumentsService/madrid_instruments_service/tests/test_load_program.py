"""Tests for loading a program."""

import json
import unittest

from fastapi.testclient import TestClient

from madrid_instruments_service.main import app


class TestLoadProgram(unittest.TestCase):
    """Tests for loading a program."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_load_program_returns_ok(self):
        pulse_sequence = (
            '{"program_code": [10,  "Madrid_initial_state_pulse", 120, "Madrid_pulse_1", 3,'
            '"Madrid_pulse_2", "Madrid_pulse_2", 2, "Madrid_pulse_2", "Madrid_pulse_1"]}'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)
        assert response.status_code == 200
        assert "MadridProgramId" in response.json()["program_id"]

    def test_load_pulse_sequence_doesnt_exist(self):
        pulse_sequence = (
            '{"program_code": ['
            '  10, "Madrid_initial_state_pulse",'
            '  2, "Madrid_pulse_1", "Madrid_pulse_1", "Madrid_pulse_2"'
            "]}"
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 452

    def test_load_malformed_sequence_in_program(self):
        pulse_sequence = '{ "program_code": ["Madrid_initial_state_pulse"] }'
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 454

    def test_load_empty_program(self):
        # We first load the program
        pulse_sequence = '{ "program_code": [] }'
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 454
