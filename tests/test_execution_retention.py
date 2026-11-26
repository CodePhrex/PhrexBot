import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from execution_history import ExecutionHistory
from execution_retention import prune

class RetentionTests(unittest.TestCase):
    def test_cleanup(self):
        with TemporaryDirectory() as d:
            path=Path(d)/"history.db"
            self.assertEqual(prune(path),0)
            self.assertFalse(path.exists())
            h=ExecutionHistory(path)
            with patch("execution_history.time",return_value=100):
                h.record("abcdef123456","T1","U1","completed",1,2)
            self.assertEqual(prune(path,100+31*86400),1)
            self.assertEqual(prune(path,100+31*86400),0)
