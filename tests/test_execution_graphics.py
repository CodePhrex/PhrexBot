import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from execution_history import ExecutionHistory
from execution_graphics import execution_charts

class ExecutionGraphicsTests(unittest.TestCase):
    def test_charts(self):
        with TemporaryDirectory() as d:
            path=Path(d)/"history.db"
            with self.assertRaises(FileNotFoundError):
                execution_charts(path,"T1","U1")
            h=ExecutionHistory(path)
            h.record("abcdef123456","T1","U1","completed",0,28.5)
            h.record("abcdef123457","T1","U2","failed",99,99)
            charts=execution_charts(path,"T1","U1")
            self.assertEqual(len(charts),3)
            for png,alt in charts.values():
                self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
                self.assertIn("1 terminal executions",alt)
            self.assertIn("mean: 28.5",charts["execution_seconds"][1])
            self.assertIn("failed: 0",charts["outcomes"][1])
            self.assertIn("mean: missing",execution_charts(path,"T1","U3")["execution_seconds"][1])
            with self.assertRaises(ValueError):
                execution_charts(path,"T1","*")
