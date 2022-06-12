"""Tests for running a program."""

import json
import unittest

from fastapi.testclient import TestClient

from madrid_instruments_service.main import app


class TestRunProgram(unittest.TestCase):
    """Tests for running a program."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_run_program_returns_195(self):
        # Load the program.
        pulse_sequence = (
            '{ "program_code": [10, "Madrid_initial_state_pulse", 120, "Madrid_pulse_1",'
            '3, "Madrid_pulse_2", "Madrid_pulse_2", 2, "Madrid_pulse_2",'
            '"Madrid_pulse_1"] }'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 200
        program_id = response.json()["program_id"]
        assert "MadridProgramId" in program_id

        # Run the program.
        response = self.client.get(f"/program/run/{program_id}")

        assert response.status_code == 200
        assert json.loads(response.content)["result"] == 195

    def test_run_program_not_found(self):
        # Load the program.
        pulse_sequence = (
            '{ "program_code": [10, "Madrid_initial_state_pulse", 120, "Madrid_pulse_1",'
            '3, "Madrid_pulse_2", "Madrid_pulse_2", 2, "Madrid_pulse_2",'
            '"Madrid_pulse_1"] }'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 200

        # Run the program.
        response = self.client.get("/program/run/bad_ID")

        assert response.status_code == 455

    def test_run_division_by_zero(self):
        # Load the program.
        pulse_sequence = (
            '{ "program_code": [10, "Madrid_initial_state_pulse", 120, "Madrid_pulse_1",'
            '3, "Madrid_pulse_2", "Madrid_pulse_2", 0, "Madrid_pulse_2",'
            '"Madrid_pulse_1"] }'
        )
        json_pulses = json.loads(pulse_sequence)
        response = self.client.post("/program/load", json=json_pulses)

        assert response.status_code == 200
        program_id = response.json()["program_id"]
        assert "MadridProgramId" in program_id

        # Run the program.
        response = self.client.get(f"/program/run/{program_id}")

        assert response.status_code == 456
