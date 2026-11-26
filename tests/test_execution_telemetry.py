import unittest
from unittest.mock import patch, Mock
from pathlib import Path
from tempfile import TemporaryDirectory
from execution_telemetry import record_execution
from execution_history import ExecutionHistory

class TelemetryTests(unittest.TestCase):
    def test_record(self):
        with TemporaryDirectory() as directory, patch("execution_telemetry.data_root",return_value=Path(directory)):
            self.assertTrue(record_execution("abcdef123456","T1","U1","completed",1,2,Mock()))
            self.assertEqual(len(ExecutionHistory(Path(directory)/"execution-history.db").recent("T1","U1")),1)

    def test_failure(self):
        with patch("execution_telemetry.data_root",side_effect=OSError):
            self.assertFalse(record_execution("abcdef123456","T1","U1","failed",1,2,Mock()))
