from pathlib import Path
import unittest

from mbselang.parser import load, parse
from mbselang.render import render_mermaid
from mbselang.runtime import run_scenario
from mbselang.trace import trace_requirement
from mbselang.validate import validate


EXAMPLE = Path(__file__).parents[1] / "examples" / "rover" / "rover.mbse"


class VerticalSliceTests(unittest.TestCase):
    def test_rover_model_validates(self) -> None:
        model = load(EXAMPLE)
        self.assertEqual(model.name, "Rover")
        self.assertFalse([item for item in validate(model) if item.severity == "error"])

    def test_braking_scenario_verifies_requirement(self) -> None:
        result = run_scenario(load(EXAMPLE), "braking_test")
        self.assertTrue(result.passed)
        self.assertAlmostEqual(result.values["emergency_stop.stopping_distance"].value, 4 / 3)
        self.assertEqual(result.verified_requirements, ["REQ-001"])

    def test_trace_links_requirement_to_design_and_scenario(self) -> None:
        trace = trace_requirement(load(EXAMPLE), "REQ-001")
        self.assertEqual(trace["satisfied_by"], ["Rover"])
        self.assertEqual(trace["verified_by"], ["braking_test"])

    def test_render_contains_architecture_connections(self) -> None:
        diagram = render_mermaid(load(EXAMPLE))
        self.assertIn("controller -- motor_command to command --> motor", diagram)
        self.assertIn("battery -- power to power --> motor", diagram)

    def test_validator_detects_interface_mismatch(self) -> None:
        text = EXAMPLE.read_text().replace("port command: Command in", "port command: Torque in")
        errors = [item.message for item in validate(parse(text)) if item.severity == "error"]
        self.assertTrue(any("incompatible interfaces" in message for message in errors))

    def test_validator_detects_unit_mismatch(self) -> None:
        text = EXAMPLE.read_text().replace("set rover.speed = 2 m/s", "set rover.speed = 2 km")
        errors = [item.message for item in validate(parse(text)) if item.severity == "error"]
        self.assertTrue(any("unit mismatch" in message for message in errors))

    def test_parser_accepts_tab_indentation(self) -> None:
        text = """model Tiny

requirement works:
\tid: REQ-001
\tshall result == 1 m
\tverify_by test

scenario proof:
\tassert 1 == 1
\tverifies REQ-001
"""
        model = parse(text)
        self.assertEqual(model.requirements["works"].identifier, "REQ-001")
        self.assertEqual(model.scenarios["proof"].verifies, ["REQ-001"])

    def test_parser_rejects_mixed_indentation(self) -> None:
        text = "model Tiny\nrequirement bad:\n  \tid: REQ-001\n"
        with self.assertRaisesRegex(ValueError, "do not mix spaces and tabs"):
            parse(text)


if __name__ == "__main__":
    unittest.main()
