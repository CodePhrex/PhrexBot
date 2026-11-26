import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from execution_history import ExecutionHistory
from diagnostic_commands import diagnostic_command

class DiagnosticTests(unittest.TestCase):
    def test_reports(self):
        with TemporaryDirectory() as d, patch("diagnostic_commands.data_root",return_value=Path(d)):
            body={"team_id":"T1","user_id":"U1"}
            self.assertIn("No execution history",diagnostic_command("metrics",body))
            h=ExecutionHistory(Path(d)/"execution-history.db")
            h.record("abcdef123456","T1","U1","failed",1,2,"timeout")
            h.record("abcdef123457","T1","U2","completed",1,99)
            self.assertIn("abcdef123456",diagnostic_command("history",body))
            self.assertNotIn("abcdef123457",diagnostic_command("history",body))
            self.assertIn("timeout: 1",diagnostic_command("diagnostics",body))
            self.assertIn("Recorded terminal executions: 1",diagnostic_command("metrics",body))
            self.assertIn("Usage:",diagnostic_command("performance 31",body))
            self.assertEqual(diagnostic_command("history",{}),"Not authorized.")
