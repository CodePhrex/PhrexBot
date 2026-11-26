import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from execution_history import ExecutionHistory

class HistoryTests(unittest.TestCase):
    def test_persistence_and_scope(self):
        with TemporaryDirectory() as directory:
            path=Path(directory)/"history.db"
            h=ExecutionHistory(path)
            h.record("abcdef123456","T1","U1","completed",1,2)
            self.assertEqual(len(ExecutionHistory(path).recent("T1","U1")),1)
            self.assertEqual(h.recent("T1","U2"),[])
            self.assertEqual(h.recent("T2","U1"),[])
            with self.assertRaises(ValueError):
                h.record("abcdef123457","T1","U1","unknown",1,2)
