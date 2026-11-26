import sqlite3
import unittest
from contextlib import closing
from tempfile import TemporaryDirectory
from pathlib import Path
from execution_history import ExecutionHistory

class FailureTests(unittest.TestCase):
    def test_migration(self):
        with TemporaryDirectory() as d:
            path=Path(d)/"history.db"
            with closing(sqlite3.connect(path)) as db, db:
                db.execute("CREATE TABLE executions (id TEXT PRIMARY KEY,team TEXT,owner TEXT,ended REAL,outcome TEXT,queue_seconds REAL,execution_seconds REAL)")
            h=ExecutionHistory(path)
            h.record("abcdef123456","T1","U1","failed",1,2,"timeout")
            with closing(sqlite3.connect(path)) as db:
                self.assertEqual(db.execute("SELECT failure_code FROM executions").fetchone(),("timeout",))
            with self.assertRaises(ValueError):
                h.record("abcdef123457","T1","U1","failed",1,2,"raw exception text")
