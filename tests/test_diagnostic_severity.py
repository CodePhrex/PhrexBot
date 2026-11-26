import unittest
from diagnostic_severity import report_state
from diagnostic_renderer import diagnostic_payload

class SeverityTests(unittest.TestCase):
    def test_states(self):
        for line,key in [
            ("Outcomes: completed: 1, failed: 1, cancelled: 0","critical"),
            ("Outcomes: completed: 1, failed: 0, cancelled: 1","pending"),
            ("Outcomes: completed: 1, failed: 0, cancelled: 0","online"),
            ("Recorded terminal executions: 0","pending"),
            ("Not authorized.","secure"),
            ("PHREX | Diagnostic data unavailable.","critical"),
            ("Unknown report format","ai")]:
            self.assertEqual(report_state(line)[0],key)
        p=diagnostic_payload("Outcomes: completed: 1, failed: 1, cancelled: 0")
        self.assertIn(":phrex-critical:",p["blocks"][3]["elements"][0]["text"])
        self.assertEqual(p["response_type"],"ephemeral")
