import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from execution_history import ExecutionHistory
from execution_metrics import metrics, latency

class MetricsTests(unittest.TestCase):
    def test_latency(self):
        self.assertEqual(latency([1,2,3,4])["median"],2.5)
        self.assertEqual(latency(list(range(1,101)))["p95"],95)
        self.assertIsNone(latency([]))

    def test_scope(self):
        with TemporaryDirectory() as d:
            path=Path(d)/"history.db"
            h=ExecutionHistory(path)
            h.record("abcdef123456","T1","U1","completed",1,2)
            h.record("abcdef123457","T1","U1","failed",3,4)
            h.record("abcdef123458","T1","U2","completed",99,99)
            m=metrics(path,"T1","U1")
            self.assertEqual(m["total"],2)
            self.assertEqual(m["completion_rate"],.5)
            self.assertEqual(m["execution_seconds"]["mean"],3)
            self.assertIsNone(metrics(path,"T2","U1")["completion_rate"])
            with self.assertRaises(ValueError):
                metrics(path,"T1","*")
