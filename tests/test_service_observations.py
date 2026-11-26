import sqlite3
import tempfile
import unittest
from pathlib import Path
from contextlib import closing
from service_observations import collect, database_state

class ObservationTests(unittest.TestCase):
    def test_database(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.db'
            self.assertEqual(database_state(path), 'unknown')
            self.assertFalse(path.exists())
            with closing(sqlite3.connect(path)) as db:
                db.execute('CREATE TABLE fixture (id INTEGER)')
                db.commit()
            self.assertEqual(database_state(path), 'ok')
    def test_partial_observations(self):
        result = collect('unused', service_probe=lambda: 'ok', database_probe=lambda _: 'ok')
        self.assertEqual(result['status'], 'unverified')
        self.assertEqual(result['checks']['slack'], 'unknown')
    def test_stopped(self):
        result = collect('unused', service_probe=lambda: 'failed', database_probe=lambda _: 'ok')
        self.assertEqual(result['status'], 'critical')
